from agent_tools import *
from langgraph.func import entrypoint

tools = [analyze_linter_output]
model_with_tools = model.bind_tools(tools)

def syntax_agent(linter_json: dict):
    return analyze_linter_output.run(linter_json)

# Wrap as entrypoint properly
syntax_agent_entry = entrypoint()(syntax_agent)