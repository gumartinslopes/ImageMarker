import customtkinter as ctk
from ..utils.image_canvas import ImageCanvas

class ImageFrame(ctk.CTkFrame):
    def __init__(self, parent, image_path, **kwargs):
        super().__init__(master=parent, **kwargs)
        self.parent = parent
        self.image_path = image_path
        self._config_grid()
        self._config_canvas_image()
        self._config_option_frame()

    def _config_grid(self):
        self.rowconfigure(0, weight=2) 
        self.columnconfigure(0, weight=2)

    def _config_canvas_image(self):
        self._canvas_image = ImageCanvas(self, self.image_path)
        self._canvas_image.grid(row = 0, column = 0, sticky = "nswe", columnspan = 3)

    def _config_option_frame(self):
        self._option_frame = ctk.CTkFrame(self)
        self._option_frame.grid(row = 0, column = 2, sticky = "nswe")

        self._obj_btn = ctk.CTkButton(
            self._option_frame, text = "Object marker", command = self._canvas_image.set_obj_marker)
        self._uncertain_btn = ctk.CTkButton(
            self._option_frame, text = "Uncertain marker", command = self._canvas_image.set_uncertain_marker)
        self._bj_btn = ctk.CTkButton(
            self._option_frame,  text = "Background marker", command = self._canvas_image.set_bg_marker)
        self._clear_btn = ctk.CTkButton(
            self._option_frame, text = "Erase", command = self._canvas_image.set_erase)
        self._save_btn = ctk.CTkButton(
            self._option_frame, text = "Save", command = self._canvas_image.save)
    
        self._obj_btn.grid(row = 0, column = 1, padx = 20, pady = 20)
        self._uncertain_btn.grid(row = 0, column = 2, padx = 20, pady = 20)
        self._bj_btn.grid(row = 0, column = 3, padx = 20, pady = 20)
        self._clear_btn.grid(row = 1, column = 2, padx = 20, pady = 20)
        self._save_btn.grid(row = 1, column = 1, padx = 20, pady = 20)