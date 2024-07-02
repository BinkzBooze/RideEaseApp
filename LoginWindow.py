from tkinter import *
from tkinter import messagebox
import os 
import json
from PIL import Image, ImageTk
from SignUpWindow import signup_window_open

def login_window_open():
    """Initialize and display the login window"""

# ---------------------------------------------------------------------------- #
#                                    BACKEND                                   #
# ---------------------------------------------------------------------------- #

    accounts = "Accounts.json"

    def login(login_username, login_password, accounts):
        #Authenticate the user with the provided username and password.

        users = load_users_from_file(accounts)
        if login_username in users:
            # Access the password from the nested object
            stored_password = users[login_username].get("password", "")
            if login_password == stored_password:
                messagebox.showinfo("Login Successful", "Welcome, " + login_username + "!")
                print(f"User '{login_username}' logged in successfully!")
                login_window.destroy()
                # booking_window_open()  # Uncomment this when you define the function
            else:
                messagebox.showerror("Login Failed", "Invalid password.")
                print(f"Login failed for user '{login_username}': Incorrect password.")
        else:
            messagebox.showerror("Login Failed", "Username does not exist.")
            print(f"Login failed: Username '{login_username}' not found.")

    def load_users_from_file(accounts):
        #Load user accounts from a JSON file

        if os.path.exists(accounts):
            with open(accounts, "r") as file:
                return json.load(file)
        else:
            return {}

    def toggle_password_visibility():
        #Toggle the visibility of the password entry field.

        if show_password_var.get():
            login_password.config(show="")
        else:
            login_password.config(show="*")

    def username_focus(event):
        #Clear the placeholder text in the username entry field when it gains focus.
        if user.get() == "Username":
            user.delete(0, END)

    def password_focus(event):
        #Clear the placeholder text in the password entry field and mask input when it gains focus.
        if login_password.get() == "Password":
            login_password.delete(0, END)
            login_password.config(show="*")
    
    def username_blur(event):
        #Restore the placeholder text in the username entry field if it is empty when losing focus.
        if user.get() == "":
            user.insert(0, "Username")

    def password_blur(event):
        #Restore the placeholder text in the password entry field and unmask input if it is empty when losing focus.
        if login_password.get() == "":
            login_password.insert(0, "Password")
            login_password.config(show="")
    
    def login_clicked():
        #Retrieves the username and password from the entry fields and calls the login function.
        username = user.get()
        passwd = login_password.get()
        login(username, passwd, accounts)

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
    user = Entry(login_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11))
    user.place(x=75,y=105)
    user.insert(0, "Username")
    Frame(login_frame, width=202, height=1, bg="black").place(x=75,y=125)

    user.bind("<FocusIn>", username_focus)
    user.bind("<FocusOut>", username_blur)

    #Login Password Label
    login_password_label = Label(login_frame, text="Enter your password", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    login_password_label.place(x=72, y=135)

    #Login Password Entry
    login_password = Entry(login_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11))
    login_password.place(x=75,y=160)
    login_password.insert(0, "Password")
    Frame(login_frame, width=202, height=1, bg="black").place(x=75,y=180)

    login_password.bind("<FocusIn>", password_focus)
    login_password.bind("<FocusOut>", password_blur)

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





