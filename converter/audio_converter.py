import ffmpeg
from tkinter import messagebox

def convert(input_file, output_file, progress, root):
    """Convierte un archivo de audio utilizando ffmpeg y actualiza la barra de progreso."""
    try:
        process = (
            ffmpeg
            .input(input_file)
            .output(output_file)
            .run_async(pipe_stderr=True)
        )

        # Simulamos progreso arbitrario (real no es fácil sin duración)
        while True:
            line = process.stderr.readline()
            if not line:
                break

            decoded_line = line.decode("utf-8", errors="ignore")
            if "size=" in decoded_line:
                # Se puede usar este punto para actualizar un valor estimado de progreso
                progress['value'] += 1
                if progress['value'] > 100:
                    progress['value'] = 100
                root.update_idletasks()

        process.wait()

        root.after(0, lambda: messagebox.showinfo("Éxito", f"Conversión completada:\n{output_file}"))
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", f"Error al convertir {input_file}:\n{e}"))