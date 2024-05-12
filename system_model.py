import psutil
import toolbox

class SystemModel:
    def __init__(self):
        pass

    # Obtém o uso da CPU
    def get_cpu_usage(self):
        cpu_percent = psutil.cpu_percent()
        cpu_idle = 100 - cpu_percent
        process_count = len(psutil.pids())
        thread_count = psutil.cpu_count()
        return cpu_percent, cpu_idle, process_count, thread_count

    # Obtém o uso da memória
    def get_memory_usage(self):
        virtual_memory = psutil.virtual_memory()
        physical_memory = psutil.swap_memory()
        memory_percent = virtual_memory.percent
        memory_free = toolbox.bytes_to_gb(virtual_memory.available)
        physical_memory_total = toolbox.bytes_to_gb(physical_memory.total)
        virtual_memory_total = toolbox.bytes_to_gb(virtual_memory.total)
        return memory_percent, memory_free, physical_memory_total, virtual_memory_total
    
    # Retorna uma lista com os nomes dos processos e o pid
    def get_process_list(self):
        process_list = psutil.process_iter(['pid', 'name'])
        return [(process.info['pid'], process.info['name']) for process in process_list]

    # Método estático para obter informações sobre um determinado processo
    @staticmethod
    def get_process_details(pid):
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