import tkinter as tk
from tkinter import *
from tkinter import ttk
import psutil

import toolbox

# Função de atualizar os dados mostrados
def update_data():
    cpu_percent, cpu_idle, process_count, thread_count = toolbox.get_cpu_usage()
    cpu_percent_label.config(text=f"Uso do Processador: {cpu_percent}%")
    cpu_idle_label.config(text=f"Tempo Ocioso: {cpu_idle}%")
    process_count_label.config(text=f"Total de Processos: {process_count}")
    thread_count_label.config(text=f"Total de Threads: {thread_count}")

    memory_percent, memory_free, physical_memory_total, virtual_memory_total = toolbox.get_memory_usage()
    progressbar["value"] = memory_percent
    memory_percent_label.config(text=f"Uso da Memória: {memory_percent}%")
    memory_free_label.config(text=f"Memória Livre: {memory_free:.2f} Gb")
    physical_memory_total_label.config(text=f"Memória Física Total (RAM): {physical_memory_total:.2f} Gb")
    virtual_memory_total_label.config(text=f"Memória Virtual Total: {virtual_memory_total:.2f} Gb")
    pass

# Função temporizada para chamar a função novamente
def schedule_update():
    update_data()
    app.after(5000, schedule_update)

# Função que mostra informações detalhadas dos processos
def show_process_details(pid):
    try:
        process_details = toolbox.get_memory_details(pid)
        if process_details:
            details_window = tk.Toplevel(app)
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
            details_text = f"PID: {process_details['pid']}\n"
            details_text += f"Nome: {process_details['name']}\n"
            if 'memory_info' in process_details:
                details_text += f"Memória Residente: {toolbox.bytes_to_mb(process_details['memory_info'].rss):.2f} Mb\n"
            else:
                details_text += "Informações de memória não disponíveis\n"

            details_label.config(text=details_text)
        else:
            tk.showerror("Erro", f"O processo com PID {pid} não foi encontrado.")
    except psutil.AccessDenied as e:
        tk.showerror("Erro de Permissão", f"Você não tem permissão para acessar informações sobre o processo com PID {pid}.")
    except Exception as e:
        tk.showerror("Erro", f"Ocorreu um erro ao obter informações sobre o processo com PID {pid}: {str(e)}")
    pass

# Função para criar um botão para cada processo
def create_process_buttons():
    process_list = psutil.process_iter(['pid', 'name'])
    for idx, process in enumerate(process_list):
        pid = process.info['pid']
        name = process.info['name']
        process_button = tk.Button(process_container, text=f"{pid} - {name}", command=lambda p=pid: show_process_details(p))
        process_button.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

# Tela princial
app = tk.Tk()
app.title("Dashboard")
app.geometry("675x380")
app.configure(bg="grey")

# Container da tela
main_frame = tk.Frame(app)
main_frame.pack(expand=True, fill="both", padx=10, pady=10)
main_frame.configure(bg="darkslategray")

# Container do uso de CPU
cpu_label = tk.Label(main_frame, text="Uso de CPU:", foreground="white", bg="darkslategrey")
cpu_label.grid(row=0, column=0, padx=0, pady=(10, 0))
cpu_frame = tk.Frame(main_frame, bg="grey", borderwidth=2, relief="groove")
cpu_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w", columnspan=4)

# Dados do container de uso do CPU
cpu_percent_label = tk.Label(cpu_frame, text="", bg="grey", foreground="white")
cpu_idle_label = tk.Label(cpu_frame, text="", bg="grey", foreground="white")
process_count_label = tk.Label(cpu_frame, text="", bg="grey", foreground="white")
thread_count_label = tk.Label(cpu_frame, text="", bg="grey", foreground="white")

cpu_percent_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
cpu_idle_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
process_count_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
thread_count_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

# Container de uso de Memória
memory_label = tk.Label(main_frame, text="Uso de memória:", foreground="white", bg="darkslategrey")
memory_label.grid(row=2, column=0, padx=0, pady=(0, 5))
memory_frame = tk.Frame(main_frame, bg="grey", borderwidth=2, relief="groove")
memory_frame.grid(row=3, column=0, padx=10, pady=0, sticky="w", columnspan=4)

# Dados do container de uso de memória
progressbar = ttk.Progressbar(memory_frame, orient="horizontal", mode="determinate")
memory_percent_label = tk.Label(memory_frame, text="", bg="grey", foreground="white")
memory_free_label = tk.Label(memory_frame, text="", bg="grey", foreground="white")
physical_memory_total_label = tk.Label(memory_frame, text="", bg="grey", foreground="white")
virtual_memory_total_label = tk.Label(memory_frame, text="", bg="grey", foreground="white")

progressbar.grid(row=0, column=0, padx=10, pady=(10,0), sticky="n")
memory_percent_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
memory_free_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
physical_memory_total_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
virtual_memory_total_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

scrollbar = tk.Scrollbar(main_frame, orient="vertical")

# Container dos processos individuais
process_label = tk.Label(main_frame, text="Processos abertos:", foreground="white", bg="darkslategrey")
process_label.grid(row=0, column=1, padx=0, pady=(10, 0))
process_frame = tk.Frame(main_frame, borderwidth=2, relief="groove")
process_frame.grid(row=1, column=1, padx=10, pady=5, ipady=23, sticky="w", rowspan=10)

# Criar uma Canvas para o quadro dos processos
process_canvas = tk.Canvas(process_frame)
process_scrollbar = tk.Scrollbar(process_frame, orient="vertical", command=process_canvas.yview)
process_scrollbar.pack(side="right", fill="y")
process_canvas.pack(side="right", fill="both", expand=True)
process_canvas.configure(yscrollcommand=process_scrollbar.set)

process_container = tk.Frame(process_canvas)
process_canvas.create_window((0, 0), window=process_container, anchor="nw")
process_canvas.bind("<Configure>", lambda e: process_canvas.configure(scrollregion=process_canvas.bbox("all")))

create_process_buttons()
schedule_update()

# Ajuste de largura da coluna do lado esquerdo
memory_frame.update_idletasks()
memory_frame_width = memory_frame.winfo_reqwidth()
main_frame.columnconfigure(0, minsize=memory_frame_width+10)
cpu_frame.columnconfigure(0, minsize=memory_frame_width-5)

app.mainloop()