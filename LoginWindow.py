#Please install the following first to ensure all details will show accordingly.
    #1. pip install pillow
    #2. pip install tkinter 
    #3. pip install tkintermapview
    #4. pip install requests

import sqlite3
from tkinter import *
from tkinter import messagebox
from tkintermapview import *
from PIL import Image, ImageTk
from SignUpWindow import signup_window_open
from Frontend import main_window

def login_window_open():
    """Initialize and display the login window"""

# ---------------------------------------------------------------------------- #
#                                    BACKEND                                   #
# ---------------------------------------------------------------------------- #

    def connect_db():
            # Connect to SQLite database
            conn = sqlite3.connect('Accounts.db')
            cursor = conn.cursor()
            # Create table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                password TEXT NOT NULL,
                                email TEXT NOT NULL
                            )''')
            conn.commit()
            return conn
    
    def login_clicked():
        conn = connect_db()
        cursor = conn.cursor()

        username = login_username_entry.get()
        password = login_password_entry.get()

        # Check if the username exists
        find_user = "SELECT * FROM users WHERE username = ?"
        cursor.execute(find_user, [username])
        account_username = cursor.fetchone()
        
        if account_username:
            # Check if the password matches
            find_password = "SELECT * FROM users WHERE username = ? AND password = ?"
            cursor.execute(find_password, [(username), (password)])
            account = cursor.fetchone()
            
            if account:
                messagebox.showinfo("Login Successful", "Welcome, " + login_username_entry.get() + "!")
                login_window.destroy()
                main_window()
            else:
                messagebox.showerror("Login Failed", "Incorrect password.")
                print(f"Login failed for user '{login_username_entry.get()}': Incorrect password.")
        else:
            messagebox.showerror("Login Failed", "Username not found.")
            print(f"Login failed: Username '{login_username_entry.get()}' not found.")

        conn.close()    

    def toggle_password_visibility():
        #Toggle the visibility of the password entry field.

        if show_password_var.get():
            login_password_entry.config(show="")
        else:
            login_password_entry.config(show="*")

    def username_focus(event):
        #Clear the placeholder text in the username entry field when it gains focus.
        if login_username_entry.get() == "Username":
            login_username_entry.delete(0, END)

    def password_focus(event):
        #Clear the placeholder text in the password entry field and mask input when it gains focus.
        if login_password_entry.get() == "Password":
            login_password_entry.delete(0, END)
            login_password_entry.config(show="*")
    
    def username_blur(event):
        #Restore the placeholder text in the username entry field if it is empty when losing focus.
        if login_username_entry.get() == "":
            login_username_entry.insert(0, "Username")

    def password_blur(event):
        #Restore the placeholder text in the password entry field and unmask input if it is empty when losing focus.
        if login_password_entry.get() == "":
            login_password_entry.insert(0, "Password")
            login_password_entry.config(show="")

    def on_enter(event):
        #Change Color of signup button on Hover.
        signup_label.configure(fg="white", font=("Helvetica", 10, "underline",))

    def on_leave(event):
        #Reset color of signup button when not hovered.
        signup_label.configure(fg="black", font=("Helvetica", 10, "underline"))

    def on_click(event):
        #Display Sign up window.
        signup_window_open()

# ---------------------------------------------------------------------------- #
#                                   FRONTEND                                   #
# ---------------------------------------------------------------------------- #

    #Login Window
    login_window = Tk()
    login_window.title("Ride Ease - Login")
    login_window.geometry("925x500+300+200")
    login_window.configure(bg="white")
    login_window.resizable(False, False)
    login_window.iconbitmap("icons/RideEaseLogo.ico") 

    #Login Text variables
    username = StringVar()
    password = StringVar()

    #Logo Image
    login_logo_image_path = "images/welcome_new.png" 
    login_logo_image = Image.open(login_logo_image_path)
    login_logo_image = login_logo_image.resize((340, 190), Image.LANCZOS)
    login_logo_photo_image = ImageTk.PhotoImage(login_logo_image)

    login_image_label = Label(login_window, image=login_logo_photo_image, bg="white")
    login_image_label.place(x=100, y=15)

    #Login Image
    login_image_path = "images/log in.jpg"
    login_image = Image.open(login_image_path)
    login_image = login_image.resize((380, 280), Image.LANCZOS)
    login_photo_image = ImageTk.PhotoImage(login_image)

    image_label = Label(login_window, image=login_photo_image, bg="white")
    image_label.place(x=75, y=175)

    #Login Frame
    login_frame=Frame(login_window, width=350, height=370, bg="#f8c81c")
    login_frame.place(x=530,y=70)

    login_heading=Label(login_frame, text="Login", fg="black", bg="#f8c81c", font=("Helvetica", 30, "bold"))
    login_heading.place(x=125, y=20)

    #Login Username Label
    login_username_label = Label(login_frame, text="Enter your username", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    login_username_label.place(x=72, y=80)

    #Username Entry
    login_username_entry = Entry(login_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11), textvariable=username)
    login_username_entry.place(x=75,y=105)
    login_username_entry.insert(0, "Username")
    Frame(login_frame, width=202, height=1, bg="black").place(x=75,y=125)

    login_username_entry.bind("<FocusIn>", username_focus)
    login_username_entry.bind("<FocusOut>", username_blur)

    #Login Password Label
    login_password_label = Label(login_frame, text="Enter your password", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    login_password_label.place(x=72, y=135)

    #Login Password Entry
    login_password_entry = Entry(login_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11), textvariable=password)
    login_password_entry.place(x=75,y=160)
    login_password_entry.insert(0, "Password")
    Frame(login_frame, width=202, height=1, bg="black").place(x=75,y=180)

    login_password_entry.bind("<FocusIn>", password_focus)
    login_password_entry.bind("<FocusOut>", password_blur)

    #Login Show Password 
    show_password_var = BooleanVar()
    show_password_check = Checkbutton(login_frame, text="Show Password", bg="#f8c81c", font=("Helvetica", 8), variable=show_password_var, command=toggle_password_visibility)
    show_password_check.place(x=167, y=190)

    #Login Button
    login_button = Button(login_frame, width=20, pady=5, text="Login", bg="white", fg="black", font=("Helvetica", 10), border=2, relief=RAISED, command=login_clicked)
    login_button.place(x=92,y=225)

    #SignUp Label Only
    signup_text = Label(login_frame, text="No account yet? ", fg="black", bg="#f8c81c", font=("Helvetica", 9))
    signup_text.place(x=69, y=270)

    #SigUp Label as a Button
    signup_label = Label(login_frame, text="Click here to sign up", fg="black", font=("Helvetica", 9, "underline"), bg="#f8c81c")
    signup_label.place(x=162, y=270)

    signup_label.bind("<Enter>", on_enter)
    signup_label.bind("<Leave>", on_leave)
    signup_label.bind("<Button-1>", on_click)

    #Image reference
    login_window.logo_photo_image = login_logo_photo_image
    login_window.login_photo_image = login_photo_image

    login_window.mainloop()

login_window_open()





