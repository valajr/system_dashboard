from system_model import SystemModel

class SystemController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.schedule_update()

    # Método para atualizar as informações do dashboard
    def refresh_data(self):
        cpu_percent, cpu_idle, process_count, thread_count = self.model.get_cpu_usage()
        memory_percent, memory_free, physical_memory_total, virtual_memory_total = self.model.get_memory_usage()
        process_list = self.model.get_process_list()
        
        self.view.update_cpu_usage(cpu_percent, cpu_idle, process_count, thread_count)
        self.view.update_memory_usage(memory_percent, memory_free, physical_memory_total, virtual_memory_total)
        self.view.create_process_buttons(process_list)
        self.view.adjust_column_widths()

    # Temporizador para atualizar as informações novamente
    def schedule_update(self):
        self.refresh_data()
        self.view.after(5000, self.schedule_update)

    @staticmethod
    def get_process_details(pid):
        details = SystemModel.get_process_details(pid)
        return details