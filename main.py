import tkinter as tk

from system_model import SystemModel
from system_view import SystemView
from system_controller import SystemController


class App:
    def __init__(self):
        # Tela princial
        self.root = tk.Tk()
        self.root.title("Dashboard do Sistema")
        self.root.geometry("675x380")
        self.root.configure(bg="grey")

        # Container da tela
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.main_frame.configure(bg="darkslategray")

        # Inicializa o mvc
        self.model = SystemModel()
        self.view = SystemView(self.main_frame)
        self.controller = SystemController(self.model, self.view)

        self.adjust_column_widths()

        self.root.mainloop()

    def adjust_column_widths(self):
        self.view.adjust_column_widths()
        
# Instância da classe App e o loop principal do Tkinter
if __name__ == "__main__":
    app = App()