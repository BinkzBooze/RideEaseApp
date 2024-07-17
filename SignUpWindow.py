import sqlite3
import re
import string

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.scrolledtext import ScrolledText

from DatabaseConnection import *

current_signup_window = None

def signup_window_open(event=None):
    """Initialize and display the sign up window"""

    # ---------------------------------------------------------------------------- #
    #                                    BACKEND                                   #
    # ---------------------------------------------------------------------------- #
    
    global current_signup_window
    if current_signup_window is not None:
        return

    def signup_clicked(event):
        #Validates signup information and creates a new user account if valid.
        valid_email, email_msg = validate_email_signup(signup_email_entry.get())
        valid_username, username_msg = validate_username_signup(signup_user_entry.get())
        valid_password, password_msg = validate_password_signup(signup_password_entry.get())
        valid_confirm, confirm_msg = validate_confirmpw_signup(signup_confirm_entry.get(), signup_password_entry.get())
        valid_gender, gender_msg = gender_option_picked(signup_gender_var.get())
        valid_terms, terms_msg = terms_and_conditions_checked(terms_var.get())

        if not valid_email:
            messagebox.showerror("Invalid Email Address", email_msg, parent=current_signup_window)
            return False
        elif not valid_username:
            messagebox.showerror("Invalid Username", username_msg, parent=current_signup_window)
            return False
        elif not valid_password:
            messagebox.showerror("Invalid Password", password_msg, parent=current_signup_window)
            return False
        elif not valid_confirm:
            messagebox.showerror("Passwords do not match", confirm_msg, parent=current_signup_window)
            return False
        elif not valid_gender:
            messagebox.showerror("Selection Required.", gender_msg, parent=current_signup_window)
            return False
        elif not valid_terms:
            messagebox.showerror("Agreement Required", terms_msg, parent=current_signup_window)
            return False
        else:
            username = signup_user_entry.get().strip()
            password = signup_password_entry.get().strip()
            email = signup_email_entry.get().strip()

            conn = connect_db()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                               (username, password, email))
                conn.commit()
                print(f"User '{username}' signed up successfully!")
                messagebox.showinfo("Signup Successful", "Account created successfully!", parent=current_signup_window)
                current_signup_window.destroy()  # Close the signup window after signing up
            except sqlite3.IntegrityError:
                messagebox.showerror("Username Taken", "This username is already taken. Please choose another.", parent=current_signup_window)
            finally:
                conn.close()

    def validate_username_signup(username):
        #Validates the username for signup.
        if len(str(username)) < 4 or len(str(username)) > 20 or username == "Username":
            return False, "Username must be between 4 and 20 characters"
        if not str(username).isalnum():
            return False, "Username can only contain alphanumeric characters"
        return True, ""

    def contains_alnum_and_special(password):
        #Check if a string contains both alphanumeric and special characters.
        has_alnum = any(char.isalnum() for char in str(password))
        has_special = any(char in string.punctuation for char in str(password))
        return has_alnum and has_special

    def validate_password_signup(password):
        #Validates the password for signup.
        if len(str(password)) < 6 or len(str(password)) > 30 or password == "Password":
            return False, "Password must be between 6 and 30 characters"
        result = contains_alnum_and_special(password)
        if not result:
            return False, "Passwords must contain a mix of letters, numbers, and special characters."
        return True, ""

    def validate_email_signup(email):
        #Validates the email address for signup.
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, str(email)):
            return True, ""
        else:
            return False, "Please enter a valid email address."

    def validate_confirmpw_signup(confirm, password):
        #Checks if the confirm password matches the initial password.
        if password == confirm:
            return True, ""
        else:
            return False, "Passwords do not match."
        
    def gender_option_picked(gender):
        #Verifies if the user picks an option.
        if gender == "-- Select Your Gender --":
            return False, "Please select a gender option before proceeding."
        else:
            return True, ""
        
    def terms_and_conditions_checked(terms):
        #Verifies if the user agrees to the terms and conditions.
        if terms == 0:
            return False, "Please agree to the terms and conditions before proceeding."
        else:
            return True, ""

    def on_signup_email_focus_in(event):
        #Clear the placeholder text in the email entry field when it gains focus.
        if signup_email_entry.get() == "Email Address":
            signup_email_entry.delete(0, END)
            signup_email_entry.config(show="")

    def on_signup_email_focus_out(event):
        #Restore the placeholder text in the email entry field if it is empty when losing focus.
        if signup_email_entry.get() == "":
            signup_email_entry.insert(0, "Email Address")
            signup_email_entry.config(show="")

    def on_signup_user_focus_in(event):
        #Clear the placeholder text in the username entry field when it gains focus.
        if signup_user_entry.get() == "Username":
            signup_user_entry.delete(0, END)

    def on_signup_user_focus_out(event):
        #Restore the placeholder text in the username entry field if it is empty when losing focus.
        if signup_user_entry.get() == "":
            signup_user_entry.insert(0, "Username")

    def on_signup_password_focus_in(event):
        #Clear the placeholder text in the password entry field when it gains focus.
        if signup_password_entry.get() == "Password":
            signup_password_entry.delete(0, END)
            signup_password_entry.config(show="")

    def on_signup_password_focus_out(event):
        #Restore the placeholder text in the password entry field if it is empty when losing focus.
        if signup_password_entry.get() == "":
            signup_password_entry.insert(0, "Password")
            signup_password_entry.config(show="")

    def on_signup_confirm_focus_in(event):
        #Clear the placeholder text in the confirm password entry field when it gains focus.
        if signup_confirm_entry.get() == "Password":
            signup_confirm_entry.delete(0, END)
            signup_confirm_entry.config(show="")

    def on_signup_confirm_focus_out(event):
        #Restore the placeholder text in the confirm password entry field if it is empty when losing focus.
        if signup_confirm_entry.get() == "":
            signup_confirm_entry.insert(0, "Password")
            signup_confirm_entry.config(show="")

    def on_terms_enter(event):
        #Change Color of "terms and conditions" button on Hover.
        terms_label.config(fg="blue")

    def on_terms_leave(event):
        #Reset color of "terms and conditions" button when not hovered.
        terms_label.config(fg="black")

    def show_terms():
        #Window for terms and conditions
        terms_window = Toplevel(current_signup_window)
        terms_window.title("Terms and Conditions")
        terms_window.geometry("750x350+388+275")
        terms_window.configure(bg="white", padx=20, pady=20)
        terms_window.iconbitmap("icons/RideEaseLogo.ico") 

        terms_heading = Label(terms_window, text="Terms and Conditions", font=("Helvetica", 25, "bold"), bg="white", fg="black")
        terms_heading.pack(pady=10)
        terms_text = ScrolledText(terms_window, wrap=WORD, bg="white", fg="black", font=("Helvetica", 10))
        terms_text.pack(expand=1, fill=BOTH, padx=10, pady=10)
        terms_text.insert(END, """Privacy Policy

    Personal Information: We collect personal information (such as usernames and email addresses) when users register for an account on our Ride Booking System. This information is used solely for the purpose of providing and improving our service.

    Data Security: We implement a variety of security measures to maintain the safety of your personal information. Your personal information is contained behind secured networks and is only accessible by a limited number of persons who have special access rights to such systems, and are required to keep the information confidential.

    Third Parties: We do not sell, trade, or otherwise transfer to outside parties your personally identifiable information unless we provide users with advance notice.

    Consent: By using our site, you consent to our Privacy Policy.

    Terms of Use

    Acceptance of Terms: By accessing and using our Ride Booking System, you accept and agree to be bound by the terms and provision of the Terms of Use.

    Use of the Service: You agree to use the service for its intended purpose and not for any illicit purposes including, but not limited to, the reverse engineering of the site and/or its processes and the inclusion of such processes or services in a derivative service.

    Account Responsibilities: Users are responsible for maintaining the confidentiality of their login credentials, and are fully responsible for all activities that occur under their account.

    Changes to Terms: We reserve the right to modify these Terms of Use at any time. Your decision to continue to visit and make use of the site after such changes have been made constitutes your formal acceptance of the new Terms of Use.""")
        bold_words = [
            "Privacy Policy", "Personal Information", "Data Security",
            "Third Parties", "Consent", "Terms of Use",
            "Acceptance of Terms", "Use of the Service",
            "Account Responsibilities", "Changes to Terms"
        ]
        for word in bold_words:
            start_index = "1.0"
            while True:
                start_index = terms_text.search(word, start_index, stopindex=END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                terms_text.tag_add("Bold", start_index, end_index)
                start_index = end_index
        terms_text.tag_configure("Bold", font=("Helvetica", 10, "bold"))
        terms_text.config(state=DISABLED)

        def enable_checkbox(event):
            """Enable the checkbox if the user has scrolled to the bottom of the terms_text."""
            # Get the scrollbar position
            scrollbar_pos = terms_text.yview()
            
            # Check if the scrollbar is at the bottom (close to 1.0)
            if scrollbar_pos[1] == 1.0:
                terms_check.config(state=NORMAL)

        terms_text.bind("<MouseWheel>", enable_checkbox)

    def clear_current_signup_window():
        global current_signup_window
        current_signup_window = None

    # ---------------------------------------------------------------------------- #
    #                                   FRONTEND                                   #
    # ---------------------------------------------------------------------------- #

    #Signup Window
    current_signup_window = Toplevel(current_signup_window)
    current_signup_window.title("Ride Ease - Sign Up")
    current_signup_window.geometry("925x500+300+200")
    current_signup_window.configure(bg="white")
    current_signup_window.resizable(False, False)
    current_signup_window.iconbitmap("icons/RideEaseLogo.ico") 
    current_signup_window.bind("<Destroy>", lambda event: clear_current_signup_window())
    current_signup_window.lift()

    #SignUp Variables
    username = StringVar()
    email = StringVar()
    password = StringVar()
    confirm_password = StringVar()

    #Signup Logo Image
    signup_logo_image_path = "images/welcome_new.png" 
    signup_logo_image = Image.open(signup_logo_image_path)
    signup_logo_image = signup_logo_image.resize((340, 190), Image.LANCZOS)
    signup_logo_photo_image = ImageTk.PhotoImage(signup_logo_image)
    
    signup_logo_image_label = Label(current_signup_window, image=signup_logo_photo_image, bg="white")
    signup_logo_image_label.place(x=100, y=15)
    signup_logo_image_label.image = signup_logo_photo_image

    #Signup Image
    signup_image_path = "images/sign up.jpg"
    signup_image = Image.open(signup_image_path)
    signup_image = signup_image.resize((450, 315), Image.LANCZOS)
    signup_photo_image = ImageTk.PhotoImage(signup_image)

    signup_image_label = Label(current_signup_window, image=signup_photo_image, bg="white")
    signup_image_label.place(x=40, y=175)
    signup_image_label.image = signup_photo_image

    #Signup Frame
    global signup_frame
    signup_frame=Frame(current_signup_window, width=350, height=400, bg="#f8c81c")
    signup_frame.place(x=530, y=70)

    signup_heading=Label(signup_frame, text="Create an Account", fg="black", bg="#f8c81c", font=("Helvetica", 25, "bold"))
    signup_heading.place(x=29, y=20)

    #Email Entry
    signup_email_label = Label(signup_frame, text="Email", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_email_label.place(x=33, y=73)

    signup_email_entry = Entry(signup_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11), textvariable = email)
    signup_email_entry.place(x=35, y=95)
    signup_email_entry.insert(0, "Email Address")
    Frame(signup_frame, width=202, height=1, bg="black").place(x=35, y=115)

    signup_email_entry.bind("<FocusIn>", on_signup_email_focus_in)
    signup_email_entry.bind("<FocusOut>", on_signup_email_focus_out)

    #Signup Username Entry
    signup_username_label = Label(signup_frame, text="Username", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_username_label.place(x=33, y=117)

    signup_user_entry = Entry(signup_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11), textvariable=username)
    signup_user_entry.place(x=35, y=140)
    signup_user_entry.insert(0, "Username")
    Frame(signup_frame, width=202, height=1, bg="black").place(x=35, y=160)

    signup_user_entry.bind("<FocusIn>", on_signup_user_focus_in)
    signup_user_entry.bind("<FocusOut>", on_signup_user_focus_out)

    # Signup Password Entry
    signup_password_label = Label(signup_frame, text="Create Password", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_password_label.place(x=33, y=163)

    signup_password_entry = Entry(signup_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11), textvariable=password)
    signup_password_entry.place(x=35, y=185)
    signup_password_entry.insert(0, "Password")
    Frame(signup_frame, width=202, height=1, bg="black").place(x=35, y=205)

    signup_password_entry.bind("<FocusIn>", on_signup_password_focus_in)
    signup_password_entry.bind("<FocusOut>", on_signup_password_focus_out)

    # Signup Confirm Password Entry
    signup_confirm_label = Label(signup_frame, text="Confirm Password", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_confirm_label.place(x=33, y=209)

    signup_confirm_entry = Entry(signup_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11), textvariable=confirm_password)
    signup_confirm_entry.place(x=35, y=230)
    signup_confirm_entry.insert(0, "Password")
    Frame(signup_frame, width=202, height=1, bg="black").place(x=35, y=250)

    signup_confirm_entry.bind("<FocusIn>", on_signup_confirm_focus_in)
    signup_confirm_entry.bind("<FocusOut>", on_signup_confirm_focus_out)

    #Gender Entry
    signup_gender_label = Label(signup_frame, text=" ", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_gender_label.place(x=33, y=243)

    gender_options = ["-- Select Your Gender --" , "Male", "Female", "Rather not say"]
    signup_gender_var = StringVar(signup_frame)
    signup_gender_var.set(gender_options[0])  # set the default value

    signup_gender_dropdown = OptionMenu(signup_frame, signup_gender_var, *gender_options)
    signup_gender_dropdown.config(width=23, fg="#0f0f0f", bg="white", border=0, font=("Helvetica", 10))
    signup_gender_dropdown.place(x=33, y=266)
    Frame(signup_frame, width=190, height=1, bg="black").place(x=35, y=250)

    #Sign Up Button
    signup_button = Button(signup_frame, width=20, pady=5, text="Sign Up", bg="white", fg="black", font=("Helvetica", 10), border=2, relief=RAISED, command=signup_clicked)
    signup_button.place(x=90, y=340)

    # Privacy Policy and Terms of Use
    terms_var = BooleanVar()
    terms_check = Checkbutton(signup_frame, text="I agree to the", bg="#f8c81c", font=("Helvetica", 8), variable=terms_var, onvalue=True, offvalue=False)
    terms_check.place(x=20, y=310)
    terms_check.config(state=DISABLED)

    terms_label = Label(signup_frame, text="Privacy Policy and Terms of Use", fg="blue", font=("Helvetica", 8, "underline"), bg="#f8c81c", cursor="hand2")
    terms_label.place(x=90, y=312)
    terms_label.bind("<Enter>", on_terms_enter)
    terms_label.bind("<Leave>", on_terms_leave)
    terms_label.bind("<Button-1>", lambda event: show_terms())

    current_signup_window.mainloop()
