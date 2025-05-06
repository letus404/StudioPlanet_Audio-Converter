from converter.gui import AudioConverterApp
from converter.ffmpeg_config import configure_ffmpeg
from ttkbootstrap import Window

def main():
    configure_ffmpeg()
    app = Window(themename="darkly")
    AudioConverterApp(app)
    app.mainloop()

if __name__ == "__main__":
    main()