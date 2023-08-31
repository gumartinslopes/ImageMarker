import customtkinter as ctk
from scripts.frames.image_frame import ImageFrame
from PIL import Image
app = ctk.CTk()

test_image_path = "CellsDataset/original/1.jpg"
image = Image.open(test_image_path)
app.geometry("1200x600")
app.image_frame = ImageFrame(app, image)
app.image_frame.pack(fill=ctk.BOTH, expand=True)

app.mainloop()  