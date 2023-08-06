from unittest import mock
from uuid import uuid4

from celery.exceptions import MaxRetriesExceededError

from ussd.tasks import report_session
from ussd.tests import UssdTestCase
from ussd.tests.utils import MockResponse
from celery import current_app


class TestingUssdReportSession(UssdTestCase.BaseUssdTestCase):

    def setUp(self):
        current_app.conf.task_always_eager = True
        super(TestingUssdReportSession, self).setUp()
        self.journey_name = "sample_journey"
        self.valid_version = "sample_report_session"
        # self.valid_yml = self.customer_journey_to_use

    def get_ussd_client(self, journey_name="sample_journey",
                        journey_version="sample_report_session"):
        return self.ussd_client(
            generate_customer_journey=False,
            extra_payload={
                "journey_name": journey_name,
                "journey_version": journey_version
            }
        )

    @mock.patch("ussd.core.report_session.apply_async")
    def test_report_session_task(self, report_mock):
        ussd_client = self.get_ussd_client()

        self.assertEqual(
            "Enter you name\n",
            ussd_client.send('')  # dial in
        )

        report_mock.assert_called_once_with(
            args=(ussd_client.session_id,),
            kwargs=dict(
                screen_content={
                    "type": "initial_screen",
                    "next_screen": "screen_one",
                    "ussd_report_session": {
                        "session_key": "reported",
                        "validate_response": [
                            {"expression": "{{reported.status_code}} == 200"}
                        ],
                        "retry_mechanism": {
                            "max_retries": 3
                        },
                        "request_conf": {
                            "url": "localhost:8006/api",
                            "method": "post",
                            "data": {
                                "ussd_interaction": "{{ussd_interaction}}",
                                "session_id": "{{session_id}}"
                            }
                        },
                        "async_parameters": {
                            "queue": "report_session",
                            "countdown": 900
                        }
                    }
                }
            ),
            queue="report_session",
            countdown=900
        )

    @mock.patch("ussd.core.report_session.apply_async")
    def test_quit_screen_sends_report_session(self, mock_report_session):
        ussd_client = self.get_ussd_client()

        self.assertEqual(
            "Enter you name\n",
            ussd_client.send('')  # dial in
        )

        self.assertEqual(
            "Your name is test",
            ussd_client.send('test')  # enter name as test.
        )

        self.assertEqual(mock_report_session.call_count, 2)

        expected_calls = [
            mock.call(
                args=(ussd_client.session_id,),
                kwargs=dict(
                    screen_content={
                        "type": "initial_screen",
                        "next_screen": "screen_one",
                        "ussd_report_session": {
                            "session_key": "reported",
                            "validate_response": [
                                {"expression":
                                     "{{reported.status_code}} == 200"}
                            ],
                            "retry_mechanism": {
                                "max_retries": 3
                            },
                            "request_conf": {
                                "url": "localhost:8006/api",
                                "method": "post",
                                "data": {
                                    "ussd_interaction": "{{ussd_interaction}}",
                                    "session_id": "{{session_id}}"
                                }
                            },
                            "async_parameters": {
                                "queue": "report_session",
                                "countdown": 900
                            }
                        }
                    }
                ),
                queue="report_session",
                countdown=900
            ),
            mock.call(
                args=(ussd_client.session_id,),
                kwargs=dict(
                    screen_content={
                        "type": "initial_screen",
                        "next_screen": "screen_one",
                        "ussd_report_session": {
                            "session_key": "reported",
                            "validate_response": [
                                {"expression":
                                     "{{reported.status_code}} == 200"}
                            ]
                            ,
                            "retry_mechanism": {
                                "max_retries": 3
                            },
                            "request_conf": {
                                "url": "localhost:8006/api",
                                "method": "post",
                                "data": {
                                    "ussd_interaction": "{{ussd_interaction}}",
                                    "session_id": "{{session_id}}"
                                }
                            },
                            "async_parameters": {
                                "queue": "report_session",
                                "countdown": 900
                            }
                        }
                    }
                ),
                queue="report_session",
            )
        ]

        mock_report_session.assert_has_calls(expected_calls)

    @mock.patch('ussd.core.requests.request')
    def test_http_call(self, mock_request):
        mock_response = MockResponse({"balance": 250})
        mock_request.return_value = mock_response

        session = self.ussd_session(str(uuid4()))
        session['session_id'] = session.session_key
        session['ussd_interaction'] = []
        session.save()

        screen_content = {
            "type": "initial_screen",
            "next_screen": "screen_one",
            "ussd_report_session": {
                "session_key": "reported",
                "retry_mechanism": {
                    "max_retries": 3
                },
                "validate_response": [
                    {"expression":
                         "{{reported.status_code}} == 200"}
                ],
                "request_conf": {
                    "url": "localhost:8006/api",
                    "method": "post",
                    "data": {
                        "ussd_interaction": "{{ussd_interaction}}",
                        "session_id": "{{session_id}}"
                    }
                },
                "async_parameters": {
                    "queue": "report_session",
                    "countdown": 900
                }
            }
        }

        report_session.delay(
            session.session_key,
            screen_content
        )

        mock_request.assert_called_once_with(
            url="localhost:8006/api",
            method="post",
            data=dict(
                ussd_interaction=[],
                session_id=session.session_key
            )
        )

    @mock.patch("ussd.tasks.requests.request")
    def test_if_session_is_already_posted_wont_post_again(self, mock_request):
        mock_response = MockResponse({"balance": 250})
        mock_request.return_value = mock_response

        session = self.ussd_session(str(uuid4()))
        session['session_id'] = session.session_key
        session['ussd_interaction'] = []
        session['posted'] = True
        session.save()

        screen_content = {
            "type": "initial_screen",
            "next_screen": "screen_one",
            "ussd_report_session": {
                "session_key": "reported",
                "retry_mechanism": {
                    "max_retries": 3
                },
                "validate_response": [
                    {"expression":
                         "{{reported.status_code}} == 200"}
                ],
                "request_conf": {
                    "url": "localhost:8006/api",
                    "method": "post",
                    "data": {
                        "ussd_interaction": "{{ussd_interaction}}",
                        "session_id": "{{session_id}}"
                    }
                },
                "async_parameters": {
                    "queue": "report_session",
                    "countdown": 900
                }
            }
        }

        report_session.delay(
            session.session_key,
            screen_content
        )
        self.assertFalse(mock_request.called)

    @mock.patch("requests.request")
    @mock.patch.object(report_session, 'retry')
    def test_retry(self, mock_retry, mock_request):
        mock_response = MockResponse({"balance": 250},
                                     status=400
                                     )
        mock_request.return_value = mock_response
        ussd_client = self.get_ussd_client()
        ussd_client.send('mwas')

        # check posted flag has been set to false
        self.assertFalse(
            self.ussd_session(ussd_client.session_id)['posted'],
        )

        self.assertTrue(mock_retry.called)

    @mock.patch("ussd.core.report_session.apply_async")
    def test_report_task_only_called_when_activated(self, mock_report_session):
        # using a journey that report_session has not been activated
        # and one that has quit screen
        ussd_client = self.get_ussd_client(journey_name="quit_screen", journey_version="valid_quit_screen_conf")

        self.assertEqual(
            "Test getting variable from os environmen. variable_test",
            ussd_client.send('')  # dial in
        )

    @mock.patch("ussd.core.requests.request")
    @mock.patch.object(report_session, 'retry')
    def test_maximum_retries(self, mock_retry, mock_request):
        mock_response = MockResponse({"balance": 250},
                                     status=400
                                     )
        mock_request.return_value = mock_response
        mock_retry.side_effect = MaxRetriesExceededError()

        ussd_client = self.get_ussd_client()
        ussd_client.send('mwas')

    def testing_invalid_customer_journey(self):
        # this is tested in the initial screen
        pass
