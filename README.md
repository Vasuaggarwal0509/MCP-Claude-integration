## MCP and Claude integration

step 1. create folder in vs code

step 2. create venv

step 3. activate venv .ps1

step 4. install dependencies

step 5. make mcp_tools.py file and write starter code

step 6. locate claude folder in your pc using [explorer "$env:APPDATA\Claude"] in powershell

step 7. create a config json file using [code "path_to_folder\claude_desktop_config.json" ]

step 8. write json code (this is configuration file code to be written in claude folder ):

```
{
  "preferences": {
    "menuBarEnabled": false,
    "legacyQuickEntryEnabled": false
  },
  "mcpServers": {
    "simple_math": {
      "command": "D:\\MCP server learning\\venv\\Scripts\\python.exe",
      "args": [
        "D:\\MCP server learning\\mcp_tools.py"
      ]
    }
  }
}
```

step 9. restart claude properly (note: ctrl+ shift + esc  to end task of claude in backcgrund to restart it)

step 10. just write in claude prompt bar directly

example : use simple_math add 5 and 10
here we made a tool simple_math where add is written

Claude Desktop never executes your Python functions directly.

What Claude actually does is:

✔ It launches your Python process
✔ It connects to it through stdin/stdout
✔ It speaks the Model Context Protocol (MCP)
✔ Your Python file only works because it is an MCP server

hence we need mcp server to interact with llm with our personal python code

Here i made multiply in addition tool to verify my custom tool code and it is working fine.


<img width="1919" height="1009" alt="Screenshot 2025-11-19 193458" src="https://github.com/user-attachments/assets/984b16fb-4ece-4f6a-9622-e8cf928bed7f" />
