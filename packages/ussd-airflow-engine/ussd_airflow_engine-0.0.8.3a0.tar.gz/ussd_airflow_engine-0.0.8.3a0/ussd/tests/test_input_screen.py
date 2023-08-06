from ussd.tests import UssdTestCase


class TestInputHandler(UssdTestCase.BaseUssdTestCase):
    validation_error_message = dict(
        enter_height={
            "validators": {
                0: {'text': ['This field is required.']}
            },
            "next_screen": ['This field is required.']
        },
        enter_age={
            "input_identifier": ['This field is required.'],
            "next_screen": ['thank_you_screen is missing in ussd journey'],
            "options": ['Not a valid list.']
        },
        show_information={
            "type": ['Invalid screen type not supported']
        },
        hidden_fields={
            "initial_screen": ["This field is required."]
        },
        invalid_next_screen=dict(
            next_screen={'next_screen': ['This field is required.']}
        )
    )

    def test_showing_screen_content(self):
        ussd_client = self.ussd_client()

        self.assertEqual(
            "Enter your height\n",
            ussd_client.send('')  # dial in
        )

        self.assertEqual(
            "Enter your age\n1. back\n",
            ussd_client.send('5')  # enter height
        )

        # confirm height entered is 5 before going back
        self.assertEqual(
            self.ussd_session(ussd_client.session_id)["height"],
            '5'
        )

        self.assertEqual(
            "Enter your height\n",
            ussd_client.send('1')  # enter one to go back
        )

        ussd_client.send('6')  # enter height

        self.assertEqual(
            "Your age is 24 and your height is 6.\n"
            "Enter anything to go back to the first screen\n",
            ussd_client.send('24')  # enter age
        )

    def test_multilanguage_support(self):
        ussd_client = self.ussd_client(language='sw')

        # Dial in
        response = ussd_client.send('1')

        self.assertEqual(
            "Weka ukubwa lako\n",
            response
        )

        response = ussd_client.send('7')

        self.assertEqual(
            "Weka miaka yako\n1. rudi\n",
            response
        )

        response = ussd_client.send('23')

        self.assertEqual(
            "Miaka yako in 23 na ukubwa wako in 7.\n"
            "Weka kitu ingine yoyote unende "
            "kwenye screen ya kwanza\n",
            response
        )

    def test_input_validation(self):
        ussd_client = self.ussd_client()

        # dial in
        ussd_client.send('')

        # enter invalid height
        response = ussd_client.send('mwas')

        # should get a invalid error message
        self.assertEqual(
            "Enter number between 1 and 7\n",
            response
        )

        # enter valid height
        response = ussd_client.send('6')

        self.assertEqual(
            "Enter your age\n1. back\n",
            response
        )

        # enter invalid age greater thatn 100
        response = ussd_client.send('150')

        self.assertEqual(
            "Number over 100 is not allowed\n",
            response
        )

        # enter a valid age
        response = ussd_client.send('23')

        self.assertEqual(
            "Your age is 23 and your height is 6.\n"
            "Enter anything to go back to the first screen\n",
            response
        )

    def test_next_screen_configuration(self):
        ussd_client = self.ussd_client()
        ussd_client.send('')  # dial in

        self.assertEqual(
            "We are not interested with height above 60",
            ussd_client.send('60')
        )

        ussd_client = self.ussd_client()
        ussd_client.send('')  # dial in

        self.assertEqual(
            "We are not interested with height below 30",
            ussd_client.send('30')
        )
