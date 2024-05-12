import psutil
    
def bytes_to_mb(bytes):
    return bytes / (1024 ** 2)  # 1 MB = 1024 * 1024 bytes

def bytes_to_gb(bytes):
    return bytes / (1024 ** 3)  # 1 GB = 1024 * 1024 * 1024 bytes

def get_cpu_usage():
    cpu_percent = psutil.cpu_percent()
    cpu_idle = 100 - cpu_percent
    process_count = len(psutil.pids())
    thread_count = psutil.cpu_count()
    return cpu_percent, cpu_idle, process_count, thread_count

def get_memory_usage():
    virtual_memory = psutil.virtual_memory()
    physical_memory = psutil.swap_memory()
    memory_percent = virtual_memory.percent
    memory_free = bytes_to_gb(virtual_memory.available)
    physical_memory_total = bytes_to_gb(physical_memory.total)
    virtual_memory_total = bytes_to_gb(virtual_memory.total)
    return memory_percent, memory_free, physical_memory_total, virtual_memory_total

def get_memory_details(pid):
    try:
        proc = psutil.Process(pid)
        memory_info = proc.memory_full_info()
        return {
            'pid': proc.pid,
            'name': proc.name(),
            'memory_info': memory_info,
        }
    except psutil.NoSuchProcess:
        return None