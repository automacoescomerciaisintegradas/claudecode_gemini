"""
Claude Agent SDK Mock Client
"""
class ClaudeSDKClient:
    async def query(self, message): pass
    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass
