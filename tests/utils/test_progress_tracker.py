import unittest
from unittest.mock import patch, mock_open
from src.utils.progress_tracker import ProgressTracker


class TestProgressTracker(unittest.TestCase):

    def setUp(self):
        """Set up for each test."""
        self.test_file = "test_tracker.csv"
        # Mock os.path.exists to control file existence
        self.patcher_exists = patch("os.path.exists")
        self.mock_exists = self.patcher_exists.start()
        # Mock os.makedirs
        self.patcher_makedirs = patch("os.makedirs")
        self.mock_makedirs = self.patcher_makedirs.start()
        # Mock open
        self.patcher_open = patch("builtins.open", mock_open())
        self.mock_file = self.patcher_open.start()

    def tearDown(self):
        """Clean up after each test."""
        self.patcher_exists.stop()
        self.patcher_makedirs.stop()
        self.patcher_open.stop()

    def test_initialization_creates_file(self):
        """Test that the tracker creates a new file with a header."""
        self.mock_exists.return_value = False
        ProgressTracker(self.test_file)

        self.mock_exists.assert_called_with(self.test_file)
        self.mock_makedirs.assert_called_once()
        self.mock_file.assert_called_with(self.test_file, "w", newline="")

        # Check that the header was written
        handle = self.mock_file()
        handle.write.assert_called_once()
        # The call is to a DictWriter, so we check the first arg
        self.assertIn("timestamp", handle.write.call_args[0][0])

    def test_load_progress(self):
        """Test loading data from an existing CSV."""
        self.mock_exists.return_value = True
        csv_data = (
            "timestamp,parameters_json,total_profiles,is_workable,status,"
            "last_completed_page\n"
            '2025-01-01T12:00:00,{"country": "UK"},100,True,COMPLETED,1'
        )
        self.patcher_open.stop()  # Stop the generic mock
        m_open = mock_open(read_data=csv_data)
        self.patcher_open = patch("builtins.open", m_open)
        self.patcher_open.start()

        tracker = ProgressTracker(self.test_file)
        tracker.load_progress()

        self.assertEqual(len(tracker.progress_data), 1)
        self.assertIn('{"country": "UK"}', tracker.progress_data)
        self.assertEqual(
            tracker.progress_data['{"country": "UK"}']["status"], "COMPLETED"
        )

    def test_log_check_and_get_progress(self):
        """Test logging a new check and retrieving it."""
        self.mock_exists.return_value = True
        tracker = ProgressTracker(self.test_file)
        params = {"countries": "UK", "seniority": "Director"}

        tracker.log_check(params, 500, True)

        progress = tracker.get_progress(params)
        self.assertIsNotNone(progress)
        self.assertEqual(progress["total_profiles"], 500)
        self.assertEqual(progress["is_workable"], True)
        self.assertEqual(progress["status"], "PENDING")

    def test_update_and_mark_status(self):
        """Test updating a record's status and page progress."""
        self.mock_exists.return_value = True
        tracker = ProgressTracker(self.test_file)
        params = {"countries": "UK"}

        # Initial log
        tracker.log_check(params, 150, True)

        # Update progress
        tracker.update_page_progress(params, 1)
        progress = tracker.get_progress(params)
        self.assertEqual(progress["last_completed_page"], 1)
        self.assertEqual(progress["status"], "IN_PROGRESS")

        # Mark as completed
        tracker.mark_completed(params)
        progress = tracker.get_progress(params)
        self.assertEqual(progress["status"], "COMPLETED")

        # Mark as failed
        tracker.mark_failed(params)
        progress = tracker.get_progress(params)
        self.assertEqual(progress["status"], "FAILED")


if __name__ == "__main__":
    unittest.main()
