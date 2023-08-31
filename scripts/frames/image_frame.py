import customtkinter as ctk
from PIL import Image
from ..utils.image_canvas import ImageCanvas
from ..utils.file_manager import read_file_path, open_image

class ImageFrame(ctk.CTkFrame):
    def __init__(self, parent, image, **kwargs):
        super().__init__(master=parent, **kwargs)
        self.parent = parent
        self._config_grid()
        self._config_widgets(image)

    def _config_grid(self):
        self.rowconfigure(0, weight=2) 
        self.columnconfigure(0, weight=2)

    def _choose_marker(self, choice):
        if choice == "Object Marker":
            self._image_canvas.set_obj_marker()
        elif choice == "Background Marker":
            self._image_canvas.set_bg_marker()
        elif choice == "Uncertain Marker":
            self._image_canvas.set_uncertain_marker()
        else:
            self._image_canvas.set_remove()

    def _config_widgets(self, image):
        self._image_canvas = ImageCanvas(self, image)
        self._image_canvas.grid(row = 0, column = 0, sticky = "nswe", columnspan = 3)
        self._config_option_frame()


    def _config_option_frame(self):
        self._option_frame = ctk.CTkFrame(self)
        self._option_frame.grid(row = 0, column = 2, sticky = "nswe")
        self.combobox = ctk.CTkOptionMenu(master=self._option_frame,
                                       values=["Object Marker", "Background Marker", "Uncertain Marker", "remove"],
                                       command=self._choose_marker)
        self.combobox.set("Object Marker")  # set initial value
        self._save_btn = ctk.CTkButton(
            self._option_frame, text = "Save", command = self._image_canvas.save)
        
        self._new_image_btn =  ctk.CTkButton(
            self._option_frame, text = "New Image", command = self._load_new_image)
        
        self._load_annotation_btn =  ctk.CTkButton(
            self._option_frame, text = "Load annotation", command = self._image_canvas.load_annotation)
        
        self.combobox.grid(row = 0, column = 0, padx=20, pady=10)
        self._save_btn.grid(row = 1, column = 0, padx = 20, pady = 20)
        self._new_image_btn.grid(row = 2, column = 0, padx = 20, pady = 20)
        self._load_annotation_btn.grid(row =3, column = 0, padx = 20, pady = 20)
    
    def _load_new_image(self):
        img_path = read_file_path()
        image = open_image(img_path)
        if image is not None:
            self._image_canvas.destroy()
            self._config_widgets(image)