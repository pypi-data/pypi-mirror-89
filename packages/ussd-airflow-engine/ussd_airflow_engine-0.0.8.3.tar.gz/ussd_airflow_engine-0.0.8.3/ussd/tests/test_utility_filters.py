from ussd.tests import UssdTestCase


class TestScreensUsingFilters(UssdTestCase.BaseUssdTestCase):
    validate_ussd = False

    def get_ussd_client(self):
        return self.ussd_client(
            generate_customer_journey=False,
            extra_payload={
                "journey_name": "sample_journey",
                "journey_version": "sample_using_utility_filters"
            }
        )

    def test_using_filters(self):
        client = self.get_ussd_client()
        # dial in
        response = client.send('')

        self.assertEqual(
            "Formatting numbers 1,000.00 and currency conversation "
            "Ksh 1,000.00\n", response)
