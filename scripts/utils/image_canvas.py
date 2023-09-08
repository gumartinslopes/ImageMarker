import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
from .constants import OBJECT_COLOR, BACKGROUND_COLOR, UNCERTAIN_COLOR
from .marker import *
from . import file_manager

class ImageCanvas(ctk.CTkFrame):
    def __init__(self, master, original_image, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self._original_image = original_image
        self._image_size = original_image.size

        # Zoom and translation control variables
        self._zoom_factor = 1
        self._translation_x = 0
        self._translation_y = 0
        self._last_x = 0
        self._last_y = 0

        # Marker setup
        self._obj_marker_list = []
        self._bg_marker_list = []
        self._uncer_marker_list = []
        self._brush_size = 5
        self.set_obj_marker()

        # Frame setup
        self._config_grid()
        self._config_canvas()
        self._config_bindings()
    
    def _config_grid(self):
        self.rowconfigure(0, weight=2) 
        self.columnconfigure(0, weight=2)
    
    def _config_canvas(self):
        self._canvas = ctk.CTkCanvas(self, bg="black")
        self._canvas.grid(row = 0, column = 0, sticky="nsew", columnspan=2)
        self._painting_image = self._original_image.copy()
        self._displayed_image = ImageTk.PhotoImage(self._painting_image)

        self.image_item = self._canvas.create_image(0, 0, anchor=ctk.NW, image=self._displayed_image)
      
    def _config_bindings(self):
        self._canvas.bind("<Button-1>", self._left_mouse_click)
        self._canvas.bind("<MouseWheel>", self._mouse_wheel)
        self._canvas.bind("<Button-4>", self._scroll)     # Para o Linux (scroll para cima)
        self._canvas.bind("<Button-5>", self._scroll)     # Para o Linux (scroll para baixo)
        
        self._canvas.bind("<ButtonPress-3>", self._start_translation)
        self._canvas.bind("<B3-Motion>", self._right_mouse_click)
    
    def _print_list(self):
        print('[')
        for i in range(0, len(self._obj_marker_list) - 1):
            print(self._obj_marker_list[i], end = ', ')
        print(self._obj_marker_list[-1], end = ']')
        
        for i in range(0, len(self._bg_marker_list) - 1):
            print(self._bg_marker_list[i], end = ', ')
        print(self._bg_marker_list[-1], end = ']')
        
        for i in range(0, len(self._uncer_marker_list) - 1):
            print(self._uncer_marker_list[i], end = ', ')
        print(self._uncer_marker_list[-1], end = ']')

        print("\n\n")
    
    def save(self):
        file_manager.save_results(
        self._original_image, self._painting_image, self._obj_marker_list, self._bg_marker_list, self._uncer_marker_list)
    
    def load_annotation(self):
        obj_markers, bg_markers, uncer_markers = file_manager.load_annotation_from_file()
        if obj_markers is not None and bg_markers is not None and uncer_markers is not None:
            self._obj_marker_list = obj_markers
            self._bg_marker_list = bg_markers
            self._uncer_marker_list = uncer_markers
            self._update_image()

    def _left_mouse_click(self, event):
        if self._erasing == False:
            self._mark(event)
        else:
            self._remove_marker(event)

    # Drawing event
    def _mark(self, event):
        x = int(event.x / self._zoom_factor) - self._translation_x / self._zoom_factor
        y = int(event.y / self._zoom_factor) - self._translation_y / self._zoom_factor
        self._last_x = x
        self._last_y = y
        if self._current_marker_type == MarkerType.OBJECT:
            self._obj_marker_list.append(Marker(int(x),int(y), self._current_marker_type, self._brush_size))
        elif self._current_marker_type == MarkerType.BACKGROUND:
            self._bg_marker_list.append(Marker(int(x),int(y), self._current_marker_type, self._brush_size))
        else:    
            self._uncer_marker_list.append(Marker(int(x), int(y), self._current_marker_type, self._brush_size))
        self._update_image()
    
    def _place_marker(self,marker):
        paint = ImageDraw.Draw(self._painting_image)
        paint.rectangle((marker.x, marker.y, marker.x + marker.size , marker.y + marker.size), fill=marker.color, width=2)

    def check_collision(self, coords_1, coords_2):
        x_min_1, y_min_1, x_max_1, y_max_1 = coords_1
        x_min_2, y_min_2, x_max_2, y_max_2 = coords_2

        if (x_max_1 >= x_min_2 and x_min_1 <= x_max_2) and (y_max_1 >= y_min_2 and y_min_1 <= y_max_2):
            return True
        else:
            return False
            
    def _remove_marker(self, event):
        click_x = int(event.x / self._zoom_factor) - self._translation_x / self._zoom_factor
        click_y = int(event.y / self._zoom_factor) - self._translation_y / self._zoom_factor
        for obj_marker in self._obj_marker_list:
            collision = self.check_collision(
                [obj_marker.x, obj_marker.y,obj_marker.x + obj_marker.size, obj_marker.y + obj_marker.size],
                [click_x, click_y,click_x + self._brush_size, click_y + self._brush_size]
            )

            if collision:
                self._obj_marker_list.remove(obj_marker)
        
        for bg_marker in self._bg_marker_list:
            collision = self.check_collision(
                [bg_marker.x, bg_marker.y,bg_marker.x + bg_marker.size, bg_marker.y + bg_marker.size],
                [click_x, click_y,click_x + self._brush_size, click_y + self._brush_size ]
            )

            if collision:
                self._bg_marker_list.remove(bg_marker)

        for uncer_marker in self._uncer_marker_list:
            collision = self.check_collision(
                [uncer_marker.x, uncer_marker.y,uncer_marker.x + uncer_marker.size, uncer_marker.y + uncer_marker.size],
                [click_x, click_y,click_x + self._brush_size, click_y + self._brush_size ]
            )

            if collision:
                self._uncer_marker_list.remove(uncer_marker)
        
        
        self._update_image()
    
    def set_obj_marker(self):
        self._current_marker_type = MarkerType.OBJECT
        self._marker_color = OBJECT_COLOR
        self._erasing = False
    
    def set_bg_marker(self):
        self._current_marker_type = MarkerType.BACKGROUND
        self._marker_color = BACKGROUND_COLOR
        self._erasing = False
    
    def set_remove(self):
        self._erasing = True
    
    def set_uncertain_marker(self):
        self._current_marker_type = MarkerType.UNCERTAIN
        self._marker_color = UNCERTAIN_COLOR
        self._erasing = False
    
    def _set_brush_size(self, size):
        self._brush_size = size
    
    # Zoom event on Linux
    def _scroll(self, event):
      if event.num == 4 or event.delta == 120:  # Scroll para cima
        self._zoom_in()
      elif event.num == 5 or event.delta == -120:  # Scroll para baixo
        self._zoom_out()

    # Zoom event on Windows
    def _mouse_wheel(self, event):
        if (event.delta > 0):
            self._zoom_in()
        else:
            self._zoom_out()
            
    def _zoom_in(self):
        if self._zoom_factor < 1.5:
            self._zoom_factor *= 1.5
            self._update_image()

    def _zoom_out(self):
        if self._zoom_factor > 0.2:
            self._zoom_factor /= 1.5
            self._update_image()
    
    def _update_image(self):
        self._painting_image = self._original_image.copy()
        for obj_marker in self._obj_marker_list:
            self._place_marker(obj_marker)
        for bg_marker in self._bg_marker_list:
            self._place_marker(bg_marker)
        for uncer_marker in self._uncer_marker_list:
            self._place_marker(uncer_marker)
        
        zoomed_width = int(self._painting_image.width * self._zoom_factor)
        zoomed_height = int(self._painting_image.height * self._zoom_factor)
        zoomed_image = self._painting_image.resize((zoomed_width, zoomed_height), Image.LANCZOS)
        self._image_size = zoomed_image.size
        self._displayed_image = ImageTk.PhotoImage(zoomed_image)
        self._canvas.itemconfig(self.image_item, image=self._displayed_image)
    
    # Translation event
    def _right_mouse_click(self, event):
        dx = (event.x - self._last_x) / self._zoom_factor
        dy = (event.y - self._last_y) / self._zoom_factor
        self._last_x = event.x
        self._last_y = event.y
        self._translate_image(dx, dy)

    def _start_translation(self, event):
        self._last_x = event.x
        self._last_y = event.y

    def _translate_image(self, dx, dy):
        self._translation_x += dx
        self._translation_y += dy
        self._canvas.move(self.image_item, dx, dy)
