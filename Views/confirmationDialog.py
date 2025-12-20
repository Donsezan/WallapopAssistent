import customtkinter

class ConfirmationDialog(customtkinter.CTkToplevel):
    def __init__(self, title="Confirmation", text="Are you sure?", on_yes=None, on_no=None):
        super().__init__()

        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        self.label = customtkinter.CTkLabel(self, text=text, font=customtkinter.CTkFont(size=14))
        self.label.pack(pady=20, padx=20)

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10, fill="x")

        self.yes_button = customtkinter.CTkButton(self.button_frame, text="Yes", command=lambda: self._on_button_click(on_yes), width=80)
        self.yes_button.pack(side="left", padx=(40, 10), expand=True)

        self.no_button = customtkinter.CTkButton(self.button_frame, text="No", command=lambda: self._on_button_click(on_no), width=80, fg_color="gray")
        self.no_button.pack(side="right", padx=(10, 40), expand=True)
        
        self.grab_set() # Make modal

    def _on_button_click(self, callback):
        if callback:
            callback()
        self.destroy()
