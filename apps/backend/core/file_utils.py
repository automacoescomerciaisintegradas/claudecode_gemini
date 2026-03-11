"""
File utilities.
"""
import json
import os
import tempfile

def write_json_atomic(path, data):
    fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(path))
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)
