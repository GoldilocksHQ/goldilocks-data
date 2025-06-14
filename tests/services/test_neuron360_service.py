import unittest
from unittest.mock import patch, MagicMock
import requests
from src.services.neuron360_service import Neuron360Service
from src.config.api_config import API_CONFIG


class TestNeuron360Service(unittest.TestCase):

    def setUp(self):
        """Set up for each test."""
        self.service = Neuron360Service()
        self.test_url = f"{API_CONFIG['base_url']}/v1/profile_search"
        self.test_payload = {"test": "data"}

    @patch("requests.post")
    def test_search_profiles_success(self, mock_post):
        """Test a single successful API call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        response = self.service.search_profiles(self.test_payload)

        mock_post.assert_called_once_with(
            self.test_url, json=self.test_payload, headers=API_CONFIG["headers"]
        )
        self.assertEqual(response, {"success": True})

    @patch("requests.post")
    def test_search_profiles_client_error_no_retry(self, mock_post):
        """Test that a 4xx client error is not retried."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Client Error"
        )
        mock_post.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.service.search_profiles(self.test_payload)

        mock_post.assert_called_once()  # Should only be called once

    @patch("time.sleep", return_value=None)  # Mock time.sleep to speed up test
    @patch("requests.post")
    def test_search_profiles_server_error_retry_and_fail(self, mock_post, mock_sleep):
        """Test that a 5xx server error is retried 3 times and then fails."""
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "Server Error"
        )
        mock_post.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.service.search_profiles(self.test_payload)

        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)  # Sleeps between retries
        mock_sleep.assert_any_call(2)
        mock_sleep.assert_any_call(4)

    @patch("time.sleep", return_value=None)
    @patch("requests.post")
    def test_search_profiles_retry_and_succeed(self, mock_post, mock_sleep):
        """Test a 5xx error that succeeds on the second attempt."""
        # First response is a server error
        mock_failure_response = MagicMock()
        mock_failure_response.status_code = 503

        # Second response is a success
        mock_success_response = MagicMock()
        mock_success_response.status_code = 200
        mock_success_response.json.return_value = {"success": True}

        # requests.post will return the failure, then the success
        mock_post.side_effect = [mock_failure_response, mock_success_response]

        response = self.service.search_profiles(self.test_payload)

        self.assertEqual(mock_post.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)
        self.assertEqual(response, {"success": True})


if __name__ == "__main__":
    unittest.main()
