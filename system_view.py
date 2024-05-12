import tkinter as tk
from tkinter import *
from tkinter import ttk

from system_controller import SystemController
import toolbox

class SystemView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets(master)

    def create_widgets(self, main_frame):
        # Container do uso de CPU
        self.cpu_label = tk.Label(main_frame, text="Uso de CPU:", foreground="white", bg="darkslategrey")
        self.cpu_label.grid(row=0, column=0, padx=0, pady=(10, 0))
        self.cpu_frame = tk.Frame(main_frame, bg="grey", borderwidth=2, relief="groove")
        self.cpu_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w", columnspan=4)

        self.cpu_percent_label = tk.Label(self.cpu_frame, text="", bg="grey", foreground="white")
        self.cpu_idle_label = tk.Label(self.cpu_frame, text="", bg="grey", foreground="white")
        self.process_count_label = tk.Label(self.cpu_frame, text="", bg="grey", foreground="white")
        self.thread_count_label = tk.Label(self.cpu_frame, text="", bg="grey", foreground="white")
        
        self.cpu_percent_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.cpu_idle_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.process_count_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.thread_count_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Container de uso de Memória
        self.memory_label = tk.Label(main_frame, text="Uso de memória:", foreground="white", bg="darkslategrey")
        self.memory_label.grid(row=2, column=0, padx=0, pady=(0, 5))
        self.memory_frame = tk.Frame(main_frame, bg="grey", borderwidth=2, relief="groove")
        self.memory_frame.grid(row=3, column=0, padx=10, pady=0, sticky="w", columnspan=4)

        self.progressbar = ttk.Progressbar(self.memory_frame, orient="horizontal", mode="determinate")
        self.memory_percent_label = tk.Label(self.memory_frame, text="", bg="grey", foreground="white")
        self.memory_free_label = tk.Label(self.memory_frame, text="", bg="grey", foreground="white")
        self.physical_memory_total_label = tk.Label(self.memory_frame, text="", bg="grey", foreground="white")
        self.virtual_memory_total_label = tk.Label(self.memory_frame, text="", bg="grey", foreground="white")
        
        self.progressbar.grid(row=0, column=0, padx=10, pady=(10,0), sticky="n")
        self.memory_percent_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.memory_free_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.physical_memory_total_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.virtual_memory_total_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        
        # Container dos processos individuais
        self.process_label = tk.Label(main_frame, text="Processos abertos:", foreground="white", bg="darkslategrey")
        self.process_label.grid(row=0, column=1, padx=0, pady=(10, 0))
        self.process_frame = tk.Frame(main_frame, borderwidth=2, relief="groove")
        self.process_frame.grid(row=1, column=1, padx=10, pady=5, ipady=23, sticky="w", rowspan=10)

        # Canvas para o quadro dos processos
        self.process_canvas = tk.Canvas(self.process_frame)
        self.process_scrollbar = tk.Scrollbar(self.process_frame, orient="vertical", command=self.process_canvas.yview)
        self.process_scrollbar.pack(side="right", fill="y")
        self.process_canvas.pack(side="right", fill="both", expand=True)
        self.process_canvas.configure(yscrollcommand=self.process_scrollbar.set)

        self.process_container = tk.Frame(self.process_canvas)
        self.process_canvas.create_window((0, 0), window=self.process_container, anchor="nw")
        self.process_canvas.bind("<Configure>", lambda e: self.process_canvas.configure(scrollregion=self.process_canvas.bbox("all")))

        pass

    # Atualiza as informações de uso do CPU
    def update_cpu_usage(self, cpu_percent, cpu_idle, process_count, thread_count):
        self.cpu_percent_label.config(text=f"Uso do Processador: {cpu_percent}%")
        self.cpu_idle_label.config(text=f"Tempo Ocioso: {cpu_idle}%")
        self.process_count_label.config(text=f"Total de Processos: {process_count}")
        self.thread_count_label.config(text=f"Total de Threads: {thread_count}")

        pass

    # Atualiza as informações do uso de memória
    def update_memory_usage(self, memory_percent, memory_free, physical_memory_total, virtual_memory_total):        
        self.progressbar["value"] = memory_percent
        self.memory_percent_label.config(text=f"Uso da Memória: {memory_percent}%")
        self.memory_free_label.config(text=f"Memória Livre: {memory_free:.2f} Gb")
        self.physical_memory_total_label.config(text=f"Memória Física Total (RAM): {physical_memory_total:.2f} Gb")
        self.virtual_memory_total_label.config(text=f"Memória Virtual Total: {virtual_memory_total:.2f} Gb")
        
        pass

    # Cria os botões dos processos abertos
    def create_process_buttons(self, process_list):
        for idx, (pid, name) in enumerate(process_list):
            process_button = tk.Button(self.process_container, text=f"{pid} - {name}", 
                                       command=lambda p=pid: self.show_process_details(p))
            process_button.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

    # Método que será executado ao clicar um botão de processo
    def show_process_details(self, pid):
        process_details = SystemController.get_process_details(pid)
        if process_details:
            # Cria uma nova janela
            details_window = tk.Toplevel(self.master)
            details_window.title(f"Processo {pid}")
            details_window.geometry("250x140")

            # Cria uma borda da janela nova 
            border_frame = tk.Frame(details_window, bg="grey", padx=10, pady=10)
            border_frame.pack(expand=True, fill="both")
            details_frame = tk.Frame(border_frame, bg="darkslategrey")
            details_frame.pack(expand=True, fill="both")

            # Cria os elementos a serem mostrados
            border_label = tk.Label(details_frame, pady=0, text=f"Informações do Processo {pid}", bg="darkslategrey",
                                    foreground="white")
            border_label.pack(expand=True)
            details_label = tk.Label(details_frame, padx=10, pady=10, text="", bg="grey", foreground="white", borderwidth=2, 
                                    relief="groove")
            details_label.pack(expand=True)
            details_text = f"PID: {pid}\n"
            details_text += f"Nome: {process_details['name']}\n"
            if 'memory_info' in process_details:
                details_text += f"Memória Residente: {toolbox.bytes_to_mb(process_details['memory_info'].rss):.2f} Mb\n"
            else:
                details_text += "Informações de memória não disponíveis\n"

            details_label.config(text=details_text)
        else:
            tk.showerror("Erro", f"O processo com PID {pid} não foi encontrado.")
        pass

    # Ajuste de largura da coluna do lado esquerdo
    def adjust_column_widths(self):
        self.memory_frame.update_idletasks()
        memory_width = self.memory_frame.winfo_reqwidth()
        self.master.columnconfigure(0, minsize=memory_width + 10)
        self.cpu_frame.columnconfigure(0, minsize=memory_width - 5)

    pass