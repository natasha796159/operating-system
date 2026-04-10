import psutil

# Cache active process classes to correctly calculate CPU time diffs iteratively
process_cache = {}

def get_all_processes():
    global process_cache
    processes = []
    core_count = psutil.cpu_count() or 1
    
    current_pids = set()
    
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            
            # Explicitly exclude System Idle Process and PID 0 (Windows)
            if pid == 0 or (name and 'idle' in name.lower()):
                continue
                
            current_pids.add(pid)
                
            if pid not in process_cache:
                process_cache[pid] = proc
                proc.cpu_percent(interval=None) # Warmup call
                cpu_percent = 0.0
            else:
                try:
                    cpu_percent = process_cache[pid].cpu_percent(interval=None)
                except psutil.NoSuchProcess:
                    # Clean up if process died between iter and here
                    continue
                    
            # Normalize multi-core CPU usage (so it caps at 100%)
            normalized_cpu = cpu_percent / core_count
            
            pinfo = proc.info
            pinfo['cpu_percent'] = round(normalized_cpu, 1)
            
            if pinfo['memory_percent'] is not None:
                pinfo['memory_percent'] = round(pinfo['memory_percent'], 1)
            
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Evict dead processes from the cache (memory alignment)
    cached_pids = list(process_cache.keys())
    for pid in cached_pids:
        if pid not in current_pids:
            del process_cache[pid]
            
    # Sort processes by CPU usage descending by default
    processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
    return processes

def kill_process(pid):
    # Security: Prevent killing critical system processes (e.g. System Idle, System)
    if pid <= 4:
        return {"success": False, "error": "Action blocked: Cannot kill critical system process."}
    
    try:
        p = psutil.Process(pid)
        # Check if the process is actually python running our app to prevent self-termination
        if "python" in p.name().lower():
            # Simplistic check - could be improved, but good enough to stop shooting ourselves accidentally
            cmdline = " ".join(p.cmdline()).lower()
            if "app.py" in cmdline:
                return {"success": False, "error": "Action blocked: Cannot kill dashboard backend."}
        
        p.terminate()
        p.wait(timeout=3)
        return {"success": True}
    except psutil.NoSuchProcess:
        return {"success": False, "error": "Process not found."}
    except psutil.AccessDenied:
        return {"success": False, "error": "Access denied. Please run as Administrator to kill this process."}
    except Exception as e:
        return {"success": False, "error": str(e)}
