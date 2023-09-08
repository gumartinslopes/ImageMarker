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
        self.combobox.grid(row = 0, column = 0, padx=20, pady=10)
        
        self._save_btn = ctk.CTkButton(
            self._option_frame, text = "Save", command = self._image_canvas.save)
        self._save_btn.grid(row = 1, column = 0, padx = 20, pady = 20)
        
        self._new_image_btn =  ctk.CTkButton(
            self._option_frame, text = "New Image", command = self._load_new_image)
        self._new_image_btn.grid(row = 2, column = 0, padx = 20, pady = 20)
        
        self._load_annotation_btn =  ctk.CTkButton(
            self._option_frame, text = "Load annotation", command = self._image_canvas.load_annotation)
        self._load_annotation_btn.grid(row =3, column = 0, padx = 20, pady = 20)

        # Marker size slider
        self._size_slider_label = ctk.CTkLabel(master=self._option_frame, text="Brush Size    5")
        self._size_slider_label.grid(row = 5, column = 0, padx = 20, pady = (20,0), sticky = "w")
        self._size_slider = ctk.CTkSlider(master=self._option_frame, from_=1, to=20, command=self._slider_event)
        self._size_slider.grid(row = 6, column = 0)
        self._size_slider.set(5)
        
        # Zoom Buttons
        self._zoom_frame_label = ctk.CTkLabel(master = self._option_frame, text="Zoom")
        self._zoom_frame_label.grid(row = 7, column = 0, padx = 20, pady = (20,0), sticky = "w")
        self._zoom_frame = ctk.CTkFrame(self._option_frame)
        self._zoom_frame.grid(row = 8, column = 0, sticky = "s")
        
        self._zoom_in_btn =  ctk.CTkButton(
            self._zoom_frame, text = "+", command = self._image_canvas._zoom_in, width = 60)
        self._zoom_in_btn.grid(row =0, column = 0,padx = 20,pady = 20)
        
        self._zoom_out_btn =  ctk.CTkButton(
            self._zoom_frame, text = "-", command = self._image_canvas._zoom_out, width = 60)
        self._zoom_out_btn.grid(row =0, column = 1,padx = 20, pady = 20) 

    def _slider_event(self, value):
        self._size_slider_label.configure(text = f"Brush Size    {int(value)}")
        self._image_canvas._set_brush_size(value)

    def _load_new_image(self):
        img_path = read_file_path()
        image = open_image(img_path)
        if image is not None:
            self._image_canvas.destroy()
            self._config_widgets(image)