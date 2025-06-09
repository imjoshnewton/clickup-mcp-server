import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from clickup_mcp_server.server import serve, ClickUpTools

# Mock ClickUpClient class
@pytest.fixture
def mock_client():
    with patch("clickup_mcp_server.server.ClickUpClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        yield mock_client

# Mock Server class
@pytest.fixture
def mock_server():
    with patch("clickup_mcp_server.server.Server") as mock_server_cls:
        mock_server = MagicMock()
        mock_server.list_tools = MagicMock(return_value=lambda: [])
        mock_server.call_tool = MagicMock(return_value=lambda name, arguments: [])
        mock_server.create_initialization_options.return_value = {}
        mock_server.run = AsyncMock()
        mock_server_cls.return_value = mock_server
        yield mock_server

# Mock stdio_server context manager
@pytest.fixture
def mock_stdio():
    with patch("clickup_mcp_server.server.stdio_server") as mock_stdio:
        mock_read_stream = AsyncMock()
        mock_write_stream = AsyncMock()
        mock_stdio.return_value.__aenter__.return_value = (mock_read_stream, mock_write_stream)
        mock_stdio.return_value.__aexit__.return_value = None
        yield mock_stdio

class TestServer:
    @pytest.mark.asyncio
    async def test_serve_initializes_server(self, mock_client, mock_server, mock_stdio):
        """Test that serve initializes the server with the correct name"""
        # Call serve
        await serve("test_api_key")
        
        # Check that Server was initialized with correct name
        from clickup_mcp_server.server import Server
        Server.assert_called_once_with("mcp-clickup")
    
    @pytest.mark.asyncio
    async def test_list_tools_returns_all_tools(self, mock_client, mock_server, mock_stdio):
        """Test that list_tools returns all expected tools"""
        # Extract the list_tools decorator to get the actual function
        server_instance = mock_server
        list_tools_decorator = server_instance.list_tools
        
        # Call serve to register the tools
        with patch("clickup_mcp_server.server.list_tools", new_callable=AsyncMock) as mock_list_tools:
            # Capture the decorated function
            def capture_decorator(func):
                mock_list_tools.original_func = func
                return mock_list_tools
            
            server_instance.list_tools.side_effect = capture_decorator
            
            await serve("test_api_key")
            
            # Now we can access the original function and call it
            list_tools_func = server_instance.list_tools.call_args[0][0]
            tools = await list_tools_func()
            
            # Verify all tools are registered
            tool_names = [tool.name for tool in tools]
            assert set(tool_names) == set(t.value for t in ClickUpTools)
    
    @pytest.mark.asyncio
    async def test_call_tool_get_workspaces(self, mock_client, mock_server, mock_stdio):
        """Test that call_tool correctly handles get_workspaces"""
        # Setup mock response from client
        mock_client.get_workspaces.return_value = [
            {"id": "team_123", "name": "Workspace 1"}
        ]
        
        # Call serve to register the tools
        with patch("clickup_mcp_server.server.call_tool", new_callable=AsyncMock) as mock_call_tool:
            # Capture the decorated function
            def capture_decorator(func):
                mock_call_tool.original_func = func
                return mock_call_tool
            
            mock_server.call_tool.side_effect = capture_decorator
            
            await serve("test_api_key")
            
            # Now we can access the original function and call it
            call_tool_func = mock_server.call_tool.call_args[0][0]
            result = await call_tool_func(ClickUpTools.GET_WORKSPACES, {})
            
            # Verify result
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Workspace 1" in result[0].text
            assert "team_123" in result[0].text
            
            # Verify client method was called
            mock_client.get_workspaces.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_call_tool_create_task(self, mock_client, mock_server, mock_stdio):
        """Test that call_tool correctly handles create_task"""
        # Setup mock response from client
        mock_client.create_task.return_value = {
            "id": "task_123", 
            "name": "Test Task",
            "description": "Task description"
        }
        
        # Call serve to register the tools
        with patch("clickup_mcp_server.server.call_tool", new_callable=AsyncMock) as mock_call_tool:
            # Capture the decorated function
            def capture_decorator(func):
                mock_call_tool.original_func = func
                return mock_call_tool
            
            mock_server.call_tool.side_effect = capture_decorator
            
            await serve("test_api_key")
            
            # Now we can access the original function and call it
            call_tool_func = mock_server.call_tool.call_args[0][0]
            result = await call_tool_func(
                ClickUpTools.CREATE_TASK, 
                {
                    "list_id": "list_123", 
                    "name": "Test Task", 
                    "description": "Task description"
                }
            )
            
            # Verify result
            assert len(result) == 1
            assert result[0].type == "text"
            assert "Test Task" in result[0].text
            assert "task_123" in result[0].text
            
            # Verify client method was called with correct arguments
            mock_client.create_task.assert_called_once_with(
                "list_123", 
                "Test Task", 
                description="Task description"
            )