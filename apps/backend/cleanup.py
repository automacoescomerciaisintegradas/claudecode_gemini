import os
import shutil

files = ["base.py", "coder.py", "planner.py", "session.py", "memory_manager.py"]
for f in files:
    path = os.path.join(r"d:\claudecode_gemini\apps\backend", f)
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"Deleted {f}")
        except Exception as e:
            print(f"Failed to delete {f}: {e}")

utils_dir = r"d:\claudecode_gemini\apps\backend\utils"
if os.path.exists(utils_dir):
    try:
        shutil.rmtree(utils_dir)
        print("Deleted utils directory")
    except Exception as e:
        print(f"Failed to delete utils: {e}")
