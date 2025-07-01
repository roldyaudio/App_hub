from PIL import Image
import customtkinter as ctk
import subprocess
import sys

# Package installation
def install_requirements():
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                                capture_output=True, text=True)

        if result.returncode == 0:
            print("Dependencies installed successfully.")
            if "Requirement already satisfied" in result.stdout:
                print("Some packages were already installed.")
        else:
            print(f"Error installing dependencies: {result.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def center_hub(window, width: int, height: int):
    """Centers the window to the main display/monitor"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")


# GUI config
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(True)
ctk.set_window_scaling(True)


class MyTabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Audio")
        self.add("Reaper Tools")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configure
        self.title("App Hub Launcher")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        # Placement
        self.tab_view = MyTabs(master=self)
        self.tab_view.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Buttons in Tab_1
        image_analyzer = Image.open("resources/analyzer_icon.png")
        self.button_audio_analyzer = ctk.CTkButton(master=self.tab_view.tab("Audio"),
                                                   text="Audio properties analyzer",
                                                   image=ctk.CTkImage(dark_image=image_analyzer, size=(50, 50)),
                                                   fg_color="transparent",
                                                   border_spacing=1,
                                                   compound="bottom",
                                                   border_color="black")
        self.button_audio_analyzer.pack(pady=(15, 0))
        # self.button_audio_analyzer.grid(row=0, column=0)

        # Buttons Tab_2
        image_reaper_creator = Image.open("resources/rpp_creator_icon.png")

        self.button_reaper_creator = ctk.CTkButton(master=self.tab_view.tab("Reaper Tools"),
                                                   text="Rpp Creator",
                                                   image=ctk.CTkImage(dark_image=image_reaper_creator, size=(50, 50)),
                                                   fg_color="transparent",
                                                   border_spacing=1,
                                                   compound="bottom",
                                                   border_color="black",)
        # self.button_reaper_creator.pack(pady=(15, 0),)
        self.button_reaper_creator.grid(row=0, column=1)

        image_item_editor = Image.open("resources/item_editor_icon.png")
        self.item_editor = ctk.CTkButton(master=self.tab_view.tab("Reaper Tools"),
                                         text="Item note customizer",
                                         image=ctk.CTkImage(dark_image=image_item_editor, size=(50, 50)),
                                         fg_color="transparent",
                                         border_spacing=1,
                                         compound="bottom",
                                         border_color="black")
        # self.item_editor.pack(pady=(15, 0),)
        self.item_editor.grid(row=0, column=2, pady=15)




install_requirements()
app = App()
center_hub(app, 300, 300)
app.mainloop()