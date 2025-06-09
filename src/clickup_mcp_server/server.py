import logging
from typing import Dict, List, Optional, Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from enum import Enum
from pydantic import BaseModel, Field
from .client import ClickUpClient
from .markdown_processor import format_description_for_display

# Input Models for ClickUp API Operations

class GetWorkspaces(BaseModel):
    pass

class GetSpaces(BaseModel):
    workspace_id: str = Field(description="ID of the workspace/team")

class CreateSpace(BaseModel):
    workspace_id: str = Field(description="ID of the workspace/team")
    name: str = Field(description="Name of the new space")

class GetLists(BaseModel):
    space_id: str = Field(description="ID of the space")

class CreateList(BaseModel):
    space_id: str = Field(description="ID of the space")
    name: str = Field(description="Name of the new list")
    folder_id: Optional[str] = Field(None, description="ID of the folder (if creating list in a folder)")

class GetTasks(BaseModel):
    list_id: str = Field(description="ID of the list/board")

class GetTasksByStatus(BaseModel):
    list_id: str = Field(description="ID of the list/board")
    status: str = Field(description="Status to filter tasks by")

class CreateTask(BaseModel):
    list_id: str = Field(description="ID of the list/board")
    name: str = Field(description="Name of the task")
    description: Optional[str] = Field(None, description="Task description")
    priority: Optional[int] = Field(None, description="Task priority (1-4)")
    due_date: Optional[int] = Field(None, description="Task due date in milliseconds")
    tags: Optional[List[str]] = Field(None, description="List of tag names to add to task")

class GetTask(BaseModel):
    task_id: str = Field(description="ID of the task")

class UpdateTask(BaseModel):
    task_id: str = Field(description="ID of the task")
    name: Optional[str] = Field(None, description="New task name")
    description: Optional[str] = Field(None, description="New task description")
    priority: Optional[int] = Field(None, description="New task priority (1-4)")
    due_date: Optional[int] = Field(None, description="New due date in milliseconds")
    tags: Optional[List[str]] = Field(None, description="New list of tag names")

class UpdateTaskStatus(BaseModel):
    task_id: str = Field(description="ID of the task")
    status: str = Field(description="New status for the task")

class AssignTask(BaseModel):
    task_id: str = Field(description="ID of the task")
    assignee_ids: List[str] = Field(description="List of user IDs to assign to the task")

class GetTaskSubtasks(BaseModel):
    task_id: str = Field(description="ID of the task")

class DeleteTask(BaseModel):
    task_id: str = Field(description="ID of the task to delete")

class MoveTask(BaseModel):
    task_id: str = Field(description="ID of the task to move")
    list_id: str = Field(description="ID of the destination list/board")

class DuplicateTask(BaseModel):
    task_id: str = Field(description="ID of the task to duplicate")
    list_id: Optional[str] = Field(None, description="ID of the destination list/board (if different from original)")

class CreateSubtask(BaseModel):
    parent_task_id: str = Field(description="ID of the parent task")
    name: str = Field(description="Name of the subtask")
    description: Optional[str] = Field(None, description="Subtask description")
    priority: Optional[int] = Field(None, description="Subtask priority (1-4)")
    due_date: Optional[int] = Field(None, description="Subtask due date in milliseconds")
    tags: Optional[List[str]] = Field(None, description="List of tag names to add to subtask")

class AddComment(BaseModel):
    task_id: str = Field(description="ID of the task")
    comment_text: str = Field(description="Text content of the comment")

class AddAttachment(BaseModel):
    task_id: str = Field(description="ID of the task")
    attachment_url: str = Field(description="URL of the attachment to add")

class BulkUpdateTasks(BaseModel):
    list_id: str = Field(description="ID of the list/board containing the tasks")
    task_ids: List[str] = Field(description="List of task IDs to update")
    name: Optional[str] = Field(None, description="New task name for all tasks")
    description: Optional[str] = Field(None, description="New task description for all tasks")
    status: Optional[str] = Field(None, description="New status for all tasks")
    priority: Optional[int] = Field(None, description="New priority for all tasks (1-4)")
    due_date: Optional[int] = Field(None, description="New due date for all tasks in milliseconds")
    tags: Optional[List[str]] = Field(None, description="New list of tag names for all tasks")

class BulkDeleteTasks(BaseModel):
    task_ids: List[str] = Field(description="List of task IDs to delete")

class GetComments(BaseModel):
    task_id: str = Field(description="ID of the task to get comments for")

# Checklist Models
class CreateChecklist(BaseModel):
    task_id: str = Field(description="ID of the task to add checklist to")
    name: str = Field(description="Name of the checklist")
    
class GetChecklists(BaseModel):
    task_id: str = Field(description="ID of the task to get checklists from")
    
class UpdateChecklist(BaseModel):
    checklist_id: str = Field(description="ID of the checklist to update")
    name: str = Field(description="New name for the checklist")
    
class DeleteChecklist(BaseModel):
    checklist_id: str = Field(description="ID of the checklist to delete")
    
class CreateChecklistItem(BaseModel):
    checklist_id: str = Field(description="ID of the checklist to add the item to")
    name: str = Field(description="Name of the checklist item")
    assignee_id: Optional[str] = Field(None, description="ID of the user to assign the item to")
    
class UpdateChecklistItem(BaseModel):
    checklist_id: str = Field(description="ID of the checklist containing the item")
    checklist_item_id: str = Field(description="ID of the checklist item to update")
    name: Optional[str] = Field(None, description="New name for the checklist item")
    resolved: Optional[bool] = Field(None, description="Whether the item is resolved or not")
    assignee_id: Optional[str] = Field(None, description="ID of the user to assign the item to")
    
class DeleteChecklistItem(BaseModel):
    checklist_id: str = Field(description="ID of the checklist containing the item")
    checklist_item_id: str = Field(description="ID of the checklist item to delete")

class GetFolders(BaseModel):
    space_id: str = Field(description="ID of the space")

class CreateFolder(BaseModel):
    space_id: str = Field(description="ID of the space")
    name: str = Field(description="Name of the new folder")

class UpdateFolder(BaseModel):
    folder_id: str = Field(description="ID of the folder to update")
    name: str = Field(description="New name for the folder")

class DeleteFolder(BaseModel):
    folder_id: str = Field(description="ID of the folder to delete")

class OrganizeLists(BaseModel):
    space_id: str = Field(description="ID of the space")
    folder_id: Optional[str] = Field(None, description="ID of a specific folder (if you only want lists from one folder)")

class GetSpaceHierarchy(BaseModel):
    space_id: str = Field(description="ID of the space")

class NavigateWorkspace(BaseModel):
    path: str = Field(description="Path through the workspace hierarchy in format: team_id/space_name/folder_name/list_name (names or IDs)")

class GetListStatuses(BaseModel):
    list_id: str = Field(description="ID of the list/board")

class GetTasksGroupedByStatus(BaseModel):
    list_id: str = Field(description="ID of the list/board")

# Custom field models
class GetCustomFields(BaseModel):
    list_id: str = Field(description="ID of the list/board to get custom fields for")

class SetCustomFieldValue(BaseModel):
    task_id: str = Field(description="ID of the task to update")
    field_id: str = Field(description="ID of the custom field to update")
    value: Any = Field(description="Value to set for the custom field")

class SetCustomFieldValueByName(BaseModel):
    task_id: str = Field(description="ID of the task to update")
    list_id: str = Field(description="ID of the list (needed to find custom field by name)")
    field_name: str = Field(description="Name of the custom field to update")
    value: Any = Field(description="Value to set for the custom field")

class RemoveCustomFieldValue(BaseModel):
    task_id: str = Field(description="ID of the task")
    field_id: str = Field(description="ID of the custom field to remove value from")

class ClickUpTools(str, Enum):
    GET_WORKSPACES = "get_workspaces"
    GET_SPACES = "get_spaces"
    CREATE_SPACE = "create_space"
    GET_FOLDERS = "get_folders"
    CREATE_FOLDER = "create_folder"
    UPDATE_FOLDER = "update_folder"
    DELETE_FOLDER = "delete_folder"
    ORGANIZE_LISTS = "organize_lists"
    GET_SPACE_HIERARCHY = "get_space_hierarchy"
    NAVIGATE_WORKSPACE = "navigate_workspace"
    GET_LISTS = "get_lists"
    CREATE_LIST = "create_list"
    GET_TASKS = "get_tasks"
    GET_TASKS_BY_STATUS = "get_tasks_by_status"
    GET_LIST_STATUSES = "get_list_statuses"
    GET_TASKS_GROUPED_BY_STATUS = "get_tasks_grouped_by_status"
    CREATE_TASK = "create_task"
    GET_TASK = "get_task"
    UPDATE_TASK = "update_task"
    UPDATE_TASK_STATUS = "update_task_status"
    ASSIGN_TASK = "assign_task"
    GET_TASK_SUBTASKS = "get_task_subtasks"
    DELETE_TASK = "delete_task"
    MOVE_TASK = "move_task"
    DUPLICATE_TASK = "duplicate_task"
    CREATE_SUBTASK = "create_subtask"
    ADD_COMMENT = "add_comment"
    GET_COMMENTS = "get_comments"
    ADD_ATTACHMENT = "add_attachment"
    BULK_UPDATE_TASKS = "bulk_update_tasks"
    BULK_DELETE_TASKS = "bulk_delete_tasks"
    # Checklist tools
    CREATE_CHECKLIST = "create_checklist"
    GET_CHECKLISTS = "get_checklists"
    UPDATE_CHECKLIST = "update_checklist"
    DELETE_CHECKLIST = "delete_checklist"
    CREATE_CHECKLIST_ITEM = "create_checklist_item"
    UPDATE_CHECKLIST_ITEM = "update_checklist_item"
    DELETE_CHECKLIST_ITEM = "delete_checklist_item"
    # Custom field tools
    GET_CUSTOM_FIELDS = "get_custom_fields"
    SET_CUSTOM_FIELD_VALUE = "set_custom_field_value"
    SET_CUSTOM_FIELD_VALUE_BY_NAME = "set_custom_field_value_by_name"
    REMOVE_CUSTOM_FIELD_VALUE = "remove_custom_field_value"

async def serve(api_key: str) -> None:
    """Run the ClickUp MCP server"""
    logger = logging.getLogger(__name__)
    client = ClickUpClient(api_key)
    
    server = Server("mcp-clickup")

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name=ClickUpTools.GET_WORKSPACES,
                description="Get all workspaces/teams",
                inputSchema=GetWorkspaces.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_SPACES,
                description="Get all spaces in a workspace",
                inputSchema=GetSpaces.schema(),
            ),
            Tool(
                name=ClickUpTools.CREATE_SPACE,
                description="Create a new space in a workspace",
                inputSchema=CreateSpace.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_FOLDERS,
                description="Get all folders in a space",
                inputSchema=GetFolders.schema(),
            ),
            Tool(
                name=ClickUpTools.CREATE_FOLDER,
                description="Create a new folder in a space",
                inputSchema=CreateFolder.schema(),
            ),
            Tool(
                name=ClickUpTools.UPDATE_FOLDER,
                description="Update a folder's name",
                inputSchema=UpdateFolder.schema(),
            ),
            Tool(
                name=ClickUpTools.DELETE_FOLDER,
                description="Delete a folder",
                inputSchema=DeleteFolder.schema(),
            ),
            Tool(
                name=ClickUpTools.ORGANIZE_LISTS,
                description="Organize lists by their location (in space or in folders)",
                inputSchema=OrganizeLists.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_SPACE_HIERARCHY,
                description="Get the full hierarchy of a space including folders and lists",
                inputSchema=GetSpaceHierarchy.schema(),
            ),
            Tool(
                name=ClickUpTools.NAVIGATE_WORKSPACE,
                description="Navigate through workspace hierarchy using a path notation (team_id/space_name/folder_name/list_name)",
                inputSchema=NavigateWorkspace.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_LISTS,
                description="Get all lists/boards in a space (including lists in folders)",
                inputSchema=GetLists.schema(),
            ),
            Tool(
                name=ClickUpTools.CREATE_LIST,
                description="Create a new list/board in a space or folder",
                inputSchema=CreateList.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_TASKS,
                description="Get all tasks in a list/board",
                inputSchema=GetTasks.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_TASKS_BY_STATUS,
                description="Get tasks with a specific status in a list/board",
                inputSchema=GetTasksByStatus.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_LIST_STATUSES,
                description="Get all statuses available in a list/board",
                inputSchema=GetListStatuses.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_TASKS_GROUPED_BY_STATUS,
                description="Get all tasks in a list/board grouped by status (including empty statuses)",
                inputSchema=GetTasksGroupedByStatus.schema(),
            ),
            Tool(
                name=ClickUpTools.CREATE_TASK,
                description="Create a new task in a list/board",
                inputSchema=CreateTask.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_TASK,
                description="Get details of a specific task",
                inputSchema=GetTask.schema(),
            ),
            Tool(
                name=ClickUpTools.UPDATE_TASK,
                description="Update a task's properties",
                inputSchema=UpdateTask.schema(),
            ),
            Tool(
                name=ClickUpTools.UPDATE_TASK_STATUS,
                description="Update a task's status",
                inputSchema=UpdateTaskStatus.schema(),
            ),
            Tool(
                name=ClickUpTools.ASSIGN_TASK,
                description="Assign users to a task",
                inputSchema=AssignTask.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_TASK_SUBTASKS,
                description="Get subtasks for a task",
                inputSchema=GetTaskSubtasks.schema(),
            ),
            Tool(
                name=ClickUpTools.DELETE_TASK,
                description="Delete a task",
                inputSchema=DeleteTask.schema(),
            ),
            Tool(
                name=ClickUpTools.MOVE_TASK,
                description="Move a task to a different list/board",
                inputSchema=MoveTask.schema(),
            ),
            Tool(
                name=ClickUpTools.DUPLICATE_TASK,
                description="Duplicate a task, optionally to a different list/board",
                inputSchema=DuplicateTask.schema(),
            ),
            Tool(
                name=ClickUpTools.CREATE_SUBTASK,
                description="Create a subtask for a parent task",
                inputSchema=CreateSubtask.schema(),
            ),
            Tool(
                name=ClickUpTools.ADD_COMMENT,
                description="Add a comment to a task",
                inputSchema=AddComment.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_COMMENTS,
                description="Get all comments for a task",
                inputSchema=GetComments.schema(),
            ),
            Tool(
                name=ClickUpTools.ADD_ATTACHMENT,
                description="Add an attachment to a task by URL",
                inputSchema=AddAttachment.schema(),
            ),
            Tool(
                name=ClickUpTools.BULK_UPDATE_TASKS,
                description="Update multiple tasks in a list at once",
                inputSchema=BulkUpdateTasks.schema(),
            ),
            Tool(
                name=ClickUpTools.BULK_DELETE_TASKS,
                description="Delete multiple tasks at once",
                inputSchema=BulkDeleteTasks.schema(),
            ),
            # Checklist tools
            Tool(
                name=ClickUpTools.CREATE_CHECKLIST,
                description="Create a new checklist in a task",
                inputSchema=CreateChecklist.schema(),
            ),
            Tool(
                name=ClickUpTools.GET_CHECKLISTS,
                description="Get all checklists for a task",
                inputSchema=GetChecklists.schema(),
            ),
            Tool(
                name=ClickUpTools.UPDATE_CHECKLIST,
                description="Update a checklist's name",
                inputSchema=UpdateChecklist.schema(),
            ),
            Tool(
                name=ClickUpTools.DELETE_CHECKLIST,
                description="Delete a checklist",
                inputSchema=DeleteChecklist.schema(),
            ),
            Tool(
                name=ClickUpTools.CREATE_CHECKLIST_ITEM,
                description="Create a new item in a checklist",
                inputSchema=CreateChecklistItem.schema(),
            ),
            Tool(
                name=ClickUpTools.UPDATE_CHECKLIST_ITEM,
                description="Update a checklist item",
                inputSchema=UpdateChecklistItem.schema(),
            ),
            Tool(
                name=ClickUpTools.DELETE_CHECKLIST_ITEM,
                description="Delete a checklist item",
                inputSchema=DeleteChecklistItem.schema(),
            ),
            # Custom field tools
            Tool(
                name=ClickUpTools.GET_CUSTOM_FIELDS,
                description="Get all custom fields for a list/board",
                inputSchema=GetCustomFields.schema(),
            ),
            Tool(
                name=ClickUpTools.SET_CUSTOM_FIELD_VALUE,
                description="Set a custom field value for a task using field ID",
                inputSchema=SetCustomFieldValue.schema(),
            ),
            Tool(
                name=ClickUpTools.SET_CUSTOM_FIELD_VALUE_BY_NAME,
                description="Set a custom field value for a task using field name",
                inputSchema=SetCustomFieldValueByName.schema(),
            ),
            Tool(
                name=ClickUpTools.REMOVE_CUSTOM_FIELD_VALUE,
                description="Remove a custom field value from a task",
                inputSchema=RemoveCustomFieldValue.schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        logger.debug(f"Calling tool: {name} with arguments: {arguments}")
        
        try:
            match name:
                case ClickUpTools.GET_WORKSPACES:
                    workspaces = client.get_workspaces()
                    return [TextContent(
                        type="text",
                        text=f"Workspaces:\n{format_json_list(workspaces)}"
                    )]
                
                case ClickUpTools.GET_SPACES:
                    spaces = client.get_spaces(arguments["workspace_id"])
                    return [TextContent(
                        type="text",
                        text=f"Spaces in workspace {arguments['workspace_id']}:\n{format_json_list(spaces)}"
                    )]
                
                case ClickUpTools.CREATE_SPACE:
                    space = client.create_space(arguments["workspace_id"], arguments["name"])
                    return [TextContent(
                        type="text",
                        text=f"Created space:\n{format_json(space)}"
                    )]
                
                case ClickUpTools.GET_FOLDERS:
                    folders = client.get_folders(arguments["space_id"])
                    return [TextContent(
                        type="text",
                        text=f"Folders in space {arguments['space_id']}:\n{format_json_list(folders)}"
                    )]
                    
                case ClickUpTools.CREATE_FOLDER:
                    folder = client.create_folder(arguments["space_id"], arguments["name"])
                    return [TextContent(
                        type="text",
                        text=f"Created folder in space {arguments['space_id']}:\n{format_json(folder)}"
                    )]
                    
                case ClickUpTools.UPDATE_FOLDER:
                    folder = client.update_folder(arguments["folder_id"], arguments["name"])
                    return [TextContent(
                        type="text",
                        text=f"Updated folder {arguments['folder_id']}:\n{format_json(folder)}"
                    )]
                    
                case ClickUpTools.DELETE_FOLDER:
                    result = client.delete_folder(arguments["folder_id"])
                    return [TextContent(
                        type="text",
                        text=f"Folder {arguments['folder_id']} deleted successfully."
                    )]
                    
                case ClickUpTools.ORGANIZE_LISTS:
                    space_id = arguments["space_id"]
                    folder_id = arguments.get("folder_id")
                    
                    location_info = f"space {space_id}"
                    if folder_id:
                        location_info = f"folder {folder_id} in space {space_id}"
                    
                    organized_lists = client.organize_lists(space_id, folder_id)
                    
                    # Format the organized lists
                    formatted_result = []
                    for location, lists in organized_lists.items():
                        formatted_result.append(f"\n## {location} ({len(lists)} lists)")
                        if lists:
                            for i, list_item in enumerate(lists, 1):
                                name = list_item.get("name", f"List {i}")
                                id_value = list_item.get("id", "unknown")
                                formatted_result.append(f"  {i}. {name} (ID: {id_value})")
                        else:
                            formatted_result.append("  (no lists)")
                    
                    return [TextContent(
                        type="text",
                        text=f"Lists organized in {location_info}:\n{''.join(formatted_result)}"
                    )]
                    
                case ClickUpTools.GET_SPACE_HIERARCHY:
                    hierarchy = client.get_space_hierarchy(arguments["space_id"])
                    
                    # Format the hierarchy
                    result = [f"Hierarchy for space: {hierarchy['name']} (ID: {hierarchy['id']})"]
                    
                    # Format direct lists
                    direct_lists = hierarchy.get("lists", [])
                    result.append(f"\n## Direct Lists ({len(direct_lists)})")
                    if direct_lists:
                        for i, list_item in enumerate(direct_lists, 1):
                            name = list_item.get("name", f"List {i}")
                            id_value = list_item.get("id", "unknown")
                            result.append(f"  {i}. {name} (ID: {id_value})")
                    else:
                        result.append("  (no direct lists)")
                    
                    # Format folders and their lists
                    folders = hierarchy.get("folders", [])
                    result.append(f"\n## Folders ({len(folders)})")
                    
                    if folders:
                        for i, folder in enumerate(folders, 1):
                            folder_name = folder.get("name", f"Folder {i}")
                            folder_id = folder.get("id", "unknown")
                            folder_lists = folder.get("lists", [])
                            
                            result.append(f"  {i}. {folder_name} (ID: {folder_id}) - {len(folder_lists)} lists")
                            
                            if folder_lists:
                                for j, list_item in enumerate(folder_lists, 1):
                                    list_name = list_item.get("name", f"List {j}")
                                    list_id = list_item.get("id", "unknown")
                                    result.append(f"     {j}. {list_name} (ID: {list_id})")
                            else:
                                result.append("     (no lists in this folder)")
                    else:
                        result.append("  (no folders)")
                    
                    return [TextContent(
                        type="text",
                        text="\n".join(result)
                    )]
                    
                case ClickUpTools.NAVIGATE_WORKSPACE:
                    path = arguments["path"]
                    navigation_result = client.navigate_workspace(path)
                    
                    # Format the path
                    path_details = navigation_result.get("path_details", [])
                    formatted_path = []
                    
                    for i, item in enumerate(path_details):
                        item_type = item.get("type", "unknown")
                        item_name = item.get("name", "Unknown")
                        item_id = item.get("id", "unknown")
                        
                        if i == 0:
                            formatted_path.append(f"Workspace: {item_name} (ID: {item_id})")
                        else:
                            indent = "  " * i
                            formatted_path.append(f"{indent}→ {item_type.capitalize()}: {item_name} (ID: {item_id})")
                    
                    # Format the target entity
                    entity = navigation_result.get("entity", {})
                    entity_type = entity.get("type", "unknown").capitalize()
                    entity_name = entity.get("name", "Unknown")
                    entity_id = entity.get("id", "unknown")
                    
                    result = [
                        f"Navigation Result: {entity_type} '{entity_name}' (ID: {entity_id})",
                        "\nPath:",
                        *formatted_path,
                        f"\nFull path: {navigation_result.get('path', 'unknown')}"
                    ]
                    
                    return [TextContent(
                        type="text",
                        text="\n".join(result)
                    )]
                
                case ClickUpTools.GET_LISTS:
                    lists = client.get_lists(arguments["space_id"])
                    return [TextContent(
                        type="text",
                        text=f"Lists in space {arguments['space_id']} (including lists in folders):\n{format_json_list(lists)}"
                    )]
                
                case ClickUpTools.CREATE_LIST:
                    space_id = arguments["space_id"]
                    name = arguments["name"]
                    folder_id = arguments.get("folder_id")
                    list_obj = client.create_list(space_id, name, folder_id)
                    
                    location_info = f"space {space_id}"
                    if folder_id:
                        location_info = f"folder {folder_id} in space {space_id}"
                        
                    return [TextContent(
                        type="text",
                        text=f"Created list in {location_info}:\n{format_json(list_obj)}"
                    )]
                
                case ClickUpTools.GET_TASKS:
                    tasks = client.get_tasks(arguments["list_id"])
                    
                    # Clean up descriptions and text_content in tasks
                    for task in tasks:
                        if "description" in task and task["description"] and ("<" in task["description"] and ">" in task["description"]):
                            task["description"] = format_description_for_display(task["description"])
                        if "text_content" in task and task["text_content"] and ("<" in task["text_content"] and ">" in task["text_content"]):
                            task["text_content"] = "(HTML content - use formatted description field)"
                    
                    return [TextContent(
                        type="text",
                        text=f"Tasks in list {arguments['list_id']}:\n{format_json_list(tasks)}"
                    )]
                
                case ClickUpTools.GET_TASKS_BY_STATUS:
                    tasks = client.get_tasks_by_status(arguments["list_id"], arguments["status"])
                    
                    # Clean up descriptions and text_content in tasks
                    for task in tasks:
                        if "description" in task and task["description"] and ("<" in task["description"] and ">" in task["description"]):
                            task["description"] = format_description_for_display(task["description"])
                        if "text_content" in task and task["text_content"] and ("<" in task["text_content"] and ">" in task["text_content"]):
                            task["text_content"] = "(HTML content - use formatted description field)"
                    
                    return [TextContent(
                        type="text",
                        text=f"Tasks with status '{arguments['status']}' in list {arguments['list_id']}:\n{format_json_list(tasks)}"
                    )]
                    
                case ClickUpTools.GET_LIST_STATUSES:
                    statuses = client.get_list_statuses(arguments["list_id"])
                    return [TextContent(
                        type="text",
                        text=f"Available statuses in list {arguments['list_id']}:\n{format_status_list(statuses)}"
                    )]
                    
                case ClickUpTools.GET_TASKS_GROUPED_BY_STATUS:
                    tasks_by_status = client.get_tasks_grouped_by_status(arguments["list_id"])
                    
                    # Clean up descriptions and text_content in tasks
                    for status, tasks in tasks_by_status.items():
                        for task in tasks:
                            if "description" in task and task["description"] and ("<" in task["description"] and ">" in task["description"]):
                                task["description"] = format_description_for_display(task["description"])
                            if "text_content" in task and task["text_content"] and ("<" in task["text_content"] and ">" in task["text_content"]):
                                task["text_content"] = "(HTML content - use formatted description field)"
                    
                    return [TextContent(
                        type="text",
                        text=format_tasks_by_status(tasks_by_status, arguments["list_id"])
                    )]
                
                case ClickUpTools.CREATE_TASK:
                    # Extract optional parameters
                    list_id = arguments.pop("list_id")
                    name = arguments.pop("name")
                    task = client.create_task(list_id, name, **arguments)
                    return [TextContent(
                        type="text",
                        text=f"Created task:\n{format_json(task)}"
                    )]
                
                case ClickUpTools.GET_TASK:
                    task = client.get_task(arguments["task_id"])
                    
                    # Enhanced handling of HTML content in task fields
                    
                    # Format the description for better readability if it exists
                    if "description" in task and task["description"]:
                        # More robust check for HTML content
                        contains_html = any(tag in task["description"] for tag in [
                            '<h', '<p>', '<div', '<span', '<ul>', '<ol>', '<li>', '<pre>', '<code>', 
                            '<a ', '<b>', '<i>', '<em>', '<strong>', '<table>', '<blockquote>'
                        ])
                        
                        if contains_html:
                            # Convert HTML to markdown for better display
                            task["description"] = format_description_for_display(task["description"])
                            logger.debug(f"Converted HTML description to markdown for task {arguments['task_id']}")
                    
                    # Handle text_content field which typically contains raw HTML
                    if "text_content" in task and task["text_content"]:
                        # If text_content contains HTML but description was empty, use text_content instead
                        if (not task.get("description") and 
                            any(tag in task["text_content"] for tag in ['<h', '<p>', '<div', '<ul>', '<ol>'])):
                            
                            task["description"] = format_description_for_display(task["text_content"])
                            task["text_content"] = "(HTML content - converted to markdown in description field)"
                            logger.debug(f"Used text_content as description for task {arguments['task_id']}")
                        else:
                            # Otherwise just hide the raw HTML
                            task["text_content"] = "(HTML content - use formatted description field)"
                    
                    # Process any custom fields that might contain HTML
                    if "custom_fields" in task and isinstance(task["custom_fields"], list):
                        for field in task["custom_fields"]:
                            if field.get("type") == "text" and field.get("value"):
                                value = field["value"]
                                if isinstance(value, str) and ("<" in value and ">" in value):
                                    field["value"] = format_description_for_display(value)
                    
                    return [TextContent(
                        type="text",
                        text=f"Task details:\n{format_json(task)}"
                    )]
                
                case ClickUpTools.UPDATE_TASK:
                    # Extract task_id and pass the rest as keyword arguments
                    task_id = arguments.pop("task_id")
                    task = client.update_task(task_id, **arguments)
                    return [TextContent(
                        type="text",
                        text=f"Updated task:\n{format_json(task)}"
                    )]
                
                case ClickUpTools.UPDATE_TASK_STATUS:
                    task = client.update_task_status(arguments["task_id"], arguments["status"])
                    return [TextContent(
                        type="text",
                        text=f"Updated task status to '{arguments['status']}':\n{format_json(task)}"
                    )]
                
                case ClickUpTools.ASSIGN_TASK:
                    result = client.assign_task(arguments["task_id"], arguments["assignee_ids"])
                    return [TextContent(
                        type="text",
                        text=f"Assigned users to task:\n{format_json(result)}"
                    )]
                
                case ClickUpTools.GET_TASK_SUBTASKS:
                    task_id = arguments["task_id"]
                    
                    # First get the parent task details for context
                    try:
                        parent_task = client.get_task(task_id)
                        parent_name = parent_task.get("name", "Unknown Task")
                    except Exception as e:
                        logger.warning(f"Error getting parent task details: {e}")
                        parent_name = "Unknown Task"
                    
                    # Get subtasks
                    subtasks = client.get_task_subtasks(task_id)
                    
                    # Format descriptions and text_content in subtasks for better readability
                    for subtask in subtasks:
                        if "description" in subtask and subtask["description"] and ("<" in subtask["description"] and ">" in subtask["description"]):
                            subtask["description"] = format_description_for_display(subtask["description"])
                        if "text_content" in subtask and subtask["text_content"] and ("<" in subtask["text_content"] and ">" in subtask["text_content"]):
                            subtask["text_content"] = "(HTML content - use formatted description field)"
                    
                    # If no subtasks were found
                    if not subtasks:
                        return [TextContent(
                            type="text",
                            text=f"No subtasks found for task '{parent_name}' (ID: {task_id})"
                        )]
                    
                    # Prepare a more detailed response
                    result = [f"Subtasks for task '{parent_name}' (ID: {task_id}):"]
                    
                    for i, subtask in enumerate(subtasks, 1):
                        name = subtask.get("name", f"Subtask {i}")
                        id_value = subtask.get("id", "unknown")
                        
                        # Get status information if available
                        status_info = ""
                        if "status" in subtask:
                            if isinstance(subtask["status"], dict):
                                status_name = subtask["status"].get("status", "Unknown")
                                status_info = f" - Status: {status_name}"
                            elif isinstance(subtask["status"], str):
                                status_info = f" - Status: {subtask['status']}"
                        
                        result.append(f"  {i}. {name} (ID: {id_value}){status_info}")
                    
                    return [TextContent(
                        type="text",
                        text="\n".join(result)
                    )]
                    
                case ClickUpTools.DELETE_TASK:
                    result = client.delete_task(arguments["task_id"])
                    return [TextContent(
                        type="text",
                        text=f"Task {arguments['task_id']} deleted successfully."
                    )]
                    
                case ClickUpTools.MOVE_TASK:
                    result = client.move_task(arguments["task_id"], arguments["list_id"])
                    return [TextContent(
                        type="text",
                        text=f"Task {arguments['task_id']} moved to list {arguments['list_id']}:\n{format_json(result)}"
                    )]
                    
                case ClickUpTools.DUPLICATE_TASK:
                    task_id = arguments["task_id"]
                    list_id = arguments.get("list_id")
                    result = client.duplicate_task(task_id, list_id)
                    
                    location_info = "same list"
                    if list_id:
                        location_info = f"list {list_id}"
                        
                    return [TextContent(
                        type="text",
                        text=f"Task {task_id} duplicated to {location_info}:\n{format_json(result)}"
                    )]
                    
                case ClickUpTools.CREATE_SUBTASK:
                    # Extract required parameters
                    parent_task_id = arguments.pop("parent_task_id")
                    name = arguments.pop("name")
                    # Pass remaining arguments as kwargs
                    result = client.create_subtask(parent_task_id, name, **arguments)
                    return [TextContent(
                        type="text",
                        text=f"Created subtask for task {parent_task_id}:\n{format_json(result)}"
                    )]
                    
                case ClickUpTools.ADD_COMMENT:
                    result = client.add_comment(arguments["task_id"], arguments["comment_text"])
                    return [TextContent(
                        type="text",
                        text=f"Added comment to task {arguments['task_id']}:\n{format_json(result)}"
                    )]
                
                case ClickUpTools.GET_COMMENTS:
                    task_id = arguments.get("task_id", "")
                    comments = []
                    
                    try:
                        # Get comments from the API
                        comments = client.get_comments(task_id)
                        
                        # Format the comments for display as plain text (no HTML/markdown processing)
                        if comments:
                            formatted_comments = []
                            for comment in comments:
                                # Format user name
                                user_name = "Unknown User"
                                if "user" in comment and isinstance(comment["user"], dict):
                                    user = comment["user"]
                                    if "username" in user and user["username"]:
                                        user_name = user["username"]
                                    elif "email" in user and user["email"]:
                                        user_name = user["email"]
                                
                                # Format date
                                date_str = ""
                                if "date" in comment:
                                    try:
                                        date_val = comment["date"]
                                        if isinstance(date_val, int):
                                            from datetime import datetime
                                            date_obj = datetime.fromtimestamp(date_val / 1000.0)
                                            date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                                    except Exception as e:
                                        logger.error(f"Error formatting date: {e}")
                                        
                                # Get comment text as plain text
                                comment_text = comment.get("comment_text", "")
                                
                                # Add formatted comment
                                formatted_comments.append(f"{user_name} ({date_str}):\n{comment_text}")
                            
                            # Join comments with separator
                            comments_text = "\n\n---\n\n".join(formatted_comments)
                            return [TextContent(
                                type="text", 
                                text=f"Comments for task {task_id}:\n\n{comments_text}"
                            )]
                    except Exception as e:
                        logger.error(f"Error getting comments: {e}", exc_info=True)
                    
                    # Fallback response if no comments or error occurred
                    return [TextContent(
                        type="text",
                        text=f"Comments for task {task_id}:\n\nView comments directly in ClickUp: https://app.clickup.com/t/{task_id}\n\nNo comments found or there was an error retrieving comments."
                    )]
                    
                    # Skip the original implementation - UNREACHABLE CODE
                    if False:  # This block will never execute
                        try:
                            # Get the task ID from arguments and validate it
                            task_id = arguments.get("task_id")
                            if not task_id:
                                raise ValueError("Missing required parameter: task_id")
                                
                            logger.debug(f"Fetching comments for task {task_id}")
                            comments = client.get_comments(task_id)
                            
                            # Format the comments for better readability
                            if not comments:
                                logger.debug(f"No comments found for task {task_id}")
                                return [TextContent(
                                    type="text",
                                    text=f"No comments found for task {task_id}"
                                )]
                            
                            logger.debug(f"Found {len(comments)} comments for task {task_id}")
                            result = [f"Comments for task {task_id}:"]
                            
                            for i, comment in enumerate(comments, 1):
                                # Extract comment metadata with safe fallbacks
                                user = comment.get("user", {})
                                user_name = user.get("username", "Unknown")
                                comment_text = comment.get("comment_text", "")
                                
                                # Format the comment_text to convert HTML to readable text
                                # Only process HTML in comment text
                                if comment_text and ("<" in comment_text and ">" in comment_text):
                                    formatted_comment = format_description_for_display(comment_text)
                                else:
                                    formatted_comment = comment_text
                                
                                # Handle date with robust type checking and error handling
                                date = comment.get("date")
                                date_str = None
                                
                                if date is not None:
                                    import datetime
                                    try:
                                        # More detailed handling of different date types
                                        if isinstance(date, (int, float)):
                                            # Already numeric, use directly
                                            timestamp_ms = date
                                        elif isinstance(date, str) and date.strip():
                                            # Try to convert string to int
                                            try:
                                                timestamp_ms = int(date.strip())
                                            except ValueError:
                                                # If it's not a simple numeric string, log warning
                                                logger.warning(f"Invalid date format for comment {i}: {date}")
                                                timestamp_ms = None
                                        else:
                                            # For other types or empty strings, log and skip
                                            logger.warning(f"Unsupported date type for comment {i}: {type(date)}")
                                            timestamp_ms = None
                                        
                                        # Convert timestamp to formatted date string if valid
                                        if timestamp_ms is not None:
                                            # Ensure timestamp_ms is treated as an integer or float
                                            try:
                                                timestamp_ms_float = float(timestamp_ms)
                                                date_str = datetime.datetime.fromtimestamp(timestamp_ms_float/1000).strftime('%Y-%m-%d %H:%M:%S')
                                            except (ValueError, TypeError) as e:
                                                logger.warning(f"Could not convert timestamp {timestamp_ms} to float: {e}")
                                                timestamp_ms = None
                                    except Exception as e:
                                        # Detailed error logging
                                        logger.error(f"Error formatting date for comment {i}: {e}, date value: {date}, type: {type(date)}")
                                
                                # Append comment header with date if available
                                if date_str:
                                    result.append(f"\n## Comment {i} by {user_name} on {date_str}")
                                else:
                                    result.append(f"\n## Comment {i} by {user_name}")
                                
                                # Append the formatted comment text
                                result.append(formatted_comment)
                            
                            # Return the formatted comments
                            return [TextContent(
                                type="text",
                                text="\n".join(result)
                            )]
                        
                        except Exception as e:
                            # Comprehensive error handling
                            logger.error(f"Error processing GET_COMMENTS: {str(e)}", exc_info=True)
                            return [TextContent(
                                type="text",
                                text=f"Error retrieving comments: {str(e)}"
                            )]
                    
                case ClickUpTools.ADD_ATTACHMENT:
                    result = client.add_attachment(arguments["task_id"], arguments["attachment_url"])
                    return [TextContent(
                        type="text",
                        text=f"Added attachment to task {arguments['task_id']}:\n{format_json(result)}"
                    )]
                    
                case ClickUpTools.BULK_UPDATE_TASKS:
                    # Extract required parameters
                    list_id = arguments.pop("list_id")
                    task_ids = arguments.pop("task_ids")
                    # Pass remaining arguments as kwargs
                    result = client.bulk_update_tasks(list_id, task_ids, **arguments)
                    return [TextContent(
                        type="text",
                        text=f"Bulk updated {len(task_ids)} tasks in list {list_id}:\n{format_json(result)}"
                    )]
                    
                case ClickUpTools.BULK_DELETE_TASKS:
                    result = client.bulk_delete_tasks(arguments["task_ids"])
                    return [TextContent(
                        type="text",
                        text=f"Bulk deleted {len(arguments['task_ids'])} tasks:\n{format_json(result)}"
                    )]
                    
                # Checklist operations
                case ClickUpTools.CREATE_CHECKLIST:
                    result = client.create_checklist(arguments["task_id"], arguments["name"])
                    return [TextContent(
                        type="text",
                        text=f"Created checklist in task {arguments['task_id']}:\n{format_json(result)}"
                    )]
                    
                case ClickUpTools.GET_CHECKLISTS:
                    checklists = client.get_checklists(arguments["task_id"])
                    if not checklists:
                        return [TextContent(
                            type="text",
                            text=f"No checklists found for task {arguments['task_id']}"
                        )]
                    
                    result = [f"Checklists for task {arguments['task_id']}:"]
                    for i, checklist in enumerate(checklists, 1):
                        checklist_name = checklist.get("name", f"Checklist {i}")
                        checklist_id = checklist.get("id", "unknown")
                        result.append(f"\n## {i}. {checklist_name} (ID: {checklist_id})")
                        
                        # Format items in the checklist
                        items = checklist.get("items", [])
                        if items:
                            for j, item in enumerate(items, 1):
                                item_name = item.get("name", f"Item {j}")
                                item_id = item.get("id", "unknown")
                                resolved = "✓" if item.get("resolved") else "□"
                                result.append(f"   {j}. {resolved} {item_name} (ID: {item_id})")
                        else:
                            result.append("   (no items)")
                    
                    return [TextContent(
                        type="text",
                        text="\n".join(result)
                    )]
                    
                case ClickUpTools.UPDATE_CHECKLIST:
                    result = client.update_checklist(arguments["checklist_id"], arguments["name"])
                    return [TextContent(
                        type="text",
                        text=f"Updated checklist {arguments['checklist_id']}:\n{format_json(result)}"
                    )]
                    
                case ClickUpTools.DELETE_CHECKLIST:
                    result = client.delete_checklist(arguments["checklist_id"])
                    return [TextContent(
                        type="text",
                        text=f"Deleted checklist {arguments['checklist_id']} successfully."
                    )]
                    
                case ClickUpTools.CREATE_CHECKLIST_ITEM:
                    checklist_id = arguments["checklist_id"]
                    name = arguments["name"]
                    assignee_id = arguments.get("assignee_id")
                    
                    result = client.create_checklist_item(checklist_id, name, assignee_id)
                    return [TextContent(
                        type="text",
                        text=f"Created item in checklist {checklist_id}:\n{format_json(result)}"
                    )]
                    
                case ClickUpTools.UPDATE_CHECKLIST_ITEM:
                    checklist_id = arguments["checklist_id"]
                    checklist_item_id = arguments["checklist_item_id"]
                    name = arguments.get("name")
                    resolved = arguments.get("resolved")
                    assignee_id = arguments.get("assignee_id")
                    
                    result = client.update_checklist_item(
                        checklist_id, 
                        checklist_item_id, 
                        name, 
                        resolved, 
                        assignee_id
                    )
                    
                    return [TextContent(
                        type="text",
                        text=f"Updated item {checklist_item_id} in checklist {checklist_id}:\n{format_json(result)}"
                    )]
                    
                case ClickUpTools.DELETE_CHECKLIST_ITEM:
                    checklist_id = arguments["checklist_id"]
                    checklist_item_id = arguments["checklist_item_id"]
                    
                    result = client.delete_checklist_item(checklist_id, checklist_item_id)
                    return [TextContent(
                        type="text",
                        text=f"Deleted item {checklist_item_id} from checklist {checklist_id} successfully."
                    )]
                
                # Custom field operations
                case ClickUpTools.GET_CUSTOM_FIELDS:
                    list_id = arguments["list_id"]
                    fields = client.get_custom_fields(list_id)
                    
                    if not fields:
                        return [TextContent(
                            type="text",
                            text=f"No custom fields found for list {list_id}"
                        )]
                    
                    result = [f"Custom fields for list {list_id}:"]
                    for i, field in enumerate(fields, 1):
                        field_name = field.get("name", f"Field {i}")
                        field_id = field.get("id", "unknown")
                        field_type = field.get("type", "unknown")
                        
                        # Get type config info if available
                        type_config = field.get("type_config", {})
                        type_info = ""
                        if field_type == "drop_down" and "options" in type_config:
                            options = [opt.get("name", "Unknown") for opt in type_config.get("options", [])]
                            type_info = f" (options: {', '.join(options[:3])}" + ("..." if len(options) > 3 else "") + ")"
                        elif field_type == "url":
                            type_info = " (URL field)"
                        elif field_type == "text":
                            type_info = " (text field)"
                        elif field_type == "number":
                            type_info = " (number field)"
                        elif field_type == "date":
                            type_info = " (date field)"
                        
                        result.append(f"  {i}. {field_name} (ID: {field_id}, Type: {field_type}{type_info})")
                    
                    return [TextContent(
                        type="text",
                        text="\n".join(result)
                    )]
                
                case ClickUpTools.SET_CUSTOM_FIELD_VALUE:
                    task_id = arguments["task_id"]
                    field_id = arguments["field_id"]
                    value = arguments["value"]
                    
                    result = client.set_custom_field_value(task_id, field_id, value)
                    return [TextContent(
                        type="text",
                        text=f"Set custom field {field_id} to '{value}' for task {task_id}"
                    )]
                
                case ClickUpTools.SET_CUSTOM_FIELD_VALUE_BY_NAME:
                    task_id = arguments["task_id"]
                    list_id = arguments["list_id"]
                    field_name = arguments["field_name"]
                    value = arguments["value"]
                    
                    # Find the custom field by name
                    field = client.find_custom_field_by_name(list_id, field_name)
                    if not field:
                        return [TextContent(
                            type="text",
                            text=f"Custom field '{field_name}' not found in list {list_id}"
                        )]
                    
                    field_id = field.get("id")
                    result = client.set_custom_field_value(task_id, field_id, value)
                    
                    return [TextContent(
                        type="text",
                        text=f"Set custom field '{field_name}' (ID: {field_id}) to '{value}' for task {task_id}"
                    )]
                
                case ClickUpTools.REMOVE_CUSTOM_FIELD_VALUE:
                    task_id = arguments["task_id"]
                    field_id = arguments["field_id"]
                    
                    result = client.remove_custom_field_value(task_id, field_id)
                    return [TextContent(
                        type="text",
                        text=f"Removed custom field {field_id} value from task {task_id}"
                    )]
                
                case _:
                    raise ValueError(f"Unknown tool: {name}")
        
        except Exception as e:
            logger.error(f"Error calling tool {name}: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

def format_json(obj: Dict) -> str:
    """Format a dictionary in a friendly way for display"""
    if not obj:
        return "No data"
    
    lines = []
    
    # Process important fields first for better readability
    priority_fields = ["id", "name", "description", "status", "date_created", "date_updated"]
    
    # First add priority fields in a specific order
    for key in priority_fields:
        if key in obj:
            value = obj[key]
            if key == "description" or key == "text_content":
                # For description and text_content, add the entire content with indentation
                if value:
                    value_lines = value.split('\n')
                    value_str = "\n    " + "\n    ".join(value_lines)
                else:
                    value_str = "(empty)"
            elif isinstance(value, dict):
                if key == "status":
                    # Special handling for status object
                    status_name = value.get("status", "Unknown")
                    status_color = value.get("color", "unknown")
                    value_str = f"{status_name} (color: {status_color})"
                else:
                    value_str = "{...}"  # Simplified display for other nested objects
            elif isinstance(value, list):
                value_str = f"[{len(value)} items]"
            else:
                value_str = str(value)
            lines.append(f"  {key}: {value_str}")
    
    # Then add remaining fields
    for key, value in obj.items():
        if key not in priority_fields:
            if isinstance(value, dict):
                value_str = "{...}"  # Simplified display for nested objects
            elif isinstance(value, list):
                value_str = f"[{len(value)} items]"
            else:
                value_str = str(value)
            lines.append(f"  {key}: {value_str}")
    
    return "\n".join(lines)

def format_json_list(items: List[Dict]) -> str:
    """Format a list of dictionaries in a friendly way for display"""
    if not items:
        return "No items found"
    
    result = []
    for i, item in enumerate(items, 1):
        name = item.get("name", f"Item {i}")
        id_value = item.get("id", "unknown")
        
        # For lists that are in folders, show folder information
        if "folder_name" in item and "folder_id" in item:
            result.append(f"{i}. {name} (ID: {id_value}) - in folder: {item['folder_name']} (ID: {item['folder_id']})")
        else:
            result.append(f"{i}. {name} (ID: {id_value})")
    
    return "\n".join(result)

def format_status_list(statuses: List[Dict]) -> str:
    """Format a list of statuses for display"""
    if not statuses:
        return "No statuses found"
    
    result = []
    for i, status in enumerate(statuses, 1):
        status_name = status.get("status", f"Status {i}")
        status_id = status.get("id", "unknown")
        status_color = status.get("color", "unknown")
        order_index = status.get("orderindex", "unknown")
        
        result.append(f"{i}. {status_name} (ID: {status_id}, Color: {status_color}, Order: {order_index})")
    
    return "\n".join(result)

def format_tasks_by_status(tasks_by_status: Dict[str, List[Dict]], list_id: str) -> str:
    """Format tasks grouped by status for display"""
    result = [f"Tasks in list {list_id} grouped by status:"]
    
    for status, tasks in tasks_by_status.items():
        task_count = len(tasks)
        status_line = f"\n## {status} ({task_count} tasks)"
        result.append(status_line)
        
        if tasks:
            for i, task in enumerate(tasks, 1):
                name = task.get("name", f"Task {i}")
                id_value = task.get("id", "unknown")
                result.append(f"  {i}. {name} (ID: {id_value})")
        else:
            result.append("  (empty)")
    
    return "\n".join(result)