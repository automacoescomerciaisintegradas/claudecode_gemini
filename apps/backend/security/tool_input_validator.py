"""
Tool input validator for security.
"""
def get_safe_tool_input(block):
    if hasattr(block, 'input') and isinstance(block.input, dict):
        return block.input
    return {}
