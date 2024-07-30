from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import mysql.connector
import string
import secrets

root = Tk()
root.title("Login Form")

# Global variables for Entry widgets
usn = StringVar()
pas = StringVar()
n1Box = None
new_pwd_box = None

# Function to connect to the MySQL database
def connect_to_database():
    try:
        # Change these values with your MySQL database connection details
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="login"
        )
        return mydb
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

new_pwd_box = None
new_pwd_label = None

def forgot_password():
    global new_pwd_box, new_pwd_label, n1Box, usn, pas
    
    def update_password(username, new_pwd):
        try:
            mydb = connect_to_database()
            mycursor = mydb.cursor()
            query = "UPDATE student SET pwd = %s WHERE username = %s"
            mycursor.execute(query, (new_pwd, username))
            mydb.commit()
            messagebox.showinfo('Message title', 'Password updated successfully')
        except Exception as e:
            print(e)
            messagebox.showerror('Error', 'Password update failed')

    username = n1Box.get()
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(12))
  
    global new_pwd_label, new_pwd_box
    if new_pwd_label:
        new_pwd_label['text'] = "Your New Password is:"
    else:
        new_pwd_label = Label(frame, text="Your New Password is:", bg='#0D197D', width='20', fg='white', font=('Helvetica', 12, 'bold'))
        new_pwd_label.pack(pady=5)

    if new_pwd_box:
        new_pwd_box.destroy()
    new_pwd_box = Entry(frame, bg='white' ,width='16') 
    new_pwd_box.pack(pady=5)
    new_pwd_box.insert(0, password)

    # Call update_password only after displaying the new password
    update_password(username, password)
    messagebox.showinfo('New Password', f'Your new password is: {password}')

def open_mainpg(root):
    # Create and open the main window
    subprocess.run(["python", r"E:/NFUL- Project SA-ml/mainpg.py"])

def log():
    user = n1Box.get()
    pa = n2Box.get()
    if user == "" or pa == "":
        messagebox.showinfo('Message title', 'please enter username and password')
    else:
        try:
            mydb = connect_to_database()
            mycursor = mydb.cursor()
            query = "SELECT * FROM student WHERE username = %s"
            mycursor.execute(query, (user,))
            result = mycursor.fetchone()
            if result:
                if pa == result[1]:  # Check if the password matches
                    messagebox.showinfo('Message title', 'Login successful')
                    open_mainpg(root)
                else:
                    messagebox.showinfo('Message title', 'Login unsuccessful')
            else:
                messagebox.showinfo('Message title', 'User not found')
            mycursor.close()
            mydb.close()
        except Exception as e:
            print(e)
            messagebox.showerror('Error', 'Login failed')

def qit():
    res = messagebox.askquestion('Message title', 'Do you want to quit?')
    if res == 'yes':
        root.destroy()

def reset():
    usn.set("")
    pas.set("")

# Load and set the background image
bg_image = Image.open(r"E:\NFUL- Project SA-ml\img3.png")
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Create a canvas to enable transparency effect
canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.place(relx=0, rely=0)

# Add background image to the canvas
canvas.create_image(0, 0, image=bg_photo, anchor=NW)

# Create a frame with a transparent effect
frame = Frame(canvas, bg='#87CEFA', width=700)
frame.place(relx=0.45, rely=0.54, anchor=CENTER, width=400)

# Create an oval "LOGIN" area
oval_canvas = Canvas(frame, width=300, height=100, bg='#87CEFA', highlightthickness=0)
oval_canvas.pack(pady=10)
oval_canvas.create_oval(10, 10, 280, 80, fill='#D11820', outline='#D11820')
oval_canvas.create_text(150, 50, text='LOGIN', font=('Helvetica', 30, 'bold'), fill='white')

# Load and place a user icon below the oval, making it larger
user_icon = Image.open(r"E:\NFUL- Project SA-ml\user_icon.png")  # Make sure this path is correct
user_icon = user_icon.resize((120, 120), Image.LANCZOS)
user_icon_photo = ImageTk.PhotoImage(user_icon)
user_icon_label = Label(frame, image=user_icon_photo, bg='#87CEFA')
user_icon_label.pack(pady=5)

n1Label = Label(frame, text="Enter your Username:", bg='#E1BBE5', font=('Helvetica', 14))
n1Label.pack(pady=5)

# Create a canvas for the username entry line
username_canvas = Canvas(frame, width=200, height=30, bg='white', highlightthickness=0)
username_canvas.pack(pady=5)
n1Box = Entry(username_canvas, textvar=usn, bg='white', font=('Helvetica', 14), relief=FLAT, highlightthickness=0, width=16)
n1Box.pack(side=LEFT, padx=5)
username_canvas.create_line(0, 29, 100, 29, fill='black')

n2Label = Label(frame, text="Enter your Password:", bg='#E1BBE5', font=('Helvetica', 14))
n2Label.pack(pady=5)

# Create a canvas for the password entry line
password_canvas = Canvas(frame, width=200, height=30, bg='white', highlightthickness=0)
password_canvas.pack(pady=5)
n2Box = Entry(password_canvas, textvar=pas, show="*", bg='white', font=('Helvetica', 14), relief=FLAT, highlightthickness=0, width=16)
n2Box.pack(side=LEFT, padx=5)
password_canvas.create_line(0, 29, 100, 29, fill='black')

but = Button(frame, text="Login Now", command=log, bg='green', fg='white', width=15, font=('Helvetica', 16))
but.pack(pady=5)

# Create a frame to hold the three buttons side by side
button_frame = Frame(frame, bg=frame['bg'])
button_frame.pack(pady=5)

forgot_pwd_button = Button(button_frame, text="Forgot Password", command=forgot_password, bg='white', font=('Helvetica', 12))
forgot_pwd_button.grid(row=0, column=0, padx=5)

but1 = Button(button_frame, text="Quit", command=qit, bg='white', font=('Helvetica', 12))
but1.grid(row=0, column=1, padx=5)

but2 = Button(button_frame, text="Reset", command=reset, bg='white', font=('Helvetica', 12))
but2.grid(row=0, column=2, padx=5)

# Set background color for the window
root.configure(bg="sky blue")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

root.mainloop()
