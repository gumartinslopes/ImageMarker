import tkinter as tk

def botao_clicado():
    print("Botão foi clicado!")

root = tk.Tk()
root.title("Botão em um Canvas")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

button = tk.Button(canvas, text="Clique em mim", command=botao_clicado)
canvas.create_window(200, 150, window=button)

root.mainloop()
