from PIL import Image
import customtkinter as ctk
import subprocess
import sys
from repo_manager import load_repos, clone_or_update_repo_async

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


class MyTabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Audio")
        self.add("Reaper Tools")
        self.add("Backup")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configure
        self.title("App hub Launcher")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        # REPO CLONING
        self.download_path, self.repos = load_repos()

        # Placement
        self.tab_view = MyTabs(master=self, segmented_button_unselected_hover_color="green", )
        self.tab_view.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Buttons in Tab_1
            # AUDIO ANALYZER BUTTON
        image_analyzer = Image.open("resources/analyzer_icon.png")
        self.button_audio_analyzer = ctk.CTkButton(master=self.tab_view.tab("Audio"),
                                                   text="Audio analyzer",
                                                   image=ctk.CTkImage(dark_image=image_analyzer, size=(50, 50)),
                                                   fg_color="transparent",
                                                   border_spacing=1,
                                                   compound="bottom", width=100, height=100, )
        self.button_audio_analyzer.pack(pady=(15, 0), )
        # self.button_audio_analyzer.grid(row=0, column=0)

        # Buttons Tab_2
            # RPP CREATOR BUTTON
        image_reaper_creator = Image.open("resources/rpp_creator_icon.png")

        self.button_reaper_creator = ctk.CTkButton(master=self.tab_view.tab("Reaper Tools"),
                                                   text="Rpp Creator",
                                                   image=ctk.CTkImage(dark_image=image_reaper_creator, size=(50, 50)),
                                                   fg_color="transparent",
                                                   border_spacing=1,
                                                   compound="bottom", width=100, height=100, )
        self.button_reaper_creator.pack(pady=(15, 0),)
        # self.button_reaper_creator.grid(row=0, column=1, )

            # ITEM NOTE CUSTOMIZER BUTTON
        image_item_editor = Image.open("resources/item_editor_icon.png")
        self.item_editor = ctk.CTkButton(master=self.tab_view.tab("Reaper Tools"),
                                         text="Item notes\ncustomizer",
                                         image=ctk.CTkImage(dark_image=image_item_editor, size=(50, 50)),
                                         fg_color="transparent",
                                         border_spacing=1,
                                         compound="bottom", width=100, height=100, )
        self.item_editor.pack(pady=(15, 0),)
        # self.item_editor.grid(row=0, column=2, pady=15, )

        # Buttons Tab_3
            # BACKUP
        image_backup = Image.open("resources/backup_icon.png")
        self.backup_files = ctk.CTkButton(master=self.tab_view.tab("Backup"),
                                         text="Backup files",
                                         image=ctk.CTkImage(dark_image=image_backup, size=(50, 50)),
                                         fg_color="transparent",
                                         border_spacing=1,
                                         compound="bottom", width=100, height=100,
                                          command=lambda : self.clone_repo("Backup files"))
        self.backup_files.pack(pady=(15, 0), )

    def clone_repo(self, app_name):
        for repo in self.repos:
            if repo["name"] == app_name:
                clone_or_update_repo_async(repo["repo_url"], self.download_path)
                break


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(True)
ctk.set_window_scaling(True)

install_requirements()
app = App()
center_hub(app, 280, 320)
app.mainloop()