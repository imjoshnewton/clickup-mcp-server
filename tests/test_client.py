import pytest
from unittest.mock import patch, MagicMock, call
from clickup_mcp_server.client import ClickUpClient
import requests

class TestClickUpClient:
    @pytest.fixture
    def client(self):
        return ClickUpClient("test_api_key")
    
    @patch("requests.request")
    def test_get_workspaces(self, mock_request, client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"teams": [{"id": "123", "name": "Test Workspace"}]}
        mock_request.return_value = mock_response
        
        # Call method
        result = client.get_workspaces()
        
        # Verify results
        assert len(result) == 1
        assert result[0]["id"] == "123"
        assert result[0]["name"] == "Test Workspace"
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.clickup.com/api/v2/team",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json=None
        )
    
    @patch("requests.request")
    def test_get_tasks(self, mock_request, client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"tasks": [{"id": "abc123", "name": "Test Task"}]}
        mock_request.return_value = mock_response
        
        # Call method
        result = client.get_tasks("list123")
        
        # Verify results
        assert len(result) == 1
        assert result[0]["id"] == "abc123"
        assert result[0]["name"] == "Test Task"
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.clickup.com/api/v2/list/list123/task",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json=None
        )
    
    @patch("requests.request")
    def test_create_task(self, mock_request, client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "task123", "name": "New Task"}
        mock_request.return_value = mock_response
        
        # Call method
        result = client.create_task("list123", "New Task", description="Task description")
        
        # Verify results
        assert result["id"] == "task123"
        assert result["name"] == "New Task"
        
        # Verify request was made correctly - account for markdown conversion
        mock_request.assert_called_once_with(
            method="POST",
            url="https://api.clickup.com/api/v2/list/list123/task",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json={"name": "New Task", "description": "<p>Task description</p>", "markdown_content": "Task description"}
        )
    
    @patch("requests.request")
    def test_update_task_status(self, mock_request, client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "task123", "status": {"status": "In Progress"}}
        mock_request.return_value = mock_response
        
        # Call method
        result = client.update_task_status("task123", "In Progress")
        
        # Verify results
        assert result["id"] == "task123"
        assert result["status"]["status"] == "In Progress"
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="PUT",
            url="https://api.clickup.com/api/v2/task/task123",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json={"status": "In Progress"}
        )
    
    @patch("requests.request")
    def test_request_error_handling(self, mock_request, client):
        # Setup mock to raise an exception
        mock_error_response = MagicMock()
        mock_error_response.text = "API Error"
        
        mock_exception = requests.exceptions.HTTPError()
        mock_exception.response = mock_error_response
        
        mock_request.side_effect = mock_exception
        
        # Call method and check for exception
        with pytest.raises(requests.exceptions.HTTPError):
            client.get_workspaces()
    
    # Checklist tests
    
    @patch("requests.request")
    def test_create_checklist(self, mock_request, client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "checklist123", "name": "Test Checklist", "task_id": "task123"}
        mock_request.return_value = mock_response
        
        # Call method
        result = client.create_checklist("task123", "Test Checklist")
        
        # Verify results
        assert result["id"] == "checklist123"
        assert result["name"] == "Test Checklist"
        assert result["task_id"] == "task123"
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="POST",
            url="https://api.clickup.com/api/v2/task/task123/checklist",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json={"name": "Test Checklist"}
        )
    
    @patch("requests.request")
    def test_get_checklists(self, mock_request, client):
        # Setup mock responses for get_task which is called by get_checklists
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "task123",
            "name": "Test Task",
            "checklists": [
                {
                    "id": "checklist123",
                    "name": "Test Checklist",
                    "items": [
                        {"id": "item1", "name": "Item 1", "resolved": False},
                        {"id": "item2", "name": "Item 2", "resolved": True}
                    ]
                }
            ]
        }
        mock_request.return_value = mock_response
        
        # Call method
        result = client.get_checklists("task123")
        
        # Verify results
        assert len(result) == 1
        assert result[0]["id"] == "checklist123"
        assert result[0]["name"] == "Test Checklist"
        assert len(result[0]["items"]) == 2
        assert result[0]["items"][0]["name"] == "Item 1"
        assert result[0]["items"][0]["resolved"] is False
        assert result[0]["items"][1]["name"] == "Item 2"
        assert result[0]["items"][1]["resolved"] is True
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.clickup.com/api/v2/task/task123",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json=None
        )
    
    @patch("requests.request")
    def test_update_checklist(self, mock_request, client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "checklist123", "name": "Updated Checklist"}
        mock_request.return_value = mock_response
        
        # Call method
        result = client.update_checklist("checklist123", "Updated Checklist")
        
        # Verify results
        assert result["id"] == "checklist123"
        assert result["name"] == "Updated Checklist"
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="PUT",
            url="https://api.clickup.com/api/v2/checklist/checklist123",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json={"name": "Updated Checklist"}
        )
    
    @patch("requests.request")
    def test_create_checklist_item(self, mock_request, client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "item123", 
            "name": "Test Item", 
            "resolved": False,
            "checklist_id": "checklist123"
        }
        mock_request.return_value = mock_response
        
        # Call method
        result = client.create_checklist_item("checklist123", "Test Item", "user123")
        
        # Verify results
        assert result["id"] == "item123"
        assert result["name"] == "Test Item"
        assert result["resolved"] is False
        assert result["checklist_id"] == "checklist123"
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="POST",
            url="https://api.clickup.com/api/v2/checklist/checklist123/checklist_item",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json={"name": "Test Item", "assignee": "user123"}
        )
    
    @patch("requests.request")
    def test_update_checklist_item(self, mock_request, client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "item123", 
            "name": "Updated Item", 
            "resolved": True,
            "checklist_id": "checklist123"
        }
        mock_request.return_value = mock_response
        
        # Call method
        result = client.update_checklist_item(
            "checklist123", "item123", "Updated Item", True, "user123"
        )
        
        # Verify results
        assert result["id"] == "item123"
        assert result["name"] == "Updated Item"
        assert result["resolved"] is True
        assert result["checklist_id"] == "checklist123"
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="PUT",
            url="https://api.clickup.com/api/v2/checklist/checklist123/checklist_item/item123",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json={"name": "Updated Item", "resolved": True, "assignee": "user123"}
        )
    
    @patch("requests.request")
    def test_delete_checklist_item(self, mock_request, client):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "item123", "deleted": True}
        mock_request.return_value = mock_response
        
        # Call method
        result = client.delete_checklist_item("checklist123", "item123")
        
        # Verify results
        assert result["id"] == "item123"
        assert result["deleted"] is True
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="DELETE",
            url="https://api.clickup.com/api/v2/checklist/checklist123/checklist_item/item123",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params=None,
            json=None
        )
        
    @patch("requests.request")
    def test_get_task_subtasks(self, mock_request, client):
        # Test case 1: When API returns subtasks directly (primary method)
        
        # Setup mock response with direct subtasks
        direct_subtasks_response = MagicMock()
        direct_subtasks_response.json.return_value = {
            "id": "task123",
            "name": "Parent Task",
            "list": {"id": "list123", "name": "Test List"},
            "subtasks": [
                {"id": "subtask1", "name": "Subtask 1", "status": {"status": "To Do"}, "orderindex": 1},
                {"id": "subtask2", "name": "Subtask 2", "status": {"status": "In Progress"}, "orderindex": 2}
            ]
        }
        
        # Configure mock
        mock_request.return_value = direct_subtasks_response
        
        # Call method
        result = client.get_task_subtasks("task123")
        
        # Verify results
        assert len(result) == 2
        assert result[0]["id"] == "subtask1"
        assert result[0]["name"] == "Subtask 1"
        assert result[0]["status"]["status"] == "To Do"
        assert result[1]["id"] == "subtask2"
        assert result[1]["name"] == "Subtask 2"
        assert result[1]["status"]["status"] == "In Progress"
        
        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method="GET",
            url="https://api.clickup.com/api/v2/task/task123",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params={"subtasks": True, "include_subtasks": True},
            json=None
        )
        
        # Test case 2: Fallback method when API doesn't return subtasks directly
        mock_request.reset_mock()
        
        # First request - get parent task without subtasks field
        parent_task_response = MagicMock()
        parent_task_response.json.return_value = {
            "id": "task123",
            "name": "Parent Task",
            "list": {"id": "list123", "name": "Test List"}
        }
        
        # Second request - get tasks from the list
        list_tasks_response = MagicMock()
        list_tasks_response.json.return_value = {
            "tasks": [
                {"id": "subtask1", "name": "Subtask 1", "status": {"status": "To Do"}, "parent": "task123", "orderindex": 1},
                {"id": "subtask2", "name": "Subtask 2", "status": {"status": "In Progress"}, "parent": "task123", "orderindex": 2},
                {"id": "other_task", "name": "Other Task", "status": {"status": "Open"}, "parent": None}
            ]
        }
        
        # Configure mock to return different responses for different requests
        mock_request.side_effect = [parent_task_response, list_tasks_response]
        
        # Call method
        result = client.get_task_subtasks("task123")
        
        # Verify results
        assert len(result) == 2
        assert result[0]["id"] == "subtask1"
        assert result[0]["name"] == "Subtask 1"
        assert result[0]["status"]["status"] == "To Do"
        assert result[1]["id"] == "subtask2"
        assert result[1]["name"] == "Subtask 2"
        assert result[1]["status"]["status"] == "In Progress"
        
        # Verify requests were made correctly
        assert mock_request.call_count == 2
        
        # First call - get the parent task details with subtasks params
        assert mock_request.call_args_list[0] == call(
            method="GET",
            url="https://api.clickup.com/api/v2/task/task123",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params={"subtasks": True, "include_subtasks": True},
            json=None
        )
        
        # Second call - get all tasks in the list with subtasks param (updated implementation)
        assert mock_request.call_args_list[1] == call(
            method="GET",
            url="https://api.clickup.com/api/v2/list/list123/task",
            headers={"Authorization": "test_api_key", "Content-Type": "application/json"},
            params={"subtasks": True},
            json=None
        )