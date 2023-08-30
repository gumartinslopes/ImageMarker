import customtkinter as ctk
from scripts.frames.image_frame import ImageFrame

app = ctk.CTk()
test_image_path = "CellsDataset/original/1.jpg"
app.geometry("1200x600")
app.image_frame = ImageFrame(app, test_image_path)
app.image_frame.pack(fill=ctk.BOTH, expand=True)
app.mainloop()  