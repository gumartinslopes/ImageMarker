import os
from tkinter import filedialog, messagebox
from PIL import Image
from .marker import *

def open_image(filepath):
    '''Opens an input image and returns a PIL Image object.'''
    try:
        img = Image.open(filepath)
        return img
    except Exception as e:
        messagebox.showerror("Image opening error", "An error ocurred while opening the image. Please, try again.")
        return None

def read_file_path():
    '''Obtains and returns a file name string.'''
    filepath = filedialog.askopenfilename()
    return filepath

def _save_annotation(file_obj, marker_list, type_name):
    '''Auxiliar funtion to save the annotations on the respective file'''
    file_obj.write(type_name + '\n')
    for marker in marker_list:
            file_obj.write(f'{marker.x},{marker.y},{marker.size}\n')

def _save_annotation_files(filepath, obj_markers, bg_markers, uncer_markers):
    '''Saves all the annotations on the output files.''' 

    with open(filepath + "_all_annotation.txt", "w") as all_annotation_file:
        _save_annotation(all_annotation_file, obj_markers, "obj")
        _save_annotation(all_annotation_file, bg_markers, "bg")
        _save_annotation(all_annotation_file, uncer_markers, "uncer")
    # saves only object annotation
    with open(filepath + "_obj_annotation.txt", "w") as obj_file:
        _save_annotation(obj_file, obj_markers, "obj")
    
    # saves only background annotation
    with open(filepath + "_bg_annotation.txt", "w") as bg_file:
        _save_annotation(bg_file, bg_markers, "bg")
        
    # saves only object and uncertain annotation
    with open(filepath + "_obj_uncer_annotation.txt", "w") as ob_uncer_file:
        _save_annotation(ob_uncer_file, obj_markers, "obj")
        _save_annotation(ob_uncer_file, uncer_markers, "uncer")
    
    # saves only uncertain annotation
    with open(filepath + "_uncer_annotation.txt", "w") as uncer_file:
        _save_annotation(uncer_file, uncer_markers, "uncer")

def load_annotation_from_file():
    '''Loads the annotation coordinates from the output files.'''
    filepath = read_file_path()
    types = [MarkerType.OBJECT, MarkerType.BACKGROUND, MarkerType.UNCERTAIN]
    obj_markers = []
    bg_markers = []
    uncer_markers = []
    all_markers = [obj_markers, bg_markers, uncer_markers]
    type_index = 0 
    try: 
        markers_file = open(filepath, "r")
        for curr_line in markers_file:
            curr_line = curr_line.replace("\n", "")
            if curr_line == "obj":
                type_index = 0
            elif curr_line == "bg":
                type_index = 1
            elif curr_line == "uncer":
                type_index = 2
            else:
                marker_infos = curr_line.split(',')
                all_markers[type_index].append(Marker(float(marker_infos[0]),float(marker_infos[1]), types[type_index], float(marker_infos[2])))
        return obj_markers, bg_markers, uncer_markers
    
    except Exception as e:
        messagebox.showerror("Annotation opening error", "An error ocurred while opening the annotation. Please, try again.")
        return None, None, None

def save_results(original_img, painted_img, obj_markers, bg_markers, uncer_markers):
    ''' Main output saving function'''
    save_filepath = filedialog.asksaveasfilename()
    if save_filepath != "":
        name_split = save_filepath.rsplit('.', 1) 
        no_ext_filepath = name_split[0]
        original_img.save(no_ext_filepath + "_original.jpg")
        painted_img.save(no_ext_filepath + "_marked.jpg")
        _save_annotation_files(no_ext_filepath, obj_markers, bg_markers, uncer_markers)
    else:
        messagebox.showerror("Result saving error", "The file name can't be empty")