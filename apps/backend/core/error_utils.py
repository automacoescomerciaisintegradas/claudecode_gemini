"""
Error utilities for Claude Agent SDK.
"""
def is_authentication_error(e): return "authentication" in str(e).lower()
def is_rate_limit_error(e): return "rate limit" in str(e).lower()
def is_tool_concurrency_error(e): return "400" in str(e) and "tool" in str(e).lower()

async def safe_receive_messages(client, caller="session"):
    # Mock stream for now
    if False: yield None
