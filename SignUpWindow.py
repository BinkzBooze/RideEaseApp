#Please install the following first to ensure all details will show accordingly.
    #1. pip install pillow

from tkinter import *
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from PIL import Image, ImageTk
import os
import json
import re
import string
from Vehicle_Classes import *
import glob

accounts = "Accounts.json"

def main_page():

    # All color
    main_page_color = "#0f0f0f"
    menu_bar_color = "#ffb700"
    history_bg_color = "#ffec9e"

    main = Tk()
    main.geometry("800x580")
    main.title("RideSafe")
    main.configure(bg=main_page_color)
    main.resizable(False,False)
    main.iconbitmap("icons/RideEaseLogo.ico")

    def report_issue_clicked():
        return

    def history_close():
        for widgets in history_widgets:
            widgets.place_forget()
        clear_main()
        activity_clicked()

    global history_widgets
    history_widgets = []

    def history_clicked():
        
        clear_main()
        main.geometry("800x1080")
        icon_main.place_forget()
        main.configure(bg=history_bg_color)

        history_close_btn = Button(main, image=close_icon, bg=history_bg_color, bd=1, activebackground=history_bg_color,
                                    fg=main_page_color, command=history_close)
        history_close_btn.place(x=750, y=15)
        history_widgets.append(history_close_btn)

        # History Clicked Info
        date = Label(main, text="12 Jun 2024, 8:40 pm", bg=history_bg_color, font=("Helvetica", 12, "bold"), justify="center")
        date.place(x=345, y=20)
        booking_id = Label(main, text="Booking ID: BLABLABLABLA", bg=main_page_color, fg=history_bg_color, font=("Helvetica", 10),
                        anchor=W, padx=288, pady=15)
        booking_id.place(x=50, y=50)
        history_widgets.append(date)
        history_widgets.append(booking_id)

        rating = Label(main, text="Help us improve your Ride Ease experience by rating\nthis ride", bg=history_bg_color, font=("Helvetica", 11))
        rating.place(x=255,y=140)
        history_widgets.append(rating)

        rider_info_box = Label(main, bg=main_page_color, anchor=W, padx=380, pady=35)
        rider_info_box.place(x=50, y=270)
        rider_info = Label(main, text="Rider's Name", bg=main_page_color, fg=history_bg_color, font=("Helvetica", 20))
        rider_info.place(x=160, y=295)
        driver_img = Label(main, image=filler_icon, bg=main_page_color)
        driver_img.place(x=100, y=295)
        history_widgets.append(rider_info_box)
        history_widgets.append(rider_info)
        history_widgets.append(driver_img)

        amount_totalpaid = Label(main, text="TOTAL PAID", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 20, "bold"))
        amount_totalpaid.place(x=60, y=380)
        amount_price = Label(main, text="PHP 96.00", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 20, "bold"))
        amount_price.place(x=620, y=380)
        amount_mop = Label(main, text="(Mode of Payment)", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 14))
        amount_mop.place(x=620, y=420)
        history_widgets.append(amount_totalpaid)
        history_widgets.append(amount_price)
        history_widgets.append(amount_mop)

        # Sample Map
        map = Label(main, image=tk_icon, bg=main_page_color)
        map.place(x=160, y=480)
        history_widgets.append(map)

        add_detail = Label(main, text="Mototaxi (Type of vehicle)", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 14))
        add_detail.place(x=70, y=800)
        add_detail2 = Label(main, text="No. of km * No. of mins.", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 14))
        add_detail2.place(x=570, y=800)
        add_detail_price = Label(main, text="PHP 96.00", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 20, "bold"))
        add_detail_price.place(x=620, y=850)
        add_detail_mop = Label(main, text="(Mode of Payment)", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 14))
        add_detail_mop.place(x=620, y=890)
        history_widgets.append(add_detail)
        history_widgets.append(add_detail2)
        history_widgets.append(add_detail_price)
        history_widgets.append(add_detail_mop)

        pick_up_address = Label(main, text="Pick Up Address", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 14, "bold"))
        pick_up_address.place(x=120,y=850)
        pickup_time = Label(main, text="(Time)", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 11))
        pickup_time.place(x=120,y=880)
        drop_off_address = Label(main, text="Drop off Address", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 14, "bold"))
        drop_off_address.place(x=120, y=920)
        dropoff_time = Label(main, text="(Time)", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 11))
        dropoff_time.place(x=120,y=950)
        history_widgets.append(pick_up_address)
        history_widgets.append(pickup_time)
        history_widgets.append(drop_off_address)
        history_widgets.append(dropoff_time)

        report_issue = Button(main, text="Report an Issue", fg=main_page_color, bg=history_bg_color, font=("Helvetica", 20, "bold"),
                            bd=0, activebackground=history_bg_color, command=report_issue_clicked)
        report_issue.place(x=310, y=970)
        history_widgets.append(report_issue)

    def delete_close_clicked():
        for widgets in delete_list:
            widgets.place_forget()

    def deleteacc():
        main.configure(bg=main_page_color)

        global delete_list
        delete_list = []

        global delete_box, delete_close_icon, delete_box_info, delete_box_gen_info1, delete_box_gen_info2, decision_e

        delete_box = Label(main, bg="light gray", pady=200, padx=322)
        delete_box.place(x=100, y=100)

        delete_box_info = Label(main, text="Delete Account",bg="light gray", fg=main_page_color, font=("Helvetica", 20, "bold"))
        delete_box_info.place(x=330,y=120)

        gen_info1 = "Once deleted, you will not be able to retrieve any of your data, \nincluding ride history, payment details, and preferences."
        delete_box_gen_info1 = Label(main, text=gen_info1, bg="light gray", fg=main_page_color, font=("Helvetica", 16), justify="left")
        delete_box_gen_info1.place(x=130,y=210)

        gen_info2 = "This action is irresversible.\nIf you are sure, please confirm your decision below."
        delete_box_gen_info2 = Label(main, text=gen_info2, bg="light gray", fg=main_page_color, font=("Helvetica", 16), justify="left")
        delete_box_gen_info2.place(x=130,y=340)

        decision_e = Entry(main, bg=menu_bar_color, fg=main_page_color, font=("Helvetica", 16), bd=0, width=20, justify="center")
        decision_e.place(x=310,y=420)
        decision_e.insert(0, "Type 'delete' to proceed\n")

        delete_close_icon = Button(main, image=close_icon, bg="light gray", bd=0,
                                activebackground="light gray", command=delete_close_clicked)
        delete_close_icon.place(x=700, y=120)

        delete_list.append(delete_box)
        delete_list.append(delete_close_icon)
        delete_list.append(delete_box_info)
        delete_list.append(delete_box_gen_info1)
        delete_list.append(delete_box_gen_info2)
        delete_list.append(decision_e)

    def clear_main():
        main.geometry("800x580")
        main.configure(bg=main_page_color)
        icon_main.place(x=x_position, y=y_position)

        pickup_label.place_forget()
        pickup_e.place_forget()
        dropoff_label.place_forget()
        dropoff_e.place_forget()
        pax_label.place_forget()
        pax_e.place_forget()
        booking_book_btn.place_forget()

        profile_name_lb.place_forget()
        profile_e.place_forget()
        profile_email_lb.place_forget()
        profile_email_e.place_forget()
        profile_cont_lb.place_forget()
        profile_cont_e.place_forget()
        log_out_btn.place_forget()
        del_acc_btn.place_forget()

        act_recent_lb.place_forget()
        act_a4.place_forget()
        act_a3.place_forget()
        act_a2.place_forget()
        act_a1.place_forget()
        act_a4_date.place_forget()
        act_a3_date.place_forget()
        act_a2_date.place_forget()
        act_a1_date.place_forget()
        act_a4_price.place_forget()
        act_a3_price.place_forget()
        act_a2_price.place_forget()
        act_a1_price.place_forget()
        act4_icon.place_forget()
        act3_icon.place_forget()
        act2_icon.place_forget()
        act1_icon.place_forget()

    def homepage_clicked():
        clear_main()

    def booking_clicked():

        clear_main()

        pickup_label.place(x=550, y=210)
        pickup_e.place(x=550, y=255)
        dropoff_label.place(x=550, y=280)
        dropoff_e.place(x=550, y=320)
        pax_label.place(x=550, y=350)
        pax_e.place(x=550, y=390)
        booking_book_btn.place(x=550, y=440)

    def profile_clicked():

        clear_main()

        profile_name_lb.place(x=100,y=250)
        profile_e.place(x=220, y=265)
        profile_email_lb.place(x=100,y=300)
        profile_email_e.place(x=220, y=315)
        profile_cont_lb.place(x=100,y=350)
        profile_cont_e.place(x=350, y=365)
        log_out_btn.place(x=100, y=430)
        del_acc_btn.place(x=500, y=430)

    def activity_clicked():
        clear_main()

        act_recent_lb.place(x=100, y=220)
        act_a4.place(x=150,y=265)
        act_a3.place(x=150,y=335)
        act_a2.place(x=150,y=405)
        act_a1.place(x=150,y=475)

        act_a4_date.place(x=100,y=310)
        act_a3_date.place(x=100,y=380)
        act_a2_date.place(x=100,y=450)
        act_a1_date.place(x=100,y=520)

        act_a4_price.place(x=600,y=265)
        act_a3_price.place(x=600,y=345)
        act_a2_price.place(x=600,y=415)
        act_a1_price.place(x=600,y=485)

        act4_icon.place(x=110,y=265)
        act3_icon.place(x=110,y=345)
        act2_icon.place(x=110,y=415)
        act1_icon.place(x=110,y=485)

    def load_image(path):
        if os.path.exists(path):
            return ImageTk.PhotoImage(file=path)
        else:
            print(f"File not found: {path}")
            return None

    # Icons (Logo, Menu Toggle, Home, Booking, Profile, Activity, Close)
    icon_path = "icons/homepage_icon.png"
    icon = Image.open(icon_path).convert("RGBA")

    toggle_icon_path = "icons/toggle_btn_icon.png"
    toggle_icon = load_image(toggle_icon_path)

    home_icon_path = "icons/home_icon.png"
    home_icon = load_image(home_icon_path)

    booking_path = "icons/booking_icon (2).png"
    booking_icon = load_image(booking_path)

    profile_path = "icons/profile_icon.png"
    profile_icon = load_image(profile_path)

    activity_path = "icons/activity_icon.png"
    activity_icon = load_image(activity_path)

    close_path = "icons/close_btn_icon.png"
    close_icon = load_image(close_path)

    car_icon_path = "icons/car.png"
    car_icon = load_image(car_icon_path)
    filler_icon = car_icon

    # Initialize Toggle Button as default(off)
    is_on = False

    # Menu Bar Config
    menu_bar_frame = Frame(main, bg=menu_bar_color, padx=3, pady=4)

    # Mode to indicate which tab (0 for Home, 1 for Booking, 2 for Profile, 3 for Activity)
    global_mode_int = 2 # Indicates its in Booking Tab

    # Button Indicator Function
    def btn_modes(ind_lb, mode_int):

        # Changes all the menu icons to orange then changes the ind_lb to white
        home_btn_ind.config(bg=menu_bar_color)
        booking_btn_ind.config(bg=menu_bar_color)
        profile_btn_ind.config(bg=menu_bar_color)
        activity_btn_ind.config(bg=menu_bar_color)

        ind_lb.config(bg="white")

        if ind_lb == home_btn_ind:
            mode_int = 0
            print ("Home Tab")

        elif ind_lb == booking_btn_ind:
            mode_int = 1
            print ("Booking Tab")

        elif ind_lb == profile_btn_ind:
            mode_int = 2
            print ("Profile Tab")

        elif ind_lb == activity_btn_ind:
            mode_int = 3
            print ("Activity Tab")

        # Global indication for switching tabs
        global global_mode_int
        global_mode_int = mode_int

    # Home Button (Placed in Menu Bar)
    home_btn = Button(menu_bar_frame, image=home_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=lambda: (btn_modes(ind_lb=home_btn_ind, mode_int=0), homepage_clicked()))
    home_btn.place(x=8, y=130, width=30, height=40)

    # Home Button Indicator
    home_btn_ind = Label(menu_bar_frame, bg=menu_bar_color)
    home_btn_ind.place(x=1, y=130, width=3, height=40)

    # Booking Button (Placed in Menu Bar)
    booking_btn = Button(menu_bar_frame, image=booking_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=lambda: (btn_modes(booking_btn_ind, mode_int=1), booking_clicked()))
    booking_btn.place(x=8, y=190, width=30, height=40)

    # Booking Button Indicator
    booking_btn_ind = Label(menu_bar_frame, bg="white")
    booking_btn_ind.place(x=1, y=190, width=3, height=40)

    # Profile Button (Placed in Menu Bar)
    profile_btn = Button(menu_bar_frame, image=profile_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=lambda: (btn_modes(profile_btn_ind, mode_int=2), profile_clicked()))
    profile_btn.place(x=8, y=250, width=30, height=40)

    # Profile Button Indicator
    profile_btn_ind = Label(menu_bar_frame, bg=menu_bar_color)
    profile_btn_ind.place(x=1, y=250, width=3, height=40)

    # Activity Button (Placed in Menu Bar)
    activity_btn = Button(menu_bar_frame, image=activity_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=lambda: (btn_modes(activity_btn_ind, mode_int=3), activity_clicked()))
    activity_btn.place(x=8, y=310, width=30, height=40)

    # Activity Button Indicator
    activity_btn_ind = Label(menu_bar_frame, bg=menu_bar_color)
    activity_btn_ind.place(x=1, y=310, width=3, height=40)

    # Resize Icon
    resize_icon = icon.resize((500, 136), Image.LANCZOS)
    tk_icon = ImageTk.PhotoImage(resize_icon)

    # Icon Placement
    window_width = 800
    window_height = 580
    icon_width = resize_icon.width
    icon_height = resize_icon.height

    x_position = (window_width - icon_width) // 2
    x_position = x_position + 30
    y_position = 30

    icon_main = Label(main, image=tk_icon, borderwidth=0, highlightthickness=0, bg=main_page_color)
    icon_main.place(x=x_position, y=y_position)

    # Pick-up label and entry
    pickup_label = Label(main, text="Pick Up", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))
    pickup_label.place(x=550, y=210)

    pickup_e = Entry(main, width=35)
    pickup_e.place(x=550, y=255)

    # Drop-off label and entry
    dropoff_label = Label(main, text="Drop Off", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))
    dropoff_label.place(x=550, y=280)

    dropoff_e = Entry(main, width=35)
    dropoff_e.place(x=550, y=320)

    # Pax label and entry
    pax_label = Label(main, text="Pax", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))
    pax_label.place(x=550, y=350)

    pax_e = Entry(main, width=35)
    pax_e.place(x=550, y=390)

    # Book Button
    booking_book_btn = Button(main, text="Book", fg=main_page_color, bg=menu_bar_color, font=("Helvetica", 12),
                            bd=0, activebackground=menu_bar_color, padx=85, pady=5)
    booking_book_btn.place(x=550, y=440)

    # Profile
    profile_name_lb = Label(main, text="Name:", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 25))
    profile_e = Entry(main, width=50)
    profile_email_lb = Label(main, text="Email:", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 25))
    profile_email_e = Entry(main, width=50)
    profile_cont_lb = Label(main, text="Mobile Number:", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 25))
    profile_cont_e = Entry(main, width=50)
    log_out_btn = Button(main, text="Log Out", fg=main_page_color, bg=menu_bar_color, font=("Helvetica", 20),
                        activebackground=menu_bar_color)
    del_acc_btn = Button(main, text="Delete Account", fg=main_page_color, bg=menu_bar_color, font=("Helvetica", 20),
                        activebackground=menu_bar_color, command=deleteacc)

    # Activity
    act_recent_lb = Label(main, text="Recent", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))

    act_a4 = Button(main, text="Ride to 'drop off address'", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20),
                    bd=0, activebackground=main_page_color, activeforeground=menu_bar_color, command=lambda: history_clicked())
    act_a4_date = Label(main, text="12 Jun 2024, 20:40", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 15))
    act_a4_price = Label(main, text="PHP96.00", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))
    act4_icon = Label(main, image=car_icon, bg=main_page_color)

    act_a3 = Button(main, text="Ride to 'drop off address'", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20),
                    bd=0, activebackground=main_page_color, activeforeground=menu_bar_color, command=lambda: history_clicked())
    act_a3_date = Label(main, text="12 Jun 2024, 20:40", fg=menu_bar_color, bg=main_page_color, font=("Helvetica, 15"))
    act_a3_price = Label(main, text="PHP96.00", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))
    act3_icon = Label(main, image=car_icon, bg=main_page_color)

    act_a2 = Button(main, text="Ride to 'drop off address'", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20),
                    bd=0, activebackground=main_page_color, activeforeground=menu_bar_color, command=lambda: history_clicked())
    act_a2_date = Label(main, text="12 Jun 2024, 20:40", fg=menu_bar_color, bg=main_page_color, font=("Helvetica, 15"))
    act_a2_price = Label(main, text="PHP96.00", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))
    act2_icon = Label(main, image=car_icon, bg=main_page_color)

    act_a1 = Button(main, text="Ride to 'drop off address'", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20),
                    bd=0, activebackground=main_page_color, activeforeground=menu_bar_color, command=lambda: history_clicked())
    act_a1_date = Label(main, text="12 Jun 2024, 20:40", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 15))
    act_a1_price = Label(main, text="PHP96.00", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))
    act1_icon = Label(main, image=car_icon, bg=main_page_color)

    # Menu Bar Placement
    menu_bar_frame.pack(side=LEFT, fill=Y)
    menu_bar_frame.pack_propagate(False)
    menu_bar_frame.configure(width=50)

    # Toggle Icon Function
    def toggle():

        # All these global variables just shows functionality on toggle
        global is_on, extended_menu, home_name, booking_name, profile_name, activity_name
        is_on = not is_on

        # Toggles to toggle_close_icon and toggle_menu_btn
        if is_on:
            toggle_menu_btn.config(image=close_icon)
            toggle_menu_btn.place(x=8, y=15)
            extended_menu = Label(main, bg=menu_bar_color, padx=100, pady=580)
            extended_menu.place(x=50, y=0)

            # Shows extended names for the icons
            home_name = Button(main, text="HOME", bg=menu_bar_color, fg="black", bd=0, 
                            highlightthickness=0, font=("Helvetica", 20, "bold"),
                            activebackground=menu_bar_color, 
                            command=lambda: (btn_modes(ind_lb=home_btn_ind, mode_int=0), homepage_clicked()))
            home_name.place(x=70, y=130)
            booking_name = Button(main, text="BOOKING", bg=menu_bar_color, fg="black", bd=0, 
                                highlightthickness=0, font=("Helvetica", 20, "bold"),
                                activebackground=menu_bar_color,
                                command=lambda: (btn_modes(booking_btn_ind, mode_int=1), booking_clicked()))
            booking_name.place(x=70, y=190)
            profile_name = Button(main, text="PROFILE", bg=menu_bar_color, fg="black", bd=0, 
                                highlightthickness=0, font=("Helvetica", 20, "bold"),
                                activebackground=menu_bar_color,
                                command=lambda: (btn_modes(profile_btn_ind, mode_int=2), profile_clicked()))
            profile_name.place(x=70, y=250)
            activity_name = Button(main, text="ACTIVITY", bg=menu_bar_color, fg="black", bd=0, 
                                highlightthickness=0, font=("Helvetica", 20, "bold"),
                                activebackground=menu_bar_color,
                                command=lambda: (btn_modes(activity_btn_ind, mode_int=3), activity_clicked()))
            activity_name.place(x=70, y=310)
        else:
            toggle_menu_btn.config(image=toggle_icon)
            toggle_menu_btn.place(x=4, y=10)
            extended_menu.after(1, extended_menu.destroy())

            # Deletes the icon names
            home_name.after(1, home_name.destroy())
            booking_name.after(1, booking_name.destroy())
            profile_name.after(1, profile_name.destroy())
            activity_name.after(1, activity_name.destroy())

    # Toggle Icon Button and Packing (Placed in Menu Bar)
    toggle_menu_btn = Button(menu_bar_frame, image=toggle_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=toggle)
    toggle_menu_btn.place(x=4, y=10)

    main.mainloop()

def booking_tab():
    # Creation of the Class Application
    class RideBookingApp:

        def __init__(self, root):
            self.root = root
            self.root.title("Ride Booking System")
            self.api_key = "AIzaSyDVMXyo9XYUdOBjr9Kv0TLbpQiDVv2lds0" 
            self.root.iconbitmap("icons/RideEaseLogo.ico") 
            self.root.resizable(False,False)

            self.vehicles = {'Car': Car(), 'Van': Van(), 'Motorcycle': Motorcycle()}
            self.bookings = {}
            self.create_widgets()
            self.load_bookings()

            # Ensure bookings are saved when the application closes
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Creation of Widgets
        def create_widgets(self):
            # User Entry
            self.user_label = tk.Label(self.root, text="User:")
            self.user_label.grid(row=0, column=0)
            self.user_entry = tk.Entry(self.root)
            self.user_entry.grid(row=0, column=1)

            # Vehicle Selection
            self.vehicle_label = tk.Label(self.root, text="Vehicle Type:")
            self.vehicle_label.grid(row=1, column=0)
            self.vehicle_var = tk.StringVar(self.root)
            self.vehicle_var.set("Car")
            self.vehicle_menu = tk.OptionMenu(self.root, self.vehicle_var, *self.vehicles.keys())
            self.vehicle_menu.grid(row=1, column=1)

            # Start Location Entry
            self.start_label = tk.Label(self.root, text="Start Location:")
            self.start_label.grid(row=2, column=0)
            self.start_entry = tk.Entry(self.root)
            self.start_entry.grid(row=2, column=1)

            # End Location Entry
            self.end_label = tk.Label(self.root, text="End Location:")
            self.end_label.grid(row=3, column=0)
            self.end_entry = tk.Entry(self.root)
            self.end_entry.grid(row=3, column=1)

            # Distance Entry (Read-only)
            self.distance_label = tk.Label(self.root, text="Distance:")
            self.distance_label.grid(row=4, column=0)
            self.distance_entry = tk.Entry(self.root, state='readonly')
            self.distance_entry.grid(row=4, column=1)

            # Number of Passengers Entry
            self.passengers_label = tk.Label(self.root, text="Number of Passengers:")
            self.passengers_label.grid(row=5, column=0)
            self.passengers_entry = tk.Entry(self.root)
            self.passengers_entry.grid(row=5, column=1)

            # Book Button
            self.book_button = tk.Button(self.root, text="Book Ride", command=self.book_ride)
            self.book_button.grid(row=6, column=0, columnspan=2)

            # Listbox for Bookings
            self.listbox = tk.Listbox(self.root, width=50, height=10)
            self.listbox.grid(row=7, column=0, columnspan=2)
            self.listbox.bind('<Double-Button-1>', self.show_details)

            # Cancel Button
            self.cancel_button = tk.Button(self.root, text="Cancel Booking", command=self.cancel_booking)
            self.cancel_button.grid(row=8, column=0, columnspan=2)

        # Get input from user
        def book_ride(self):
            user = self.user_entry.get()
            vehicle = self.vehicles[self.vehicle_var.get()]
            start_location = self.start_entry.get()
            end_location = self.end_entry.get()
            passengers = self.passengers_entry.get()

            # VALIDATION OF INPUTS

            # Validate if all fields are filled.
            if not user or not start_location or not end_location or not passengers:
                messagebox.showerror("Error", "All fields must be filled.")
                return

            # Check if name inputted is valid.
            if not user.isascii() or not all(c.isalpha() or c in '.- ' for c in user):
                messagebox.showerror("Error", "The user name must only contain ASCII letters, dots, or dashes.")
                return False

            # Calculation of distance between two points using Google Maps API.
            try:
                # Calculate the distance
                km = Booking.get_distance(start_location, end_location, self.api_key)
                self.distance_entry.config(state='normal')
                self.distance_entry.delete(0, tk.END)
                self.distance_entry.insert(0, km)
                self.distance_entry.config(state='readonly')
            except Exception as e:
                messagebox.showerror("Error", "Invalid address or location.")
                return

            # Error if passenger is invalid.
            if not passengers.isnumeric() or int(passengers) == 0:
                messagebox.showerror("Error", "passengers should be non-negative and non-zero integers.")
                return
            
            # Car's recommended capacity is 4, allow up to 6 passengers only.
            elif isinstance(vehicle, Car) and 4 < int(passengers) <= 6:
                if not messagebox.askyesno("Confirmation", "The number of passengers exceeds the car's capacity. Are you sure you want to continue?"):
                    return
            # Van's recommended capacity is 8, allow up to 12 passengers only.
            elif isinstance(vehicle, Van) and 8 < int(passengers) <= 12:
                if not messagebox.askyesno("Confirmation", "The number of passengers exceeds the van's capacity. Are you sure you want to continue?"):
                    return

            # Error if passenger amount is greater than vehicle capacity.
            elif int(passengers) > vehicle.capacity:
                messagebox.showerror("Error", "The selected vehicle does not have enough capacity for the number of passengers.")
                return
            
            # Create a booking.
            booking = Booking(user, vehicle, start_location, end_location, km)
            self.bookings[booking.no] = booking

            # Insert the booking in the list.
            self.listbox.insert(tk.END, f"Booking #{booking.no}: {user}")
            Booking.save_to_file(booking, f"booking_{booking.no}.json")

        # Widget for cancel Booking
        def cancel_booking(self):
            selected = self.listbox.curselection()
            if selected:
                booking_id = int(self.listbox.get(selected).split(':')[0].split('#')[1])

                del self.bookings[booking_id]
                Booking.delete_file(f"booking_{booking_id}.json")
                self.listbox.delete(selected)

        # Widget for showing the full details of the transaction.
        def show_details(self, event):
            selected = self.listbox.curselection()
            if selected:
                booking_id = int(self.listbox.get(selected).split(':')[0].split('#')[1])
                booking = self.bookings[booking_id]

                details_window = tk.Toplevel(self.root)
                details_window.title(f"Booking #{booking.no} Details")
                details_window.configure(background='white')
                details_window.geometry("500x300")
                details_window.iconbitmap("icons/RideEaseLogo.ico")

                receipt_frame = ttk.Frame(details_window, padding="10", relief="solid", borderwidth=1)
                receipt_frame.pack(expand=True, fill='both', padx=10, pady=10)

                ttk.Label(receipt_frame, text="Booking Receipt", font=("Helvetica", 14, "bold"), anchor="center").pack(pady=5)
                ttk.Label(receipt_frame, text=f"\nUser: {booking.user}", anchor="center").pack(fill='x')
                ttk.Label(receipt_frame, text=f"\nVehicle Type: {type(booking.vehicle).__name__}", anchor="center").pack(fill='x')
                ttk.Label(receipt_frame, text=f"\nStart Location: {booking.start_location}", anchor="center").pack(fill='x')
                ttk.Label(receipt_frame, text=f"\nEnd Location: {booking.end_location}", anchor="center").pack(fill='x')
                ttk.Label(receipt_frame, text=f"\nTotal Distance: {booking.km} km", anchor="center").pack(fill='x')
                ttk.Label(receipt_frame, text=f"\nTotal Cost: ₱{booking.cost} ", anchor="center").pack(fill='x')

        def save_bookings(self):
            for no, booking in self.bookings.items():
                filename = f"booking_{no}.json"
                with open(filename, 'w') as f:
                    json.dump(booking.to_dict(), f, indent=4)

        def load_bookings(self):
            for filepath in glob.glob("booking_*.json"):
                with open(filepath, 'r') as f:
                    booking_data = json.load(f)
                    booking = Booking.from_dict(booking_data)
                    self.bookings[booking.no] = booking
                    self.listbox.insert(tk.END, f"Booking #{booking.no}: {booking.user}")

        def on_closing(self):
            self.save_bookings()
            self.root.destroy()

    if __name__ == "__main__":
        root = tk.Tk()
        app = RideBookingApp(root)
        root.mainloop()

   
def login(login_username, login_password, accounts):
    users = load_users_from_file(accounts)
    if login_username in users and users[login_username] == login_password:
        messagebox.showinfo("Login Successful", "Welcome, " + login_username + "!")
        print(f"User '{login_username}' logged in successfully!")
        root.destroy()
        main_page()
        booking_tab()
        
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
        print(f"Login failed for user '{login_username}'")

def toggle_password_visibility():
    if show_password_var.get():
        login_password.config(show="")
    else:
        login_password.config(show="*")

def load_users_from_file(accounts):
    if os.path.exists(accounts):
        with open(accounts, "r") as file:
            return json.load(file)
    else:
        return {}

def save_users_to_file(users, accounts):
    with open(accounts, "w") as file:
        json.dump(users, file)

users = load_users_from_file(accounts)

def validate_username_signup(username):
    if len(username) < 4 or len(username) > 20 or username == "Username":
        return False, "Username must be between 4 and 20 characters"
    if not username.isalnum():
        return False, "Username can only contain alphanumeric characters"
    return True, ""

def contains_alnum_and_special(s):
    has_alnum = any(char.isalnum() for char in s)
    has_special = any(char in string.punctuation for char in s)
    return has_alnum and has_special

def validate_password_signup(password):
    if len(password) < 6 or len(password) > 30 or password == "Password":
        return False, "Password must be between 6 and 30 characters"
    result = contains_alnum_and_special(password)
    if not result:
        return False, "Passwords must contain a mix of letters, numbers, and special characters."
    return True, ""

def validate_email_signup(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email):
        return True, ""
    else:
        return False, "Please enter a valid email address."

def validate_confirmpw_signup(confirm, password):
    if password == confirm:
        return True, ""
    else:
        return False, "Passwords do not match."
    
def gender_option_picked(gender):
    if gender == "-- Select Your Gender --":
        return False, "Please select a gender option before proceeding."
    else:
        return True, ""
    
def terms_and_conditions_checked(terms):
    if terms == 0:
        return False, "Please agree to the terms and conditions before proceeding."
    else:
        return True, ""

def signup(signup_username, signup_password, signup_email, signup_confirm, signup_gender, signup_terms, accounts):
    valid_email, email_msg = validate_email_signup(signup_email)
    valid_username, username_msg = validate_username_signup(signup_username)
    valid_password, password_msg = validate_password_signup(signup_password)
    valid_confirm, confirm_msg = validate_confirmpw_signup(signup_confirm, signup_password)
    valid_gender, gender_msg = gender_option_picked(signup_gender)
    valid_terms, terms_msg = terms_and_conditions_checked(signup_terms)

    if not valid_email:
        messagebox.showerror("Invalid Email Address", email_msg)
        return False
    elif not valid_username:
        messagebox.showerror("Invalid Username", username_msg)
        return False
    elif not valid_password:
        messagebox.showerror("Invalid Password", password_msg)
        return False
    elif not valid_confirm:
        messagebox.showerror("Passwords do not match", confirm_msg)
        return False
    elif not valid_gender:
        messagebox.showerror("Selection Required.", gender_msg)
        return False
    elif not valid_terms:
        messagebox.showerror("Agreement Required", terms_msg)
        return False
    else:
        users[signup_username] = signup_password  # Add new user to the dictionary
        save_users_to_file(users, accounts)  # Save user data to file
        print(f"User '{signup_username}' signed up successfully!")
        messagebox.showinfo("Signup Successful", "Account created successfully!")

current_signup_window = None

def open_signup_window(event=None):
    global current_signup_window
    if current_signup_window is not None:
        return
    
    def signup_clicked():
        email = signup_email_entry.get()
        username = signup_user_entry.get()
        password = signup_password_entry.get()
        confirm = signup_confirm_entry.get()
        gender = signup_gender_var.get()
        terms = terms_var.get()

        if signup(username, password, email, confirm, gender, terms, accounts) == True:
            current_signup_window.destroy()  # Close the signup window after signing up

    current_signup_window = Toplevel(current_signup_window)
    current_signup_window.title("Sign Up")
    current_signup_window.geometry("925x500+300+200")
    current_signup_window.configure(bg="white")
    current_signup_window.resizable(False, False)
    current_signup_window.iconbitmap("icons/RideEaseLogo.ico") 
  
    # Signup Logo Image
    signup_logo_image_path = "images/welcome_new.png" 
    signup_logo_image = Image.open(signup_logo_image_path)
    signup_logo_image = signup_logo_image.resize((340, 190), Image.LANCZOS)
    signup_logo_photo_image = ImageTk.PhotoImage(signup_logo_image)
    
    signup_logo_image_label = Label(current_signup_window, image=signup_logo_photo_image, bg="white")
    signup_logo_image_label.place(x=100, y=15)

    # Reference
    signup_logo_image_label.image = signup_logo_photo_image

    # Signup Image
    signup_image_path = "images/sign up.jpg"
    signup_image = Image.open(signup_image_path)
    signup_image = signup_image.resize((450, 315), Image.LANCZOS)
    signup_photo_image = ImageTk.PhotoImage(signup_image)

    signup_image_label = Label(current_signup_window, image=signup_photo_image, bg="white")
    signup_image_label.place(x=40, y=175)

    # Reference
    signup_image_label.image = signup_photo_image

    # Signup Frame
    signup_frame=Frame(current_signup_window, width=350, height=400, bg="#f8c81c")
    signup_frame.place(x=530, y=70)

    signup_heading=Label(signup_frame, text="Create an Account", fg="black", bg="#f8c81c", font=("Helvetica", 25, "bold"))
    signup_heading.place(x=29, y=20)


    # Email Entry
    signup_email_label = Label(signup_frame, text="Email", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_email_label.place(x=33, y=73)

    signup_email_entry = Entry(signup_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11))
    signup_email_entry.place(x=35, y=95)
    signup_email_entry.insert(0, "Email Address")
    Frame(signup_frame, width=202, height=1, bg="black").place(x=35, y=115)

    def on_signup_email_focus_in(event):
        if signup_email_entry.get() == "Email Address":
            signup_email_entry.delete(0, END)
            signup_email_entry.config(show="")

    def on_signup_email_focus_out(event):
        if signup_email_entry.get() == "":
            signup_email_entry.insert(0, "Email Address")
            signup_email_entry.config(show="")
    
    signup_email_entry.bind("<FocusIn>", on_signup_email_focus_in)
    signup_email_entry.bind("<FocusOut>", on_signup_email_focus_out)

  # Gender Entry
    signup_gender_label = Label(signup_frame, text=" ", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_gender_label.place(x=33, y=243)

    gender_options = ["-- Select Your Gender --" , "Male", "Female", "Rather not say"]
    signup_gender_var = StringVar(signup_frame)
    signup_gender_var.set(gender_options[0])  # set the default value

    signup_gender_dropdown = OptionMenu(signup_frame, signup_gender_var, *gender_options)
    signup_gender_dropdown.config(width=23, fg="#0f0f0f", bg="white", border=0, font=("Helvetica", 10))
    signup_gender_dropdown.place(x=33, y=266)

    Frame(signup_frame, width=190, height=1, bg="black").place(x=35, y=250)

    # Signup Username Entry
    signup_username_label = Label(signup_frame, text="Username", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_username_label.place(x=33, y=117)

    signup_user_entry = Entry(signup_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11))
    signup_user_entry.place(x=35, y=140)
    signup_user_entry.insert(0, "Username")
    Frame(signup_frame, width=202, height=1, bg="black").place(x=35, y=160)

    def on_signup_user_focus_in(event):
        if signup_user_entry.get() == "Username":
            signup_user_entry.delete(0, END)

    def on_signup_user_focus_out(event):
        if signup_user_entry.get() == "":
            signup_user_entry.insert(0, "Username")

    signup_user_entry.bind("<FocusIn>", on_signup_user_focus_in)
    signup_user_entry.bind("<FocusOut>", on_signup_user_focus_out)

    # Signup Password Entry
    signup_password_label = Label(signup_frame, text="Create Password", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_password_label.place(x=33, y=163)

    signup_password_entry = Entry(signup_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11))
    signup_password_entry.place(x=35, y=185)
    signup_password_entry.insert(0, "Password")
    Frame(signup_frame, width=202, height=1, bg="black").place(x=35, y=205)

    def on_signup_password_focus_in(event):
        if signup_password_entry.get() == "Password":
            signup_password_entry.delete(0, END)
            signup_password_entry.config(show="")

    def on_signup_password_focus_out(event):
        if signup_password_entry.get() == "":
            signup_password_entry.insert(0, "Password")
            signup_password_entry.config(show="")
    
    signup_password_entry.bind("<FocusIn>", on_signup_password_focus_in)
    signup_password_entry.bind("<FocusOut>", on_signup_password_focus_out)
    
    # Signup Confirm Password Entry
    signup_confirm_label = Label(signup_frame, text="Confirm Password", fg="black", bg="#f8c81c", font=("Helvetica", 10))
    signup_confirm_label.place(x=33, y=209)

    signup_confirm_entry = Entry(signup_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11))
    signup_confirm_entry.place(x=35, y=230)
    signup_confirm_entry.insert(0, "Password")
    Frame(signup_frame, width=202, height=1, bg="black").place(x=35, y=250)

    def on_signup_confirm_focus_in(event):
        if signup_confirm_entry.get() == "Password":
            signup_confirm_entry.delete(0, END)
            signup_confirm_entry.config(show="")

    def on_signup_confirm_focus_out(event):
        if signup_confirm_entry.get() == "":
            signup_confirm_entry.insert(0, "Password")
            signup_confirm_entry.config(show="")
    
    signup_confirm_entry.bind("<FocusIn>", on_signup_confirm_focus_in)
    signup_confirm_entry.bind("<FocusOut>", on_signup_confirm_focus_out)
    
    # Sign Up Button
    signup_button = Button(signup_frame, width=20, pady=5, text="Sign Up", bg="white", fg="black", font=("Helvetica", 10), border=2, relief=RAISED, command=signup_clicked)
    signup_button.place(x=90, y=340)

   # Privacy Policy and Terms of Use
    terms_var = BooleanVar()
    global terms_check
    terms_check = Checkbutton(signup_frame, text="I agree to the", bg="#f8c81c", font=("Helvetica", 8), variable=terms_var, onvalue=True, offvalue=False)
    terms_check.place(x=20, y=310)

    global terms_label
    terms_label = Label(signup_frame, text="Privacy Policy and Terms of Use", fg="blue", font=("Helvetica", 8, "underline"), bg="#f8c81c", cursor="hand2")
    terms_label.place(x=90, y=312)
    terms_label.bind("<Enter>", on_terms_enter)
    terms_label.bind("<Leave>", on_terms_leave)
    terms_label.bind("<Button-1>", lambda event: show_terms())

    current_signup_window.bind("<Destroy>", lambda event: clear_current_signup_window())

def clear_current_signup_window():
    global current_signup_window
    current_signup_window = None

def on_enter(event):
    signup_label.config(fg="white", font=("Helvetica", 10, "underline",))

def on_leave(event):
    signup_label.config(fg="black", font=("Helvetica", 10, "underline"))

def on_terms_enter(event):
    terms_label.config(fg="blue")

def on_terms_leave(event):
    terms_label.config(fg="black")

def show_terms():
    terms_window = Toplevel(root)
    terms_window.title("Terms and Conditions")
    terms_window.geometry("750x350+388+275")
    terms_window.configure(bg="white", padx=20, pady=20)

    # Set window icon
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
        terms_check.config(state=NORMAL)

    terms_text.bind("<Motion>", enable_checkbox)

# Main window

root = Tk()
root.title("Ride Ease - Login")
root.geometry("925x500+300+200")
root.configure(bg="white")
root.resizable(False, False)
root.iconbitmap("icons/RideEaseLogo.ico") 

# Logo Image
login_logo_image_path = "images/welcome_new.png" 
login_logo_image = Image.open(login_logo_image_path)
login_logo_image = login_logo_image.resize((340, 190), Image.LANCZOS)
login_logo_photo_image = ImageTk.PhotoImage(login_logo_image)

login_image_label = Label(root, image=login_logo_photo_image, bg="white")
login_image_label.place(x=100, y=15)

# Login Image
login_image_path = "images/log in.jpg"
login_image = Image.open(login_image_path)
login_image = login_image.resize((380, 280), Image.LANCZOS)
login_photo_image = ImageTk.PhotoImage(login_image)

image_label = Label(root, image=login_photo_image, bg="white")
image_label.place(x=75, y=175)

# Login
login_frame=Frame(root, width=350, height=370, bg="#f8c81c")
login_frame.place(x=530,y=70)

login_heading=Label(login_frame, text="Login", fg="black", bg="#f8c81c", font=("Helvetica", 30, "bold"))
login_heading.place(x=125, y=20)

# Login Username Label
login_username_label = Label(login_frame, text="Enter your username", fg="black", bg="#f8c81c", font=("Helvetica", 10))
login_username_label.place(x=72, y=80)

# Username Entry
user = Entry(login_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11))
user.place(x=75,y=105)
user.insert(0, "Username")
Frame(login_frame, width=202, height=1, bg="black").place(x=75,y=125)

def on_user_focus_in(event):
    if user.get() == "Username":
        user.delete(0, END)

def on_user_focus_out(event):
    if user.get() == "":
        user.insert(0, "Username")

user.bind("<FocusIn>", on_user_focus_in)
user.bind("<FocusOut>", on_user_focus_out)

# Login Password Label
login_password_label = Label(login_frame, text="Enter your password", fg="black", bg="#f8c81c", font=("Helvetica", 10))
login_password_label.place(x=72, y=135)

# Login Password Entry
global login_password
login_password = Entry(login_frame, width=25, fg="#0f0f0f", border=0, bg="white", font=("Helvetica", 11))
login_password.place(x=75,y=160)
login_password.insert(0, "Password")
Frame(login_frame, width=202, height=1, bg="black").place(x=75,y=180)

# Login Show Password
global show_password_var 
show_password_var = BooleanVar()
show_password_check = Checkbutton(login_frame, text="Show Password", bg="#f8c81c", font=("Helvetica", 8), variable=show_password_var, command=toggle_password_visibility)
show_password_check.place(x=167, y=190)

def on_focus_in(event):
    if login_password.get() == "Password":
        login_password.delete(0, END)
        login_password.config(show="*")

def on_focus_out(event):
    if login_password.get() == "":
        login_password.insert(0, "Password")
        login_password.config(show="")

login_password.bind("<FocusIn>", on_focus_in)
login_password.bind("<FocusOut>", on_focus_out)

# Login Button
def login_clicked():
    username = user.get()
    passwd = login_password.get()
    login(username, passwd, accounts)

login_button = Button(login_frame, width=20, pady=5, text="Login", bg="white", fg="black", font=("Helvetica", 10), border=2, relief=RAISED, command=login_clicked)
login_button.place(x=92,y=225)

# Sign Up Button
signup_text = Label(login_frame, text="No account yet? ", fg="black", bg="#f8c81c", font=("Helvetica", 9))
signup_text.place(x=69, y=270)

signup_label = Label(login_frame, text="Click here to sign up", fg="black", font=("Helvetica", 9, "underline"), bg="#f8c81c")
signup_label.place(x=162, y=270)
signup_label.bind("<Enter>", on_enter)
signup_label.bind("<Leave>", on_leave)
signup_label.bind("<Button-1>", open_signup_window)

# Image reference
root.logo_photo_image = login_logo_photo_image
root.login_photo_image = login_photo_image

root.mainloop()
