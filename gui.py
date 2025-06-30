import customtkinter as ctk

# Main GUI
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
ctk.set_widget_scaling(True)
ctk.set_window_scaling(True)

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
        self.add("Reaper Tools")
        self.add("Audio")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configure
        self.title("App Hub")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        # Placement
        self.tab_view = MyTabs(master=self)
        self.tab_view.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Buttons Tab_1
        self.button_reaper_creator = ctk.CTkButton(master=self.tab_view.tab("Reaper Tools"), text="Rpp Creator")
        self.item_editor = ctk.CTkButton(master=self.tab_view.tab("Reaper Tools"), text="Item notes Editor")
        self.button_reaper_creator.pack(pady=(20, 10))
        self.item_editor.pack(pady=(20, 20))

        # Buttons Tab_1
        self.button_audio_analizer = ctk.CTkButton(master=self.tab_view.tab("Audio"), text="Audio analyzer")
        self.button_audio_analizer.pack(pady=(20, 20))


app = App()
center_hub(app, 250, 200)
app.mainloop()