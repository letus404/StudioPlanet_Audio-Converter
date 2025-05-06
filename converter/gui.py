from ttkbootstrap import Style, Window
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog, StringVar
from tkinter.ttk import Combobox
import ttkbootstrap as ttk
import threading
import os
from converter.audio_converter import convert

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StudioPlanet Converter")
        self.root.geometry("600x460")
        self.root.resizable(False, False)
        self.selected_files = []
        self.output_folder = StringVar()
        self.output_format = StringVar()
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.root, text="StudioPlanet Audio Converter", font=("Segoe UI", 16, "bold")).pack(pady=10)

        ttk.Button(self.root, text="Seleccionar Archivos", bootstyle="primary outline", command=self.select_files).pack(pady=5)

        ttk.Button(self.root, text="Carpeta de salida", bootstyle="info outline", command=self.select_output_folder).pack(pady=5)

        ttk.Label(self.root, text="Selecciona el formato de salida:").pack(pady=5)
        self.format_combobox = Combobox(self.root, textvariable=self.output_format, values=["mp3", "wav", "flac", "ogg", "m4a", "aiff"])
        self.format_combobox.set("mp3")
        self.format_combobox.pack(pady=5)

        self.convert_button = ttk.Button(self.root, text="Convertir archivo", bootstyle="success", command=self.start_conversion_thread, width=30)
        self.convert_button.pack(pady=15)

        # Frame horizontal para el estado y el botón
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(pady=(10, 15))

        # Canvas con sombra y círculo de estado
        self.status_canvas = ttk.Canvas(bottom_frame, width=32, height=32, highlightthickness=0, bg="white")
        self.shadow_circle = self.status_canvas.create_oval(4, 4, 28, 28, fill="#d0d0d0", outline="")
        self.status_circle = self.status_canvas.create_oval(6, 6, 26, 26, fill="red", outline="")
        self.status_canvas.pack(side="left", padx=(0, 10))

        # Botón de abrir carpeta
        ttk.Button(bottom_frame, text="Abrir Carpeta de Destino", bootstyle="secondary", command=self.open_output_folder).pack(side="left")

    def set_status_color(self, color):
        self.status_canvas.itemconfig(self.status_circle, fill=color)

    def select_files(self):
        self.selected_files = filedialog.askopenfilenames(
            title="Seleccionar archivos de audio",
            filetypes=[("Archivos de Audio", "*.mp3 *.wav *.flac *.ogg *.m4a *.aiff")]
        )

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Selecciona la carpeta de salida")
        if folder:
            self.output_folder.set(folder)

    def open_output_folder(self):
        folder = self.output_folder.get()
        if folder and os.path.isdir(folder):
            os.startfile(folder)

    def start_conversion_thread(self):
        threading.Thread(target=self.convert_files, daemon=True).start()

    def convert_files(self):
        if not self.selected_files:
            self.root.after(0, lambda: Messagebox.show_warning("No se seleccionaron archivos."))
            return
        if not self.output_folder.get():
            self.root.after(0, lambda: Messagebox.show_warning("Selecciona una carpeta de salida."))
            return

        self.convert_button["state"] = "disabled"
        self.set_status_color("orange")

        output_format = self.output_format.get()

        for i, file in enumerate(self.selected_files, 1):
            filename = os.path.basename(file)
            basename = os.path.splitext(filename)[0]
            output_filename = f"{basename}.{output_format}"
            output_path = os.path.join(self.output_folder.get(), output_filename)

            try:
                convert(file, output_path, None, self.root)
            except Exception as e:
                self.root.after(0, lambda f=file, err=e: Messagebox.show_error(f"Error al convertir {f}:\n{err}"))
                self.set_status_color("red")
                continue

        self.set_status_color("green")
        self.root.after(0, lambda: Messagebox.ok("Conversión lista."))
        self.root.after(100, self.open_output_folder)
        self.convert_button["state"] = "normal"
