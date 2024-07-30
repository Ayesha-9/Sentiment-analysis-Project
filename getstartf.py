from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

def open_login_page():
    try:
        subprocess.run(["python", "E:/NFUL- Project SA-ml/loginpgf.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to open login page: {e}")

def get_resized_image(path, screen_width, screen_height):
    image = Image.open(path)
    image = image.resize((screen_width, screen_height), Image.LANCZOS)
    return ImageTk.PhotoImage(image)

root = Tk()
root.title("Getting Started Form")

# Setting the window to full screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Setting the background color
root.configure(bg="sky blue")




# Creating a photoimage object to use image
photo = get_resized_image(r"E:\NFUL- Project SA-ml\img3.png", screen_width, screen_height)

# Label with image
label = Label(root, image=photo, borderwidth=0)
label.pack(side=TOP, pady=0)

# Get Started button
but = Button(root, text="Get Started", command=open_login_page, font=('Helvetica', 16, 'bold'), bg='dark red', fg='white', padx=15, pady=10)
but.place(relx=0.7, rely=0.8, anchor=CENTER)

root.mainloop()
