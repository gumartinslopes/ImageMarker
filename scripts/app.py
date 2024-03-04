import customtkinter as ctk
from tkinter import messagebox
from .utils.file_manager import read_file_path
from .frames.initial_frame import InitialFrame
from .frames.image_frame import ImageFrame
from .utils.file_manager import open_image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image Marker")
        self._config_window(width = 1200,height = 600)
        self._current_frame = None
        self._load_initial_frame()
        self.__project_name = ''

    @property
    def project_name(self):
        return self.__project_name
    
    @project_name.setter
    def set_project_name(self, new_name):
        self.__project_name = new_name
        
    def _config_window(self, width, height):
        self.width = width
        self.height = height
        self.geometry(f"{width}x{height}")
        self._center_window()

    def _center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width/2) - (self.width/2)
        y = (screen_height/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y-50))
    
    def _clear_frame(self):
        if self._current_frame is not None:
            self._current_frame.destroy()

    def _load_initial_frame(self):
        self._clear_frame()
        self._initial_frame = InitialFrame(parent = self)
        self._current_frame = self._initial_frame
        self._initial_frame.pack(fill=ctk.BOTH, expand=True)

    def _load_image_frame(self):
        filepath = read_file_path()
        image = open_image(filepath)
        if image is not None:
            self._clear_frame()
            self._image_frame = ImageFrame(parent = self, image=image)
            self._current_frame = self._image_frame
            self._image_frame.pack(fill=ctk.BOTH, expand=True)