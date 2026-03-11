"""
Graphiti configuration placeholder.
"""

def is_graphiti_enabled():
    return False

def get_graphiti_status():
    return {
        "enabled": False,
        "available": False,
        "reason": "Not configured",
        "host": "localhost",
        "port": 5000,
        "database": "graphiti",
        "llm_provider": "openai",
        "embedder_provider": "openai"
    }
