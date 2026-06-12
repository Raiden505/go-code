import subprocess
import json
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
client = TavilyClient(os.getenv("TAVILY_API_KEY"))


#Tool schemas
TOOL_SCHEMAS = [
    #Read
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "reads contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "file path to read"
                    }
                },
                "required": ["path"],
                "additionalProperties": False
            }
        }
    },

    #Write
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "creates or overwrites content to file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "file path to write to"
                    },
                    "content": {
                        "type": "string",
                        "description": "content to write to file"
                    }
                },
                "required": ["path", "content"],
                "additionalProperties": False
            }
        }
    },

    #Edit
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "finds and replaces text",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "file path to edit at"
                    },
                    "find": {
                        "type": "string",
                        "description": "content in the file to look for, must match exactly including indentation"
                    },
                    "replace_content": {
                        "type": "string",
                        "description": "content to write to file"
                    }
                },
                "required": ["path", "find", "replace_content"],
                "additionalProperties": False
            }
        }
    },

    #Shell_commands
    {
        "type": "function",
        "function": {
            "name": "shell_command",
            "description": "executes shell commands in a terminal or shell",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "exact shell command to be ran on the computer's terminal/shell"
                    }
                },
                "required": ["command"],
                "additionalProperties": False
            }
        }
    },

    #Web search
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "searches the live internet for accurate up-to-date information, documentation, code examples or news",
            "parameters": {
                "type": "object",
                "properties": {
                    "searchQuery": {
                        "type": "string",
                        "description": "Search query to be searched for"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "The number of search results to return",
                        "default": 5
                    }
                },
                "required": ["searchQuery"],
                "additionalProperties": False
            }
        }
    },

    #List directory
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Lists contents of the directory specified",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory file path"
                    }
                },
                "required": ["directory"],
                "additionalProperties": False
            }
        }
    }
]


#Tool implementation

#read file
def read_file(path: str) -> dict[str, any]:
    """Read a file and return its contents"""
    try:
        with open(path, 'r') as f:
            content = f.read()
        return {
            "success": True,
            "content": content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
#write to file
def write_file(path: str, content: str) -> dict[str, any]:
    """Create and write, or overwrite a file"""
    try:
        with open(path, 'w') as f:
            f.write(content)
        return {
            "success": True,
            "message": "Sucessfully written"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
#edit file
def edit_file(path: str, find: str, replace_content: str) -> dict[str, any]:
    try:
        with open(path, 'r') as f:
            file_content = f.read()
        
        if find not in file_content:
            return {
                "success": False,
                "error": f"Could not find exact text block in {path}. Make sure argument matches the files indentation and spacing perfectly"
            }
        
        updated_content = file_content.replace(find, replace_content)
        with open(path, 'w') as f:
            f.write(updated_content)

        return {
            "success": True,
            "message": "Successfully edited"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"failed to edit file: {str(e)}"
        }

#shell command
def shell_command(command: str) -> dict[str, any]:
    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text = True)
    stdout, stderr = pipe.communicate()
    exit_code = pipe.returncode
    if exit_code != 0:
        return {
            "success": False,
            "output": stdout,
            "diagnostic": stderr,
        }
    else:
        return {
            "success": True,
            "output": stdout,
            "diagnostic": stderr
        }

#web_search
def web_search(searchQuery: str, num_results: int) -> dict[str, any]:
    response = client.search(
        query=searchQuery,
        search_depth="advanced",
        max_results=num_results
    )
    return response

def list_directory(directory: str) -> dict[str, any]:
    try:
        list = os.listdir(directory)
        return {
            "success": True,
            "list": list
        }
    except OSError as error:
        return {
            "success": False,
            "error": error.strerror
        }
    
available_function = {
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "shell_command": shell_command,
    "web_search": web_search,
    "list_directory": list_directory
}

def execute_tool_call(tool_call):
    function_name = tool_call.function.name
    try:
        function_to_call = available_function[function_name]
    except Exception as e:
        return {
            "success": False,
            "error": "Requested tool " + function_name + " doesn't exist in the tool definitions. Refer to tools schema" 
        }
    function_args = json.loads(tool_call.function.arguments)

    return function_to_call(**function_args)