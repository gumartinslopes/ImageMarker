import customtkinter as ctk
class InitialFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.parent = parent
        self._select_image_btn = ctk.CTkButton(
            master = self, 
            text = "Load Image",
            command=parent._load_image_frame
        )

        self._select_image_btn.place(relx=0.5, rely=0.5, anchor="center")
        