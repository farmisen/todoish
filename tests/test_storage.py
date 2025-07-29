"""Unit tests for the storage module."""

import json
from pathlib import Path
from unittest.mock import mock_open, patch


from src.storage import load_tasks, save_tasks


class TestLoadTasks:
    """Test cases for the load_tasks function."""

    def test_load_tasks_with_existing_file(self):
        """Test loading tasks from an existing JSON file."""
        mock_tasks = [
            {"id": 1, "description": "Test task 1", "status": "pending"},
            {"id": 2, "description": "Test task 2", "status": "completed"},
        ]
        mock_file_content = json.dumps(mock_tasks)

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = load_tasks()

        assert result == mock_tasks
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["status"] == "completed"

    def test_load_tasks_with_empty_file(self):
        """Test loading tasks from an empty JSON file."""
        mock_file_content = "[]"

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = load_tasks()

        assert result == []
        assert isinstance(result, list)

    def test_load_tasks_file_not_found(self):
        """Test that load_tasks returns empty list when file doesn't exist."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_tasks()

        assert result == []
        assert isinstance(result, list)

    def test_load_tasks_uses_correct_file_path(self):
        """Test that load_tasks opens the correct file."""
        mock_file_content = "[]"
        mock_open_func = mock_open(read_data=mock_file_content)

        with patch("builtins.open", mock_open_func):
            load_tasks()

        mock_open_func.assert_called_once_with(
            Path("tasks.json"), "r", encoding="utf-8"
        )


class TestSaveTasks:
    """Test cases for the save_tasks function."""

    def test_save_tasks_basic(self):
        """Test saving a list of tasks to file."""
        tasks = [
            {"id": 1, "description": "Task 1", "status": "pending"},
            {"id": 2, "description": "Task 2", "status": "completed"},
        ]

        mock_open_func = mock_open()
        with patch("builtins.open", mock_open_func):
            save_tasks(tasks)

        mock_open_func.assert_called_once_with(
            Path("tasks.json"), "w", encoding="utf-8"
        )

        # Get the write calls
        handle = mock_open_func()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        written_data = json.loads(written_content)

        assert written_data == tasks

    def test_save_tasks_empty_list(self):
        """Test saving an empty task list."""
        tasks = []

        mock_open_func = mock_open()
        with patch("builtins.open", mock_open_func):
            save_tasks(tasks)

        handle = mock_open_func()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        written_data = json.loads(written_content)

        assert written_data == []

    def test_save_tasks_overwrites_existing_file(self):
        """Test that save_tasks overwrites the entire file."""
        new_tasks = [{"id": 3, "description": "New task", "status": "pending"}]

        mock_open_func = mock_open()
        with patch("builtins.open", mock_open_func):
            save_tasks(new_tasks)

        # Verify file was opened in write mode (which overwrites)
        mock_open_func.assert_called_once_with(
            Path("tasks.json"), "w", encoding="utf-8"
        )

    def test_save_tasks_unicode_support(self):
        """Test saving tasks with unicode characters."""
        tasks = [
            {"id": 1, "description": "Test émojis 🎉 and 中文", "status": "pending"}
        ]

        mock_open_func = mock_open()
        with patch("builtins.open", mock_open_func):
            save_tasks(tasks)

        handle = mock_open_func()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        written_data = json.loads(written_content)

        assert written_data[0]["description"] == "Test émojis 🎉 and 中文"

    def test_save_tasks_formatting(self):
        """Test that saved JSON is properly formatted with indentation."""
        tasks = [{"id": 1, "description": "Task", "status": "pending"}]

        mock_open_func = mock_open()
        with patch("builtins.open", mock_open_func):
            save_tasks(tasks)

        handle = mock_open_func()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        # Check that the output includes indentation (pretty printed)
        assert "  " in written_content  # JSON should be indented
        assert (
            "[\n" in written_content or "[\r\n" in written_content
        )  # Should have newlines
