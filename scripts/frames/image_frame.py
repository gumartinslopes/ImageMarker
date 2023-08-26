import customtkinter as ctk
from PIL import Image

class ImageFrame(ctk.CTkFrame):
    def __init__(self, parent, image_path):
        super().__init__(master=parent)
        self.parent = parent
        self.image_path = image_path
        self._config_btns()

    def _config_btns(self):
        self._select_image_btn = ctk.CTkButton(
            master = self, 
            text = "Image Frame", 
            command=self.parent.open_img
        )

        self._select_image_btn.place(relx=0.5, rely=0.5, anchor="center")