"""
Client factory for LLM providers.
"""
def create_client(project_dir, spec_dir, model, **kwargs):
    class MockClient:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
    return MockClient()
