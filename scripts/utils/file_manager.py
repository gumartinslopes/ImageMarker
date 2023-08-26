from tkinter import filedialog

def read_file_path():
    filepath = filedialog.askopenfilename()
    return filepath