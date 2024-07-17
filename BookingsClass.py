import requests
import os
from datetime import datetime

from tkinter import *
from tkinter import messagebox, font
from tkinter.ttk import Treeview
from tkintermapview import *
from PIL import ImageTk, Image
from pyperclip import *

from API_KEY import api_key
from Vehicle_Classes import Car, Van, Motorcycle
from DatabaseConnection import *
from BookingsClass import Booking
 
def booking_window_open(current_user):

    # ---------------------------------------------------------------------------- #
    #                                    FUNCTIONS USING GOOGLE MAPS API           #
    # ---------------------------------------------------------------------------- #

    def get_distance(pickup_location, dropoff_location, api_key):
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": pickup_location,
            "destinations": dropoff_location,
            "key": api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                distance_value = data['rows'][0]['elements'][0]['distance']['value']  # in meters
                distance_km = round(distance_value / 1000, 2)  # convert to kilometers
                return int(distance_km)
            else:
                raise ValueError(f"Error from API: {data['status']}")
        else:
            response.raise_for_status()
    
    def on_closing():
        main.destroy()

    def load_image(path):
        if os.path.exists(path):
            return ImageTk.PhotoImage(file=path)
        else:
            print(f"File not found: {path}")
            return None
        
    # ---------------------------------------------------------------------------- #
    #                         FUNCTIONS FOR SWITCHING TABS                         #
    # ---------------------------------------------------------------------------- #
    def clear_main():
        main.geometry("800x580")
        main.configure(bg=main_page_color)
        icon_main.place(x=x_position, y=y_position)

        for widgets in home_tab_append:
            widgets.place_forget()

        pickup_label.place_forget()
        pickup_e.place_forget()
        dropoff_label.place_forget()
        dropoff_e.place_forget()
        pax_label.place_forget()
        pax_e.place_forget()
        booking_book_btn.place_forget()
        map_lbl_frame.place_forget()
        home_map.pack_forget()

        profile_tab_lb.place_forget()
        backtohome_btn.place_forget()
        del_acc_btn.place_forget()

        act_treeview.place_forget()

    def homepage_clicked():
        clear_main()
        
        home_lbl_container1.place(x=80, y=210)
        motorcycle_img.place(x=125, y=225)
        motorcycle_name.place(x=93, y=330)
        motorcycle_info.place(x=92, y=385)
        container1_btn.place(x=97, y=460)
        home_lbl_container2.place(x=330, y=210)
        car_img.place(x=370, y=225)
        car_name.place(x=400, y=330)
        car_info.place(x=336, y=385)
        container2_btn.place(x=345, y=460)
        home_lbl_container3.place(x=580, y=210)
        van_img.place(x=618, y=225)
        van_name.place(x=650, y=330)
        van_info.place(x=590, y=385)
        container3_btn.place(x=595, y=460)

    def booking_clicked():

        clear_main()

        pickup_label.place(x=550, y=210)
        pickup_e.place(x=550, y=255)
        dropoff_label.place(x=550, y=280)
        dropoff_e.place(x=550, y=320)
        pax_label.place(x=550, y=350)
        pax_e.place(x=550, y=390)
        booking_book_btn.place(x=550, y=440)
        map_lbl_frame.place(x=80, y=210)
        home_map.pack()

    def success_clicked():

        clear_main()

        profile_tab_lb.place(x=100,y=250)
        backtohome_btn.place(x=100, y=430)
        del_acc_btn.place(x=500, y=430)

    def history_clicked():
        clear_main()

        act_treeview.place(x=100, y=220)
        act_btn_cnl.place()

    # ---------------------------------------------------------------------------- #
    #                             FUNCTIONS FOR BUTTONS                            #
    # ---------------------------------------------------------------------------- #

    def motorcycle_button_clicked():
        global vehicle
        vehicle = Motorcycle()
 
    def car_button_clicked():
        global vehicle
        vehicle = Car()

    def van_button_clicked():
        global vehicle
        vehicle = Van()
    
    def go_back_to_home_page_button_clicked(event):
        homepage_clicked()

    def view_bookings_list_button_clicked(event):
        success_clicked()

    def cancel_button_clicked(event):
        selected_item = act_treeview.focus()
        if selected_item:
            act_treeview.item(selected_item, values=("Cancelled",))
            cancel_booking()

    # ---------------------------------------------------------------------------- #
    #                       FUNCTIONS FOR VALIDATION OF INPUTS                     #
    # ---------------------------------------------------------------------------- #

    def is_address_valid(address):
        endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': address,
            'key': api_key,
        }
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                return True
            else:
                return False
        else:
            print(f"Error: {response.status_code}")
            return False

    def validate_pickup_address(pickup_address):
        if not pickup_address:
            return False, "Please enter a pickup address."
        elif not is_address_valid(pickup_address):
            return False, "Pickup address not found or invalid."
        else:
            return True, ""

    def validate_dropoff_address(dropoff_address):
        if not dropoff_address:
            return False, "Please enter a dropoff address."
        elif not is_address_valid(dropoff_address):
            return False, "Dropoff address not found or invalid."
        else:
            return True, ""

    def validate_passenger_amount(passengers):
        global vehicle

        if vehicle is None:
            return False, "Vehicle type not selected."
        try:
            passenger_count = int(passengers)
        except ValueError:
            return False, "Passenger count should be a numeric value."

        if passenger_count <= 0:
            return False, "Passenger count should be a positive integer."

        if isinstance(vehicle, Car) and 4 < passenger_count <= 6:
            if not messagebox.askyesno("Confirmation", "The number of passengers exceeds the car's capacity. Are you sure you want to continue?", parent=main):
                return False, "Capacity exceeded confirmation denied."

        elif isinstance(vehicle, Van) and 10 < passenger_count <= 12:
            if not messagebox.askyesno("Confirmation", "The number of passengers exceeds the van's capacity. Are you sure you want to continue?", parent=main):
                return False, "Capacity exceeded confirmation denied."

        elif passenger_count > vehicle.capacity:
            return False, "The selected vehicle does not have enough capacity for the number of passengers."
    
        return True, ""

    # ---------------------------------------------------------------------------- #
    #                             FUNCTIONS FOR BOOKING                            #
    # ---------------------------------------------------------------------------- #

    def book_button_clicked():
        #Validates booking information and creates a new booking if valid. Saves it in the current user's list.
        valid_pickup_location, pickup_msg = validate_pickup_address(pickup_e.get().strip())
        valid_dropoff_location, dropoff_msg = validate_dropoff_address(dropoff_e.get().strip())
        valid_passenger_amount, pax_msg = validate_passenger_amount(pax_e.get().strip())

        if not valid_pickup_location:
            messagebox.showerror("Invalid Pick-up Address", pickup_msg, parent=main)
            return False
        
        elif not valid_dropoff_location:
            messagebox.showerror("Invalid Drop off Address", dropoff_msg, parent=main)
            return False
            
        elif not valid_passenger_amount:
            messagebox.showerror("Invalid Passenger Amount", pax_msg, parent=main)
            return False
        
        else:
            username = current_user
            pickup = pickup_e.get().strip()
            dropoff = dropoff_e.get().strip()
            date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vehicle_type = vehicle.get_vehicle_type()
            pax = pax_e.get().strip()
            total_distance = get_distance(pickup, dropoff, api_key)
            total_cost = vehicle.calculate_cost(total_distance)
            status = "Ongoing"

            conn = connect_db()
            cursor = conn.cursor()
            table_name = f"{current_user}_Bookings"
           
            try:
                cursor.execute(f'SELECT MAX("Booking No.") FROM "{table_name}"')
                max_booking_no = cursor.fetchone()
                if max_booking_no is not None:
                    next_booking_no = max_booking_no[0] + 1
                else:
                    next_booking_no = 1
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error fetching max booking number: {e}", parent=main)
                # Handle the error as needed, e.g., logging or displaying an error message
                next_booking_no = None  # or another appropriate value indicating failure

            booking = Booking(username, pickup, dropoff, date_and_time, pax, vehicle_type, total_distance, total_cost, status, next_booking_no)
            booking.save_to_db('RideEaseDatabase.db', f"{current_user}_Bookings")
            add_booking_to_treeview(booking.from_db('next_booking_no', 'RideEaseDatabase.db', f"{current_user}_Bookings"))
            messagebox.showinfo("Booking Successful", "Your booking has been successfully created.", parent=main)
    
            profile_clicked()
            conn.close()
    
    def add_booking_to_treeview(booking_data):
        act_treeview.insert("", "end", values=(
            booking_data["Booking No."], 
            booking_data["Username"], 
            booking_data["Pickup Address"], 
            booking_data["Dropoff Address"], 
            booking_data["Date and Time"], 
            booking_data["Vehicle Type"], 
            booking_data["Pax"], 
            booking_data["Total Distance"], 
            booking_data["Total Cost"], 
            booking_data["Status"]
        ))

    # ---------------------------------------------------------------------------- #
    #        FUNCTIONS FOR CANCEL, SAVE, AND LOAD BOOKINGS IN A FILE               #
    # ---------------------------------------------------------------------------- #

    def cancel_booking():
        selected_item = act_treeview.focus()
        if selected_item:
            booking_data = act_treeview.item(selected_item)['values']
            booking_number = booking_data[0]  # Assuming the first column is the booking ID

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE id=?", (booking_number,))
            conn.commit()
            conn.close()
            act_treeview.delete(selected_item)
            messagebox.showinfo("Booking Cancelled", "The booking has been successfully cancelled.", parent=main)

    def load_bookings():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            table_name = f"{current_user}_Bookings"
            cursor.execute(f"SELECT * FROM {table_name}")
            bookings = cursor.fetchall()
            conn.close()

            for booking in bookings:
                booking_data = {
                    "booking_number": booking[0],
                    "username": booking[1],
                    "pickup": booking[2],
                    "dropoff": booking[3],
                    "date_and_time": booking[4],
                    "vehicle_type": booking[5],
                    "pax": booking[6],
                    "total_distance": booking[7],
                    "total_cost": booking[8],
                    "status": booking[9]
                }
                add_booking_to_treeview(booking_data)
        except:
            pass

    load_bookings()

    # ----------------------------------------------------------------------------------------- #
    #                                   FUNCTIONS FOR FRONTEND                                  #
    # ----------------------------------------------------------------------------------------- #

     # Toggle Icon Function
    def toggle():

        # All these global variables just shows functionality on toggle
        global is_on, extended_menu, home_name, booking_name, success_name, activity_name, global_mode_int
        is_on = not is_on

        # Toggles to toggle_close_icon and toggle_menu_btn
        if is_on:

            toggle_menu_btn.config(image=close_icon)
            toggle_menu_btn.place(x=8, y=15)
            extended_menu = Label(main, bg=menu_bar_color, padx=100, pady=580)
            extended_menu.place(x=50, y=0)

            # Shows extended names for the icons (2)
            home_name = Button(main, text="HOME", bg=menu_bar_color, fg="black", bd=0, 
                                highlightthickness=0, font=("Helvetica", 20, "bold"),
                                activebackground=menu_bar_color, 
                                command=lambda: (btn_modes(ind_lb=home_btn_ind, mode_int=0), homepage_clicked()))
            booking_name = Button(main, text="BOOKING", bg=menu_bar_color, fg="black", bd=0, 
                                    highlightthickness=0, font=("Helvetica", 20, "bold"),
                                    activebackground=menu_bar_color,
                                    command=lambda: (btn_modes(booking_btn_ind, mode_int=1), booking_clicked()))
            success_name = Button(main, text="PROFILE", bg=menu_bar_color, fg="black", bd=0, 
                                    highlightthickness=0, font=("Helvetica", 20, "bold"),
                                    activebackground=menu_bar_color,
                                    command=lambda: (btn_modes(profile_btn_ind, mode_int=2), success_clicked()))
            history_name = Button(main, text="ACTIVITY", bg=menu_bar_color, fg="black", bd=0, 
                                    highlightthickness=0, font=("Helvetica", 20, "bold"),
                                    activebackground=menu_bar_color,
                                    command=lambda: (btn_modes(activity_btn_ind, mode_int=3), history_clicked()))
            home_name.place(x=70, y=130)
            booking_name.place(x=70, y=190)
            success_name.place(x=70, y=250)
            history_name.place(x=70, y=310)

        else:
            toggle_menu_btn.config(image=toggle_icon)
            toggle_menu_btn.place(x=4, y=10)
            extended_menu.after(1, extended_menu.destroy())

            # Deletes the icon names
            home_name.after(1, home_name.destroy())
            booking_name.after(1, booking_name.destroy())
            success_name.after(1, success_name.destroy())
            history_name.after(1, history_name.destroy())

    # Home Page Tab
    def home_tab():
        global home_lbl_container1, motorcycle_name, motorcycle_info, motorcycle_img, container1_btn
        global home_lbl_container2, car_name, car_info, car_img, container2_btn
        global home_lbl_container3, van_name, van_info, van_img, container3_btn

        def clear_color_hometab():
            home_lbl_container1.configure(bg=menu_bar_color)
            home_lbl_container2.configure(bg=menu_bar_color)
            home_lbl_container3.configure(bg=menu_bar_color)
            motorcycle_img.configure(bg=menu_bar_color)
            car_img.configure(bg=menu_bar_color)
            van_img.configure(bg=menu_bar_color)
            motorcycle_name.configure(bg=menu_bar_color)
            car_name.configure(bg=menu_bar_color)
            van_name.configure(bg=menu_bar_color)
            motorcycle_info.configure(bg=menu_bar_color)
            car_info.configure(bg=menu_bar_color)
            van_info.configure(bg=menu_bar_color)

        def vehicle_clicked(mode):
            print(mode)
            clear_color_hometab()
            highlight_color = "#FFE8C8"
            global vehicle
            if mode == 0:
                home_lbl_container1.configure(bg=highlight_color)
                motorcycle_name.configure(bg=highlight_color)
                motorcycle_img.configure(bg=highlight_color)
                motorcycle_info.configure(bg=highlight_color)
                container1_btn.configure(state=DISABLED)
                container2_btn.configure(state=NORMAL)
                container3_btn.configure(state=NORMAL)
                vehicle = 'Motorcycle'
                print(vehicle)
            elif mode == 1:
                home_lbl_container2.configure(bg=highlight_color)
                car_name.configure(bg=highlight_color)
                car_img.configure(bg=highlight_color)
                car_info.configure(bg=highlight_color)
                container1_btn.configure(state=NORMAL)
                container2_btn.configure(state=DISABLED)
                container3_btn.configure(state=NORMAL)
                vehicle = 'Car'
                print(vehicle)
            elif mode == 2:
                home_lbl_container3.configure(bg=highlight_color)
                van_name.configure(bg=highlight_color)
                van_img.configure(bg=highlight_color)
                van_info.configure(bg=highlight_color)
                container1_btn.configure(state=NORMAL)
                container2_btn.configure(state=NORMAL)
                container3_btn.configure(state=DISABLED)
                vehicle = 'Van'
                print(vehicle)

        home_lbl_container1 = LabelFrame(main, bg=menu_bar_color, width=200, height=320, bd=3)
        home_lbl_container1.place(x=80, y=210)
        motorcycle_img = Label(main, image=motorcycle_icon, bg=menu_bar_color)
        motorcycle_img.place(x=125, y=225)
        motorcycle_name = Label(main, text="MOTORCYCLE", font=("Helvetica", 18, "bold"), bg=menu_bar_color)
        motorcycle_name.place(x=93, y=330)
        motorcycle_info = Label(main, text="Recommended Pax: 1\nPassenger Limit: 1", font=("Helvetica", 13, "bold"), bg=menu_bar_color)
        motorcycle_info.place(x=92, y=385)
        container1_btn = Button(main, text="SELECT", width=20, bd=2, bg="white", font=("Helvetica", 10, "bold"),
                                command=lambda: vehicle_clicked(0))
        container1_btn.place(x=97, y=460)

        home_lbl_container2 = LabelFrame(main, bg=menu_bar_color, width=200, height=320, bd=3)
        home_lbl_container2.place(x=330, y=210)
        car_img = Label(main, image=car2_icon, bg=menu_bar_color)
        car_img.place(x=370, y=225)
        car_name = Label(main, text="CAR", font=("Helvetica", 18, "bold"), bg=menu_bar_color)
        car_name.place(x=400, y=330)
        car_info = Label(main, text="Recommended Pax: 2-4\nPassenger Limit: 6", font=("Helvetica", 13, "bold"), bg=menu_bar_color)
        car_info.place(x=336, y=385)
        container2_btn = Button(main, text="SELECT", width=20, bd=2, bg="white", font=("Helvetica", 10, "bold"),
                                command=lambda: vehicle_clicked(1))
        container2_btn.place(x=345, y=460)

        home_lbl_container3 = LabelFrame(main, bg=menu_bar_color, width=200, height=320, bd=3)
        home_lbl_container3.place(x=580, y=210)
        van_img = Label(main, image=van_icon, bg=menu_bar_color)
        van_img.place(x=618, y=225)
        van_name = Label(main, text="VAN", font=("Helvetica", 18, "bold"), bg=menu_bar_color)
        van_name.place(x=650, y=330)
        van_info = Label(main, text="Recommended Pax: 5-10\nPassenger Limit: 12", font=("Helvetica", 11, "bold"), bg=menu_bar_color)
        van_info.place(x=590, y=385)
        container3_btn = Button(main, text="SELECT", width=20, bd=2, bg="white", font=("Helvetica", 10, "bold"),
                                command=lambda: vehicle_clicked(2))
        container3_btn.place(x=595, y=460)

        home_tab_append.extend([
        home_lbl_container1,
        home_lbl_container2,
        home_lbl_container3,
        container1_btn,
        container2_btn,
        container3_btn,
        motorcycle_img,
        motorcycle_info,
        motorcycle_name,
        car_img,
        car_name,
        car_info,
        van_img,
        van_info,
        van_name
        ])

    # Mode to indicate which tab (0 for Home, 1 for Booking, 2 for Profile, 3 for Activity)
    global_mode_int = 3 # Indicates its in Home Tab

    # Button Indicator Function
    def btn_modes(ind_lb, mode_int):
        global home_name, booking_name, success_name, history_name
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
            print ("Success Tab")

        elif ind_lb == activity_btn_ind:
            mode_int = 3
            print ("History Tab")

        global global_mode_int
        global_mode_int = mode_int
        print(global_mode_int)

    # ------------------------------------------------------------------------- #
    #                                   DESIGN                                  #
    # ------------------------------------------------------------------------- #
    
    # All color
    main_page_color = "#0f0f0f"
    menu_bar_color = "#ffb700"
    history_bg_color = "#ffec9e"

    main = Tk()
    main.geometry("800x580+0+0")
    main.title("Ride Ease - Book a Ride")
    main.resizable(False, False)
    main.configure(bg=main_page_color)
    main.iconbitmap("icons/RideEaseLogo.ico") 
    
    # Mode to indicate which tab (0 for Home, 1 for Booking, 2 for Profile, 3 for Activity)
    global_mode_int = 0 # Indicates its in Home Tab

    # Button Indicator Function
    def btn_modes(ind_lb, mode_int):
        global home_name, booking_name, profile_name, activity_name

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

        global global_mode_int
        global_mode_int = mode_int

    # Initialize Toggle Button as default(off)
    is_on = False

    # Toggle Icon Function
    def toggle():

        # All these global variables just shows functionality on toggle
        global is_on, home_name, booking_name, profile_name, activity_name, global_mode_int
        is_on = not is_on

        # Toggles to toggle_close_icon and toggle_menu_btn
        if is_on:
            menu_bar_frame.configure(width=250)
            menu_bar_frame.tkraise()
            toggle_menu_btn.configure(image=close_icon)
            toggle_menu_btn.place(x=5, y=14)

            # Shows extended names for the icons (2)
            home_name = Button(main, text="HOME", bg=menu_bar_color, fg="black", bd=0, 
                                highlightthickness=0, font=("Helvetica", 20, "bold"),
                                activebackground=menu_bar_color, 
                                command=lambda: (btn_modes(ind_lb=home_btn_ind, mode_int=0), homepage_clicked()))
            booking_name = Button(main, text="BOOKING", bg=menu_bar_color, fg="black", bd=0, 
                                    highlightthickness=0, font=("Helvetica", 20, "bold"),
                                    activebackground=menu_bar_color,
                                    command=lambda: (btn_modes(booking_btn_ind, mode_int=1), booking_clicked()))
            profile_name = Button(main, text="PROFILE", bg=menu_bar_color, fg="black", bd=0, 
                                    highlightthickness=0, font=("Helvetica", 20, "bold"),
                                    activebackground=menu_bar_color,
                                    command=lambda: (btn_modes(profile_btn_ind, mode_int=2), profile_clicked()))
            activity_name = Button(main, text="ACTIVITY", bg=menu_bar_color, fg="black", bd=0, 
                                    highlightthickness=0, font=("Helvetica", 20, "bold"),
                                    activebackground=menu_bar_color,
                                    command=lambda: (btn_modes(activity_btn_ind, mode_int=3), activity_clicked()))
            home_name.place(x=70, y=130)
            booking_name.place(x=70, y=190)
            profile_name.place(x=70, y=250)
            activity_name.place(x=70, y=310)

        else:
            menu_bar_frame.configure(width=50)
            toggle_menu_btn.configure(image=toggle_icon)
            toggle_menu_btn.place(x=4, y=10)

            # Deletes the icon names
            home_name.place_forget()
            booking_name.place_forget()
            profile_name.place_forget()
            activity_name.place_forget()

    def clear_main():
        main.configure(bg=main_page_color)
        icon_main.place(x=x_position, y=y_position)

        for widgets in home_tab_append:
            widgets.place_forget()

        pickup_label.place_forget()
        pickup_e.place_forget()
        dropoff_label.place_forget()
        dropoff_e.place_forget()
        pax_label.place_forget()
        pax_e.place_forget()
        booking_book_btn.place_forget()
        map_lbl_frame.place_forget()
        home_map.pack_forget()

        profile_tab_lb.place_forget()
        backtohome_btn.place_forget()
        del_acc_btn.place_forget()

        act_treeview.place_forget()

    def homepage_clicked():
        clear_main()
        
        home_lbl_container1.place(x=80, y=210)
        motorcycle_img.place(x=125, y=225)
        motorcycle_name.place(x=93, y=330)
        motorcycle_info.place(x=92, y=385)
        container1_btn.place(x=97, y=460)
        home_lbl_container2.place(x=330, y=210)
        car_img.place(x=370, y=225)
        car_name.place(x=400, y=330)
        car_info.place(x=336, y=385)
        container2_btn.place(x=345, y=460)
        home_lbl_container3.place(x=580, y=210)
        van_img.place(x=618, y=225)
        van_name.place(x=650, y=330)
        van_info.place(x=590, y=385)
        container3_btn.place(x=595, y=460)

    def booking_clicked():

        clear_main()

        pickup_label.place(x=550, y=210)
        pickup_e.place(x=550, y=255)
        dropoff_label.place(x=550, y=280)
        dropoff_e.place(x=550, y=320)
        pax_label.place(x=550, y=350)
        pax_e.place(x=550, y=390)
        booking_book_btn.place(x=550, y=440)
        map_lbl_frame.place(x=80, y=210)
        home_map.pack()

    def profile_clicked():

        clear_main()

        profile_tab_lb.place(x=100,y=250)
        backtohome_btn.place(x=100, y=430)
        del_acc_btn.place(x=500, y=430)

    def activity_clicked():
        clear_main()

        act_treeview.place(x=80, y=200)

    def load_image(path):
        if os.path.exists(path):
            return ImageTk.PhotoImage(file=path)
        else:
            print(f"File not found: {path}")
            return None

    home_tab_append = []

    # Home Page Tab
    def home_tab():
        global home_lbl_container1, motorcycle_name, motorcycle_info, motorcycle_img, container1_btn
        global home_lbl_container2, car_name, car_info, car_img, container2_btn
        global home_lbl_container3, van_name, van_info, van_img, container3_btn

        def clear_color_hometab():
            home_lbl_container1.configure(bg=menu_bar_color)
            home_lbl_container2.configure(bg=menu_bar_color)
            home_lbl_container3.configure(bg=menu_bar_color)
            motorcycle_img.configure(bg=menu_bar_color)
            car_img.configure(bg=menu_bar_color)
            van_img.configure(bg=menu_bar_color)
            motorcycle_name.configure(bg=menu_bar_color)
            car_name.configure(bg=menu_bar_color)
            van_name.configure(bg=menu_bar_color)
            motorcycle_info.configure(bg=menu_bar_color)
            car_info.configure(bg=menu_bar_color)
            van_info.configure(bg=menu_bar_color)

        def vehicle_clicked(mode):
            print("Mode =", mode)
            clear_color_hometab()
            highlight_color = "#FFE8C8"
            if mode == 0:
                home_lbl_container1.configure(bg=highlight_color)
                motorcycle_name.configure(bg=highlight_color)
                motorcycle_img.configure(bg=highlight_color)
                motorcycle_info.configure(bg=highlight_color)
                container1_btn.configure(state=DISABLED)
                container2_btn.configure(state=NORMAL)
                container3_btn.configure(state=NORMAL)
            elif mode == 1:
                home_lbl_container2.configure(bg=highlight_color)
                car_name.configure(bg=highlight_color)
                car_img.configure(bg=highlight_color)
                car_info.configure(bg=highlight_color)
                container1_btn.configure(state=NORMAL)
                container2_btn.configure(state=DISABLED)
                container3_btn.configure(state=NORMAL)
            elif mode == 2:
                home_lbl_container3.configure(bg=highlight_color)
                van_name.configure(bg=highlight_color)
                van_img.configure(bg=highlight_color)
                van_info.configure(bg=highlight_color)
                container1_btn.configure(state=NORMAL)
                container2_btn.configure(state=NORMAL)
                container3_btn.configure(state=DISABLED)

        home_lbl_container1 = LabelFrame(main, bg=menu_bar_color, width=200, height=320, bd=3)
        home_lbl_container1.place(x=80, y=210)
        motorcycle_img = Label(main, image=motorcycle_icon, bg=menu_bar_color)
        motorcycle_img.place(x=125, y=225)
        motorcycle_name = Label(main, text="MOTORCYCLE", font=("Helvetica", 18, "bold"), bg=menu_bar_color)
        motorcycle_name.place(x=93, y=330)
        motorcycle_info = Label(main, text="Recommended Pax: 1\nPassenger Limit: 1", font=("Helvetica", 13, "bold"), bg=menu_bar_color)
        motorcycle_info.place(x=92, y=385)
        container1_btn = Button(main, text="SELECT", width=20, bd=2, bg="white", font=("Helvetica", 10, "bold"),
                                command=lambda: [vehicle_clicked(0), btn_modes(booking_btn_ind, mode_int=1), motorcycle_button_clicked(), booking_clicked()]
                                                )
        container1_btn.place(x=97, y=460)

        home_lbl_container2 = LabelFrame(main, bg=menu_bar_color, width=200, height=320, bd=3)
        home_lbl_container2.place(x=330, y=210)
        car_img = Label(main, image=car2_icon, bg=menu_bar_color)
        car_img.place(x=370, y=225)
        car_name = Label(main, text="CAR", font=("Helvetica", 18, "bold"), bg=menu_bar_color)
        car_name.place(x=400, y=330)
        car_info = Label(main, text="Recommended Pax: 2-4\nPassenger Limit: 6", font=("Helvetica", 13, "bold"), bg=menu_bar_color)
        car_info.place(x=336, y=385)
        container2_btn = Button(main, text="SELECT", width=20, bd=2, bg="white", font=("Helvetica", 10, "bold"),
                                command=lambda: [vehicle_clicked(1), btn_modes(booking_btn_ind, mode_int=1), car_button_clicked(), booking_clicked()])
        container2_btn.place(x=345, y=460)

        home_lbl_container3 = LabelFrame(main, bg=menu_bar_color, width=200, height=320, bd=3)
        home_lbl_container3.place(x=580, y=210)
        van_img = Label(main, image=van_icon, bg=menu_bar_color)
        van_img.place(x=618, y=225)
        van_name = Label(main, text="VAN", font=("Helvetica", 18, "bold"), bg=menu_bar_color)
        van_name.place(x=650, y=330)
        van_info = Label(main, text="Recommended Pax: 5-10\nPassenger Limit: 12", font=("Helvetica", 11, "bold"), bg=menu_bar_color)
        van_info.place(x=590, y=385)
        container3_btn = Button(main, text="SELECT", width=20, bd=2, bg="white", font=("Helvetica", 10, "bold"),
                                command=lambda: [vehicle_clicked(2), btn_modes(booking_btn_ind, mode_int=1), van_button_clicked(), booking_clicked()])
        container3_btn.place(x=595, y=460)

        home_tab_append.extend([
        home_lbl_container1,
        home_lbl_container2,
        home_lbl_container3,
        container1_btn,
        container2_btn,
        container3_btn,
        motorcycle_img,
        motorcycle_info,
        motorcycle_name,
        car_img,
        car_name,
        car_info,
        van_img,
        van_info,
        van_name
        ])

    # Icons (Logo, Menu Toggle, Home, Booking, Profile, Activity, Close)
    icon_path = "images/homepage_icon.png"
    icon = Image.open(icon_path).convert("RGBA")

    toggle_icon_path = "images/toggle_btn_icon.png"
    toggle_icon = load_image(toggle_icon_path)

    home_icon_path = "images/home_icon.png"
    home_icon = load_image(home_icon_path)

    booking_path = "images/booking_icon.png"
    booking_icon = load_image(booking_path)

    profile_path = "images/profile_icon.png"
    profile_icon = load_image(profile_path)

    activity_path = "images/activity_icon.png"
    activity_icon = load_image(activity_path)

    close_path = "images/close_btn_icon.png"
    close_icon = load_image(close_path)

    motorcycle_path = "images/motorcycle.png"
    motorcycle_icon = load_image(motorcycle_path)

    car2_path = "images/car(2).png"
    car2_icon = load_image(car2_path)

    van_path = "images/van.png"
    van_icon = load_image(van_path)

    # Menu Bar Config
    menu_bar_frame = Frame(main, bg=menu_bar_color, padx=3, pady=4)

    # Menu Bar Placement
    menu_bar_frame.pack(side=LEFT, fill=Y)
    menu_bar_frame.pack_propagate(False)
    menu_bar_frame.configure(width=50)

    # Toggle Icon Button and Packing (Placed in Menu Bar)
    toggle_menu_btn = Button(menu_bar_frame, image=toggle_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=toggle)
    toggle_menu_btn.place(x=4, y=10)

    # Home Button (Placed in Menu Bar)
    home_btn = Button(menu_bar_frame, image=home_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=lambda: (btn_modes(ind_lb=home_btn_ind, mode_int=0),
                            homepage_clicked()))
    home_btn.place(x=8, y=130, width=30, height=40)

    # Home Button Indicator
    home_btn_ind = Label(menu_bar_frame, bg="white")
    home_btn_ind.place(x=1, y=130, width=3, height=40)

    # Booking Button (Placed in Menu Bar)
    booking_btn = Button(menu_bar_frame, image=booking_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=lambda: (btn_modes(booking_btn_ind, mode_int=1),
                        booking_clicked()))
    booking_btn.place(x=8, y=190, width=30, height=40)

    # Booking Button Indicator
    booking_btn_ind = Label(menu_bar_frame, bg=menu_bar_color)
    booking_btn_ind.place(x=1, y=190, width=3, height=40)

    # Profile Button (Placed in Menu Bar)
    profile_btn = Button(menu_bar_frame, image=profile_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=lambda: (btn_modes(profile_btn_ind, mode_int=2),
                            profile_clicked()))
    profile_btn.place(x=8, y=250, width=30, height=40)

    # Profile Button Indicator
    profile_btn_ind = Label(menu_bar_frame, bg=menu_bar_color)
    profile_btn_ind.place(x=1, y=250, width=3, height=40)

    # Activity Button (Placed in Menu Bar)
    activity_btn = Button(menu_bar_frame, image=activity_icon, bg=menu_bar_color,
                            bd=0, activebackground=menu_bar_color, command=lambda: (btn_modes(activity_btn_ind, mode_int=3),
                            activity_clicked()))
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
    # Home Tab
    home_tab()

    # Booking Tab (Map)
    map_lbl_frame = LabelFrame(main)

    home_map = TkinterMapView(map_lbl_frame, width=430, height=300, corner_radius=0)
    home_map.set_position(14.5995, 120.9842) # Manila
    home_map.set_zoom(10)

    # Pick-up label and entry
    pickup_label = Label(main, text="Pick Up", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))

    pickup_e = Entry(main, width=35)

    # Drop-off label and entry
    dropoff_label = Label(main, text="Drop Off", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))

    dropoff_e = Entry(main, width=35)

    # Pax label and entry
    pax_label = Label(main, text="Pax", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 20))

    pax_e = Entry(main, width=35)

    # Book Button
    booking_book_btn = Button(main, text="Book", fg=main_page_color, bg=menu_bar_color, font=("Helvetica", 12),
                            bd=0, activebackground=menu_bar_color, padx=85, pady=5, 
                            command=lambda: [btn_modes(ind_lb=profile_btn_ind, mode_int=2), book_button_clicked()])

    # Profile
    profile_tab_lb = Label(main, text="Booking Successful!", fg=menu_bar_color, bg=main_page_color, font=("Helvetica", 25))
    backtohome_btn = Button(main, text="Go Back to Homepage", fg=main_page_color, bg=menu_bar_color, font=("Helvetica", 20),
                        activebackground=menu_bar_color, command=lambda: (btn_modes(ind_lb=home_btn_ind, mode_int=0), homepage_clicked()))
    del_acc_btn = Button(main, text="View All Bookings", fg=main_page_color, bg=menu_bar_color, font=("Helvetica", 20),
                        activebackground=menu_bar_color, command=lambda: (btn_modes(activity_btn_ind, mode_int=3), activity_clicked()))

    # Activity
    act_treeview = Treeview(main, height=12)
    act_treeview["columns"] = ("Username", "Email", "Date", "Time", "Pick Up", "Drop off", "Ride Status")

    act_treeview.column("#0", width=0, stretch=NO)
    act_treeview.column("Username", anchor=W, width=120)
    act_treeview.column("Email", anchor=W, width=120)
    act_treeview.column("Date", anchor=W, width=60)
    act_treeview.column("Time", anchor=W, width=60)
    act_treeview.column("Pick Up", anchor=W, width=120)
    act_treeview.column("Drop off", anchor=W, width=120)
    act_treeview.column("Ride Status", anchor=W, width=80)

    act_treeview.heading("#0", text="", anchor=W)
    act_treeview.heading("Username", text="Username", anchor=W)
    act_treeview.heading("Email", text="Email", anchor=W)
    act_treeview.heading("Date", text="Date", anchor=W)
    act_treeview.heading("Time", text="Time", anchor=W)
    act_treeview.heading("Pick Up", text="Pick Up", anchor=W)
    act_treeview.heading("Drop off", text="Drop off", anchor=W)
    act_treeview.heading("Ride Status", text="Ride Status", anchor=W)

    act_btn_cnl = Button(main, text="Cancel Booking", fg=main_page_color, bg=menu_bar_color, font=("Helvetica", 20),
                            bd=1, activebackground=menu_bar_color)

    # Insert sample data
    act_treeview.insert(parent="", index="end", iid=0, text="",
                        values=("John", "john@example.com", "07/16", "21:00", "Manila", "Alabang", "Completed"))

    main.mainloop()
