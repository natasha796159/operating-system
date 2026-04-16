import psutil

SAFE_PROCESSES = [
    "chrome.exe",
    "msedge.exe",
    "code.exe",
    "explorer.exe",
    "python.exe"
]

CRITICAL_PIDS = [0, 4]

MODES = ["OFF", "SUGGEST", "AUTO"]

def detect_issue(cpu, memory_available_mb):
    if cpu > 85:
        return "high_cpu"
    elif memory_available_mb < 500:
        return "low_memory"
    return None

def get_target_processes(processes):
    return sorted(processes, key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)

def safe_kill(proc):
    name = proc.get('name', '').lower()
    pid = proc.get('pid', -1)
    
    # Do not kill if it's safe listed
    if name in SAFE_PROCESSES or any(safe in name for safe in SAFE_PROCESSES):
        return False
    
    if pid in CRITICAL_PIDS:
        return False
        
    # Avoid generic System processes
    if 'idle' in name or 'system' in name:
        return False
        
    return True

def auto_fix(mode, processes, cpu, memory_available_bytes):
    if mode == "OFF":
        return ["Auto Fix is OFF. No actions taken."]
        
    actions = []
    memory_available_mb = memory_available_bytes / (1024 * 1024)
    
    issue = detect_issue(cpu, memory_available_mb)

    if not issue:
        return ["System is stable - No action needed"]

    top_procs = get_target_processes(processes)

    killed_count = 0
    for proc in top_procs:
        if killed_count >= 2: # Max 2 processes per iteration
            break
            
        if not safe_kill(proc):
            continue

        cpu_used = proc.get('cpu_percent', 0)
        mem_used = proc.get('memory_percent', 0)
        
        # Only take action against processes actually consuming resources
        if cpu_used < 5 and mem_used < 5:
            continue

        msg = f"{proc.get('name')} (PID {proc.get('pid')}) consuming resources"

        if mode == "SUGGEST":
            actions.append(f"Suggested closing {msg}")
            killed_count += 1
        elif mode == "AUTO":
            try:
                p = psutil.Process(proc['pid'])
                p.terminate()
                actions.append(f"Killed {msg}")
                killed_count += 1
            except Exception:
                actions.append(f"Failed to close {msg}")

    if not actions:
        actions.append("No safe optimizations available right now")

    return actions
