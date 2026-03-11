"""
Debug utilities placeholder.
"""

def is_debug_enabled():
    return True

def debug(system, msg, **kwargs):
    print(f"[DEBUG][{system}] {msg} {kwargs if kwargs else ''}")

def debug_section(system, title):
    print(f"\n=== {title.upper()} [{system}] ===")

def debug_detailed(system, msg, **kwargs):
    debug(system, f"DETAIL: {msg}", **kwargs)

def debug_success(system, msg, **kwargs):
    print(f"[SUCCESS][{system}] {msg} {kwargs if kwargs else ''}")

def debug_warning(system, msg, **kwargs):
    print(f"[WARNING][{system}] {msg} {kwargs if kwargs else ''}")

def debug_error(system, msg, **kwargs):
    print(f"[ERROR][{system}] {msg} {kwargs if kwargs else ''}")
