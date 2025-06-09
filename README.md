# clickup-mcp-server: A ClickUp MCP Server

## Overview

A Model Context Protocol server for ClickUp API interaction and automation. This server provides tools for AI systems to read, create, and update tasks, lists, and spaces in ClickUp.

This MCP server enables AI tools like Claude to interact with your ClickUp workspace, helping automate task management, project planning, and other workflows.

## Features

This MCP server provides comprehensive integration with ClickUp, offering the following capabilities:

### Task Management
- Create, update, and delete tasks
- Move and duplicate tasks between lists and boards
- Set task properties including due dates, priorities, and tags
- Create, view, and manage subtasks
- Add comments and attachments to tasks
- Support for both single and bulk task operations
- Task grouping and filtering by status

### Workspace Organization
- Navigate and manage workspaces, spaces, folders, and lists
- Create, update, and delete spaces and folders
- Organize lists within spaces and folders
- View comprehensive workspace hierarchy
- Navigate efficiently through workspace using path notation
- Create lists in spaces or inside folders

### Formatting and Display
- Full markdown support for task descriptions and comments
- HTML conversion for proper rendering in ClickUp
- Formatted display of task details, lists, and hierarchies
- Enhanced display of complex project structures

### Developer Experience
- Comprehensive error handling and validation
- Clear, consistent API responses
- Detailed documentation for all tools
- Easy integration with Claude and other AI systems

## Tools

The server provides the following tools for interacting with ClickUp:

### Workspace/Team Tools

1. `get_workspaces`
   - Gets all workspaces/teams
   - Input: None
   - Returns: List of workspaces with IDs and names

2. `navigate_workspace`
   - Navigates through workspace hierarchy using path notation
   - Input:
     - `path` (string): Path through workspace hierarchy (team_id/space_name/folder_name/list_name)
   - Returns: Details of the target entity and its full path

### Space Tools

3. `get_spaces`
   - Gets all spaces in a workspace
   - Input:
     - `workspace_id` (string): ID of the workspace/team
   - Returns: List of spaces with IDs and names

4. `create_space`
   - Creates a new space in a workspace
   - Inputs:
     - `workspace_id` (string): ID of the workspace/team
     - `name` (string): Name of the new space
   - Returns: Details of the created space

5. `get_space_hierarchy`
   - Gets the full hierarchy of a space including folders and lists
   - Input:
     - `space_id` (string): ID of the space
   - Returns: Complete hierarchical structure of the space

### Folder Tools

6. `get_folders`
   - Gets all folders in a space
   - Input:
     - `space_id` (string): ID of the space
   - Returns: List of folders with IDs and names

7. `create_folder`
   - Creates a new folder in a space
   - Inputs:
     - `space_id` (string): ID of the space
     - `name` (string): Name of the new folder
   - Returns: Details of the created folder

8. `update_folder`
   - Updates a folder's name
   - Inputs:
     - `folder_id` (string): ID of the folder to update
     - `name` (string): New name for the folder
   - Returns: Updated folder details

9. `delete_folder`
   - Deletes a folder
   - Input:
     - `folder_id` (string): ID of the folder to delete
   - Returns: Confirmation of deletion

### List/Board Tools

10. `get_lists`
    - Gets all lists/boards in a space
    - Input:
      - `space_id` (string): ID of the space
    - Returns: List of lists/boards with IDs and names

11. `create_list`
    - Creates a new list/board in a space or folder
    - Inputs:
      - `space_id` (string): ID of the space
      - `name` (string): Name of the new list/board
      - `folder_id` (string, optional): ID of the folder (if creating list in a folder)
    - Returns: Details of the created list/board

12. `organize_lists`
    - Organizes lists by their location (in space or in folders)
    - Inputs:
      - `space_id` (string): ID of the space
      - `folder_id` (string, optional): ID of a specific folder
    - Returns: Lists organized by their containing folder

### Task Tools

13. `get_tasks`
   - Gets all tasks in a list/board
   - Input:
     - `list_id` (string): ID of the list/board
   - Returns: List of tasks with IDs, names, and other details

14. `get_tasks_by_status`
    - Gets tasks with a specific status in a list/board
    - Inputs:
      - `list_id` (string): ID of the list/board
      - `status` (string): Status to filter tasks by
    - Returns: List of tasks with the specified status

15. `create_task`
    - Creates a new task in a list/board
    - Inputs:
      - `list_id` (string): ID of the list/board
      - `name` (string): Name of the task
      - `description` (string, optional): Task description
      - `priority` (number, optional): Task priority (1-4)
      - `due_date` (number, optional): Task due date in milliseconds
      - `tags` (string[], optional): List of tag names to add to task
    - Returns: Details of the created task

16. `get_task`
    - Gets details of a specific task
    - Input:
      - `task_id` (string): ID of the task
    - Returns: Full details of the task including description, status, etc.

17. `update_task`
    - Updates a task's properties
    - Inputs:
      - `task_id` (string): ID of the task
      - `name` (string, optional): New task name
      - `description` (string, optional): New task description
      - `priority` (number, optional): New task priority (1-4)
      - `due_date` (number, optional): New due date in milliseconds
      - `tags` (string[], optional): New list of tag names
    - Returns: Updated task details

18. `update_task_status`
    - Updates a task's status
    - Inputs:
      - `task_id` (string): ID of the task
      - `status` (string): New status for the task
    - Returns: Updated task details

19. `assign_task`
    - Assigns users to a task
    - Inputs:
      - `task_id` (string): ID of the task
      - `assignee_ids` (string[]): List of user IDs to assign to the task
    - Returns: Confirmation of assignment

20. `get_task_subtasks`
    - Gets subtasks for a task
    - Input:
      - `task_id` (string): ID of the task
    - Returns: List of subtasks with their details

21. `delete_task`
    - Deletes a task
    - Input:
      - `task_id` (string): ID of the task to delete
    - Returns: Confirmation of deletion

22. `move_task`
    - Moves a task to a different list/board
    - Inputs:
      - `task_id` (string): ID of the task to move
      - `list_id` (string): ID of the destination list/board
    - Returns: Updated task details

23. `duplicate_task`
    - Duplicates a task, optionally to a different list/board
    - Inputs:
      - `task_id` (string): ID of the task to duplicate
      - `list_id` (string, optional): ID of the destination list/board
    - Returns: Details of the duplicated task

24. `create_subtask`
    - Creates a subtask for a parent task
    - Inputs:
      - `parent_task_id` (string): ID of the parent task
      - `name` (string): Name of the subtask
      - `description` (string, optional): Subtask description
      - `priority` (number, optional): Subtask priority (1-4)
      - `due_date` (number, optional): Subtask due date in milliseconds
      - `tags` (string[], optional): List of tag names for the subtask
    - Returns: Details of the created subtask

25. `add_comment`
    - Adds a comment to a task
    - Inputs:
      - `task_id` (string): ID of the task
      - `comment_text` (string): Text content of the comment
    - Returns: Details of the added comment

26. `add_attachment`
    - Adds an attachment to a task by URL
    - Inputs:
      - `task_id` (string): ID of the task
      - `attachment_url` (string): URL of the attachment to add
    - Returns: Details of the added attachment

27. `bulk_update_tasks`
    - Updates multiple tasks in a list at once
    - Inputs:
      - `list_id` (string): ID of the list/board containing the tasks
      - `task_ids` (string[]): List of task IDs to update
      - `name` (string, optional): New task name for all tasks
      - `description` (string, optional): New task description for all tasks
      - `status` (string, optional): New status for all tasks
      - `priority` (number, optional): New priority for all tasks (1-4)
      - `due_date` (number, optional): New due date for all tasks in milliseconds
      - `tags` (string[], optional): New list of tag names for all tasks
    - Returns: Confirmation of bulk update

28. `bulk_delete_tasks`
    - Deletes multiple tasks at once
    - Input:
      - `task_ids` (string[]): List of task IDs to delete
    - Returns: Confirmation of bulk deletion

### Custom Field Tools

29. `get_custom_fields`
    - Gets all custom fields for a list/board
    - Input:
      - `list_id` (string): ID of the list/board
    - Returns: List of custom fields with their IDs, names, types, and configuration

30. `set_custom_field_value`
    - Sets a custom field value for a task using field ID
    - Inputs:
      - `task_id` (string): ID of the task
      - `field_id` (string): ID of the custom field
      - `value` (any): Value to set for the custom field
    - Returns: Confirmation of custom field update

31. `set_custom_field_value_by_name`
    - Sets a custom field value for a task using field name
    - Inputs:
      - `task_id` (string): ID of the task
      - `list_id` (string): ID of the list (needed to find custom field by name)
      - `field_name` (string): Name of the custom field
      - `value` (any): Value to set for the custom field
    - Returns: Confirmation of custom field update

32. `remove_custom_field_value`
    - Removes a custom field value from a task
    - Inputs:
      - `task_id` (string): ID of the task
      - `field_id` (string): ID of the custom field
    - Returns: Confirmation of custom field removal

## Installation

### Prerequisites

- Python 3.10 or higher
- A ClickUp account with an API key

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *clickup-mcp-server*.

```
uv --directory "/path/to/clickup-mcp-server" run clickup-mcp-server --api-key YOUR_API_KEY
```

Or use a .env file (see Configuration section).

### Using PIP

Alternatively, you can install `clickup-mcp-server` via pip:

```
pip install clickup-mcp-server
```

After installation, you can run it as a script using:

```
python -m clickup_mcp_server --api-key YOUR_API_KEY
```

## Configuration

### API Key

You need a ClickUp API key to use this server. You can get one from [ClickUp API Settings](https://app.clickup.com/settings/apps).

The API key can be provided in two ways:

1. Command-line argument: `--api-key YOUR_API_KEY`
2. Environment variable in a `.env` file:
   ```
   CLICKUP_API_KEY=your_api_key_here
   ```

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "clickup": {
    "command": "uvx",
    "args": ["clickup-mcp-server", "--api-key", "YOUR_API_KEY"]
  }
}
```
</details>

<details>
<summary>Using docker</summary>

```json
"mcpServers": {
  "clickup": {
    "command": "docker",
    "args": ["run", "--rm", "-i", "-e", "CLICKUP_API_KEY=YOUR_API_KEY", "mcp/clickup"]
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "clickup": {
    "command": "python",
    "args": ["-m", "clickup_mcp_server", "--api-key", "YOUR_API_KEY"]
  }
}
```
</details>

### Usage with VS Code

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `Preferences: Open Settings (JSON)`.

Optionally, you can add it to a file called `.vscode/mcp.json` in your workspace. This will allow you to share the configuration with others. 

> Note that the `mcp` key is not needed in the `.vscode/mcp.json` file.

```json
{
  "mcp": {
    "servers": {
      "clickup": {
        "command": "uvx",
        "args": ["clickup-mcp-server"],
        "env": {
          "CLICKUP_API_KEY": "YOUR_API_KEY"
        }
      }
    }
  }
}
```

For Docker installation:

```json
{
  "mcp": {
    "servers": {
      "clickup": {
        "command": "docker",
        "args": [
          "run",
          "--rm",
          "-i",
          "-e", "CLICKUP_API_KEY=YOUR_API_KEY",
          "mcp/clickup"
        ]
      }
    }
  }
}
```

### Usage with [Zed](https://github.com/zed-industries/zed)

Add to your Zed settings.json:

<details>
<summary>Using uvx</summary>

```json
"context_servers": [
  "mcp-server-clickup": {
    "command": {
      "path": "uvx",
      "args": ["clickup-mcp-server"]
    },
    "env": {
      "CLICKUP_API_KEY": "YOUR_API_KEY"
    }
  }
],
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"context_servers": {
  "mcp-server-clickup": {
    "command": {
      "path": "python",
      "args": ["-m", "clickup_mcp_server"]
    },
    "env": {
      "CLICKUP_API_KEY": "YOUR_API_KEY"
    }
  }
},
```
</details>

## Example Usage Scenarios

### Task Management with Claude

Claude can help you manage your ClickUp tasks:

1. **Creating a Task Plan**:
   Ask Claude to create a plan based on a specific task in ClickUp. Claude will:
   - Find the task by name or ID
   - Analyze its description and subtasks
   - Generate a structured plan for completing the task

2. **Task Automation**:
   For a task containing code-related instructions, Claude can:
   - Get the task details from ClickUp
   - Update the task status to "In Progress"
   - Implement the code according to the task requirements
   - Check off subtasks as they're completed
   - Update the status to "Ready for Review" when finished

3. **Task Reporting**:
   Ask Claude to generate summaries of tasks with specific statuses:
   - Get all tasks marked "In Progress"
   - Compile a status report with completion estimates
   - Create new tasks for blockers or dependencies

4. **Custom Field Management**:
   Claude can work with custom fields to enhance your workflow:
   - List all custom fields in a project to see available metadata
   - Set custom field values like "GitHub Pull Request URL" when creating PRs
   - Update project tracking fields like "Sprint", "Story Points", or "Priority"
   - Example: "Create a PR for this branch and add the GitHub URL to the 'GitHub Pull Request URL' custom field in the related ClickUp task"

## Debugging

Run your server with the `-v` or `-vv` flag for increased verbosity:

```
uvx clickup-mcp-server -vv
```

You can use the MCP inspector to debug the server:

```
npx @modelcontextprotocol/inspector uvx clickup-mcp-server
```

## Development

### Setting Up Development Environment

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/clickup-mcp-server.git
   cd clickup-mcp-server
   ```

2. Install development dependencies:
   ```
   uv pip install -e ".[dev]"
   ```

3. Run tests:
   ```
   pytest
   ```

### Docker Build

Build the Docker image:

```bash
docker build -t mcp/clickup .
```

## Implementation Status

This MCP server implements the majority of essential ClickUp features. Below is a detailed breakdown of implemented features and those planned for future implementation.

### Task Management ✅
All core task management features have been implemented:

| Feature | Status | Description |
|---------|--------|-------------|
| Create tasks | ✅ | Create new tasks in any list or board |
| Update tasks | ✅ | Modify task properties including name, description, and more |
| Delete tasks | ✅ | Remove tasks from ClickUp |
| Move tasks | ✅ | Relocate tasks between different lists and boards |
| Duplicate tasks | ✅ | Create copies of tasks, optionally in different locations |
| Set dates | ✅ | Set start and due dates for tasks |
| View subtasks | ✅ | Retrieve subtasks for any parent task |
| Create subtasks | ✅ | Add subtasks to existing tasks |
| Manage subtasks | ✅ | Update and delete subtasks |
| Add comments | ✅ | Add comments to tasks with markdown support |
| Add attachments | ✅ | Attach files via URL to tasks |
| Single operations | ✅ | Perform actions on individual tasks |
| Bulk operations | ✅ | Perform actions on multiple tasks simultaneously |

### Workspace Organization ✅
All workspace organization features have been implemented:

| Feature | Status | Description |
|---------|--------|-------------|
| Navigate spaces | ✅ | Browse and select spaces in workspaces |
| Navigate folders | ✅ | Browse and select folders within spaces |
| Navigate lists | ✅ | Browse and select lists in spaces or folders |
| Create spaces | ✅ | Create new spaces in workspaces |
| Create lists | ✅ | Create new lists in spaces or folders |
| Create folders | ✅ | Create new folders within spaces |
| Organize lists | ✅ | Group and organize lists by location |
| Lists in folders | ✅ | Create and manage lists inside folders |
| View hierarchy | ✅ | See the complete workspace structure |
| Path navigation | ✅ | Navigate efficiently using path notation |

### Miscellaneous Features 🔧
Some advanced features are implemented, with others planned for future releases:

| Feature | Status | Description |
|---------|--------|-------------|
| Global lookups | 🔄 | Find items by name or ID across workspaces *(planned)* |
| Case-insensitive | 🔄 | Match names regardless of capitalization *(planned)* |
| Basic markdown | ✅ | Support for basic markdown in descriptions |
| Enhanced markdown | ✅ | Advanced markdown with proper rendering in ClickUp |
| Rate limiting | 🔄 | Built-in handling of API rate limits *(planned)* |
| Error handling | ✅ | Comprehensive error detection and reporting |
| Input validation | ✅ | Validation of all inputs before API submission |
| API coverage | 🔄 | Support for additional ClickUp API features *(in progress)* |

**Legend:**
- ✅ Implemented
- 🔄 Planned or in progress

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
EOF < /dev/null