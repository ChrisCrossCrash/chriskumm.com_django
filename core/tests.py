from rest_framework.test import APITestCase
from rest_framework import status


class SubmitInquiryAPITestCase(APITestCase):
    def test_valid_form_returns_201(self):
        response = self.client.post(
            '/api/submit-inquiry/',
            {
                'name': 'Chris Kumm',
                'email': 'ck@aol.com',
                'message': 'Hi!'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_blank_name_returns_400(self):
        response = self.client.post(
            '/api/submit-inquiry/',
            {
                'name': '',
                'email': 'ck@aol.com',
                'message': 'Hi!'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blank_email_returns_400(self):
        response = self.client.post(
            '/api/submit-inquiry/',
            {
                'name': 'Chris Kumm',
                'email': '',
                'message': 'Hi!'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blank_message_returns_400(self):
        response = self.client.post(
            '/api/submit-inquiry/',
            {
                'name': 'Chris Kumm',
                'email': 'ck@aol.com',
                'message': ''
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_returns_400(self):
        response = self.client.post(
            '/api/submit-inquiry/',
            {
                'name': 'Chris Kumm',
                'email': 'ck@aol',
                'message': 'Hi!'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_null_field_returns_400(self):
        response = self.client.post(
            '/api/submit-inquiry/',
            {
                # 'name': 'Chris Kumm',
                'email': 'ck@aol',
                'message': 'Hi!'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
