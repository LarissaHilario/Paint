import customtkinter
from PIL import Image, ImageTk
import cv2
import numpy as np

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("Paint")
root.configure(fg_color="#FFFFFF")
root.geometry('750x600')


drawing_mode = None
start_x, start_y = 0, 0
end_x, end_y = 0, 0
radius = 0
temp_image = None


canvas_image = np.ones((750, 600, 4), dtype=np.uint8) * 255  
cv2.circle(canvas_image, (0, 0), 1, (0, 0, 0, 0), -1)  

def on_button_click(mode):
    global drawing_mode
    drawing_mode = mode

def on_canvas_click(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def on_canvas_drag(event):
    global start_x, start_y, end_x, end_y, radius, temp_image
    
    if drawing_mode is not None:
        end_x, end_y = event.x, event.y
        temp_image = canvas_image.copy()
        if drawing_mode == "line":
            temp_image = canvas_image.copy()
            cv2.line(temp_image, (start_x, start_y), (end_x, end_y), (255, 0, 0, 255), 2) 
        elif drawing_mode == "freehand":
            cv2.line(canvas_image, (start_x, start_y), (end_x, end_y), (0, 0, 255, 255), 2) 
            start_x, start_y = end_x, end_y
        elif drawing_mode == "circle":
            temp_image = canvas_image.copy()
            radius = int(np.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2))
            cv2.circle(temp_image, (start_x, start_y), radius, (0, 255, 0, 255), 2)  
        elif drawing_mode == "square":
            cv2.rectangle(temp_image, (start_x, start_y), (end_x, end_y), (0,255, 0, 255), 2)
            print('mover')
            
        elif drawing_mode == "erase":
            temp_image = canvas_image.copy()
            radius = int(np.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2))
            cv2.circle(temp_image, (start_x, start_y), radius, (255, 255, 255, 0), -1)  
        update_canvas(temp_image)

def on_canvas_release(event):
    global start_x, start_y, end_x, end_y, radius, temp_image
    
    if drawing_mode is not None:
        end_x, end_y = event.x, event.y
       
        if drawing_mode == "line":
          
            cv2.line(canvas_image, (start_x, start_y), (end_x, end_y), (255, 0, 0, 255), 2) 
        elif drawing_mode == "freehand":
            cv2.line(canvas_image, (start_x, start_y), (end_x, end_y), (0, 0, 255, 255), 2) 
            start_x, start_y = end_x, end_y
        elif drawing_mode == "circle":
            
            radius = int(np.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2))
            cv2.circle(canvas_image, (start_x, start_y), radius, (0, 255, 0, 255), 2)  
        
        elif drawing_mode == "square":
            cv2.rectangle(canvas_image, (start_x, start_y), (end_x, end_y), (0,255, 0, 255), 2)
            print('mover')
            
        elif drawing_mode == "erase":
            
            radius = int(np.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2))
            cv2.circle(canvas_image, (start_x, start_y), radius, (255, 255, 255, 0), -1)  


    update_canvas()

def update_canvas(temp_image=None):
    if temp_image is None:
        temp_image = canvas_image

    photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(temp_image, cv2.COLOR_BGRA2RGBA)))
    canvas.itemconfig(canvas.canvas_item, image=photo)
    canvas.tk_img = photo

frame_buttons = customtkinter.CTkFrame(root, bg="white")
frame_buttons.place(x=10, y=10)


buttons = [
    {"mode": "line", "image_path": "Paint/images/LineaRecta.jpeg", "text": "Línea Recta"},
    {"mode": "freehand", "image_path": "Paint/images/LineaMano.jpeg", "text": "Línea a mano"},
    {"mode": "circle", "image_path": "Paint/images/Circulo.jpeg", "text": "Círculo"},
    {"mode": "square", "image_path": "Paint/images/Cuadrado.jpeg", "text": "Cuadrado"},
    {"mode": "erase", "image_path": "Paint/images/Borrador.jpeg", "text": "Borrar"}
]

for i, button_info in enumerate(buttons):
    img = customtkinter.CTkImage(light_image=Image.open(button_info["image_path"]), size=(50, 50))
    button = customtkinter.CTkButton(frame_buttons, image=img, fg_color="#FFFFFF", text=button_info["text"], text_color="#000", hover_color="#FFF")
    button.grid(row=i, column=0, pady=5)
    button.configure(command=lambda mode=button_info["mode"]: on_button_click(mode))


canvas = customtkinter.CTkCanvas(root, bg="white", width=750, height=600)
canvas.place(x=100, y=10)
canvas.tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(canvas_image, cv2.COLOR_BGRA2RGBA)))
canvas.canvas_item = canvas.create_image(0, 0, anchor="nw", image=canvas.tk_img)
canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<B1-Motion>", on_canvas_drag)
canvas.bind("<ButtonRelease-1>", on_canvas_release) 
root.mainloop()
