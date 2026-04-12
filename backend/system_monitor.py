import psutil
import time
import threading
import datetime

try:
    SYSTEM_BOOT_TIME = psutil.boot_time()
except Exception:
    SYSTEM_BOOT_TIME = time.time()

# Initialize CPU measurement globally before API starts
latest_cpu_percent = 0.0

def background_monitor():
    global latest_cpu_percent
    while True:
        # Blocks for 1 second, providing exact real-time average like Task Manager
        latest_cpu_percent = psutil.cpu_percent(interval=1)

monitor_thread = threading.Thread(target=background_monitor, daemon=True)
monitor_thread.start()

last_net_io = psutil.net_io_counters()
last_disk_io = psutil.disk_io_counters()
last_net_time = time.time()

def get_system_stats():
    global last_net_io, last_disk_io, last_net_time, latest_cpu_percent
    
    # Use the continuously updated true CPU percent
    cpu_percent = latest_cpu_percent
        
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    total = mem.total
    used = mem.used
    available = mem.available
    cached = getattr(mem, 'cached', 0)
    buffers = getattr(mem, 'buffers', 0)
    
    true_used = total - available
    true_percent = (true_used / total) * 100
    
    # Network and Disk Tracking
    current_net_io = psutil.net_io_counters()
    current_disk_io = psutil.disk_io_counters()
    current_time = time.time()
    time_delta = current_time - last_net_time
    
    if time_delta > 0:
        upload_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_delta
        download_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_delta
        
        # Calculate Disk Active Time (I/O time vs Elapsed time)
        read_time_diff = current_disk_io.read_time - last_disk_io.read_time
        write_time_diff = current_disk_io.write_time - last_disk_io.write_time
        active_ms = read_time_diff + write_time_diff
        
        disk_activity_percent = (active_ms / (time_delta * 1000)) * 100
        disk_activity_percent = max(0.0, min(100.0, disk_activity_percent))
        
        disk_read_speed = (current_disk_io.read_bytes - last_disk_io.read_bytes) / time_delta
        disk_write_speed = (current_disk_io.write_bytes - last_disk_io.write_bytes) / time_delta
    else:
        upload_speed = 0.0
        download_speed = 0.0
        disk_activity_percent = 0.0
        disk_read_speed = 0.0
        disk_write_speed = 0.0
        
    last_net_io = current_net_io
    last_disk_io = current_disk_io
    last_net_time = current_time

    # Primary Intelligent Health Score Math
    health_score = 100 - (cpu_percent * 0.4 + true_percent * 0.4 + disk.percent * 0.2)
    health_score = max(0, min(100, health_score)) # Clamp between 0-100
    
    # Semantic Recommendation Engine
    if cpu_percent > 85:
        recommendation = "High CPU load detected. Monitor top processes in the Processes tab."
    elif true_percent > 85:
        recommendation = "Heavy memory pressure. Close unused applications to boost health."
    elif available < 500 * 1024**2:
        recommendation = "Warning: Low available memory limits performance stability."
    elif disk.percent > 90:
        recommendation = "Critical: Disk storage logic is near capacity."
    else:
        recommendation = "System running normally. Resources are fully optimized."

    if available > 1 * 1024**3:
        status = "Healthy (High usage mostly cached)" if mem.percent > 80 else "System is using RAM efficiently"
    elif available < 500 * 1024**2:
        status = "Critical (Low available memory - performance may degrade)"
    else:
        status = "Moderate usage"
        
    # Intelligence Logic for CPU
    if cpu_percent < 5:
        cpu_status = "System is idle"
    elif cpu_percent > 80:
        cpu_status = "High load detected"
    else:
        cpu_status = "Normal usage"
        
    try:
        cpu_freq = psutil.cpu_freq()
        freq_current = round(cpu_freq.current, 0) if cpu_freq else 0
        freq_max = round(cpu_freq.max, 0) if cpu_freq else 0
    except Exception:
        freq_current, freq_max = 0, 0
        
    return {
        "cpu": {
            "percent": cpu_percent,
            "status": cpu_status,
            "cores_logical": psutil.cpu_count(logical=True),
            "cores_physical": psutil.cpu_count(logical=False),
            "freq_current": freq_current,
            "freq_max": freq_max
        },
        "memory": {
            "total": total,
            "used": used,
            "available": available,
            "cached": cached,
            "buffers": buffers,
            "true_used": true_used,
            "percent": mem.percent,
            "true_percent": round(true_percent, 1),
            "status": status
        },
        "disk": {
            "percent": disk.percent,
            "activity_percent": round(disk_activity_percent, 1),
            "read_speed": disk_read_speed,
            "write_speed": disk_write_speed,
            "used": disk.used,
            "total": disk.total
        },
        "network": {
            "upload_speed": upload_speed,
            "download_speed": download_speed
        },
        "system": {
            "boot_time": SYSTEM_BOOT_TIME
        },
        "health_score": round(health_score, 0),
        "recommendation": recommendation
    }
