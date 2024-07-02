from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview, Progressbar, Notebook
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog
from PIL import Image, ImageTk
import webbrowser
import json
import requests
from Vehicle_Classes import Vehicle, Motorcycle, Car, Van
from BookingsClass import Booking
from datetime import datetime
import requests
import glob

def booking_window_open():

# ---------------------------------------------------------------------------- #
#                                    BACKEND                                   #
# ---------------------------------------------------------------------------- #

    api_key = "AIzaSyDVMXyo9XYUdOBjr9Kv0TLbpQiDVv2lds0" 

    def get_distance(pickup_location, dropoff_location, api_key):
        #Calculates the estimated distance travelled based on common routes.
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
                distance_km = round(distance_value / 1000, 2) # convert to kilometers
                return distance_km
            else:
                raise ValueError(f"Error from API: {data['status']}")
        else:
            response.raise_for_status()

    def load_current_user():
        #Identifies which account is logged in.
        with open("Accounts.json", "r") as file:
            data = json.load(file)
        return data["current_user"]
    
    def on_closing(event):
        #Saves booking data even if the application is closed. 
        #Ensures data retention.
        booking_window.save_bookings(booking_window)
        booking_window.destroy()

# ---------------------------------------------------------------------------- #
#                         FUNCTIONS FOR SWITCHING TABS                         #
# ---------------------------------------------------------------------------- #

    def switch_to_home_tab():
        #Switches to home page
        notebook.select(home_tab)

    def switch_to_booking_tab():
        #Switches to booking tab
        notebook.select(booking_tab)

    def switch_to_booking_successful_tab():
        notebook.select(booking_successful_tab)

    def switch_to_bookings_list_tab():
        #Switches to booking lists tab.
        notebook.select(bookings_list_tab)

# ---------------------------------------------------------------------------- #
#                             FUNCTIONS FOR BUTTONS                            #
# ---------------------------------------------------------------------------- #

    def motorcycle_button_clicked(event):
        global vehicle
        vehicle = Motorcycle()
        switch_to_booking_tab()

    def car_button_clicked(event):
        global vehicle
        vehicle = Car()
        switch_to_booking_tab()

    def van_button_clicked(event):
        global vehicle
        vehicle = Van()
        switch_to_booking_tab()
    
    def go_back_to_home_page_button_clicked(event):
        switch_to_home_tab()
        #####################gamitin to para sa button ng 3rd tab pati na rin dun sa gilid na icon############

    def view_bookings_list_button_clicked(event):
        switch_to_bookings_list_tab()
        #################gamitin to para sa button ng 3rd tab pati na rin dun sa gilid na icon##########

    def cancel_button_clicked(event):
        selected_item = bookings_treeview.focus()
        if selected_item:
            bookings_treeview.item(selected_item, values=("Cancelled",))
            cancel_booking()

# ---------------------------------------------------------------------------- #
#                       FUNCTIONS FOR VALIDATION OF INPUS                      #
# ---------------------------------------------------------------------------- #

    def is_address_valid(address):
        #Check if the given address is valid according to Google Maps Geocoding API.
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

    def validate_pickup_address(pickup_address_entry):
        #Validate the pickup address if it really exsists.
        pickup_address = pickup_address_entry.get().strip()
        if not pickup_address:
            return False, "Please enter a pickup address."      
        elif not is_address_valid(pickup_address):
            return False, "Pickup address not found or invalid."
        else:
            return True

    def validate_dropoff_address(dropoff_address_entry):
        #Validates the dropoff address if it really exists.
        dropoff_address = dropoff_address_entry.get().strip()
        if not dropoff_address:
            return False, "Please enter a dropoff address."
        elif not is_address_valid(dropoff_address):
            return False, "Dropoff address not found or invalid."
        else:
            return True

    def validate_passenger_amount(passengers):
        # Validates if pax entered is less than or equal the capacity of selected vehicle.

        try:
            passenger_count = int(passengers)
        except ValueError:
            return False, "Passenger count should be a numeric value."

        if passenger_count <= 0:
            return False, "Passenger count should be a positive integer."

        #Car's recommended capacity is 4, allow up to 6 passengers only.
        if isinstance(vehicle, Car) and 4 < passenger_count <= 6:
            if not messagebox.askyesno("Confirmation", "The number of passengers exceeds the car's capacity. Are you sure you want to continue?", parent=booking_window):
                return

        #Van's recommended capacity is 10, allow up to 12 passengers only.
        elif isinstance(vehicle, Van) and 10 < passenger_count <= 12:
            if not messagebox.askyesno("Confirmation", "The number of passengers exceeds the van's capacity. Are you sure you want to continue?", parent=booking_window):
                return

        #Error if passenger amount is greater than vehicle capacity.
        elif passenger_count > vehicle.capacity:
            return "The selected vehicle does not have enough capacity for the number of passengers."
    
        return

# ---------------------------------------------------------------------------- #
#                             FUNCTIONS FOR BOOKING                            #
# ---------------------------------------------------------------------------- #

    def book_now(username, pickup, dropoff, date_and_time, pax, vehicle_type, total_distance, total_cost, status):
        #validates booking information and creates a new booking if valid.
        valid_pickup_location, pickup_msg = validate_pickup_address(pickup)
        valid_dropoff_location, dropoff_msg = validate_dropoff_address(dropoff)
        valid_passenger_amount, pax_msg = validate_passenger_amount(pax)

        if not valid_pickup_location:
            messagebox.showerror("Invalid Pick-up Address", pickup_msg, parent=booking_window)
            return False
        
        elif not valid_dropoff_location:
            messagebox.showerror("Invalid Drop off Address", dropoff_msg, parent=booking_window)
            return False
            
        elif not valid_passenger_amount:
            messagebox.showerror("Invalid Passenger Amount", dropoff_msg, parent=booking_window)
            return False
            
        else:
            booking = Booking(username, pickup, dropoff, date_and_time, vehicle_type, pax, total_distance, total_cost, status)
            Booking.to_dict()

         

                # Insert the booking in the list.
####################################PALITAN TO SYEMPRE#####################################
            self.listbox.insert(tk.END, f"Booking #{booking.no}: {user}")
            Booking.save_to_file(booking, f"booking_{booking.no}.json")

            booking.list

        # Create a booking.
            booking = Booking(user, vehicle, start_location, end_location, km)
            self.bookings[booking.no] = booking
####################################################################################
        

    def book_button_clicked(event):
        #Retrieves booking information from entry fields and calls the book_now function.
        username = load_current_user()
        pickup = pickup_user_entry.get()
        dropoff = dropoff_user_entry.get()
        date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vehicle_type = vehicle.get_vehicle_type()
        pax = pax_user_entry.get()
        total_distance = get_distance(pickup_user_entry.get(), dropoff_user_entry.get(), api_key )
        total_cost = vehicle.calculate_cost(int(total_distance))
        status = "Ongoing"

        book_now(username, pickup, dropoff, date_and_time, pax, vehicle_type, total_distance, total_cost, status)
        
    def add_booking_to_treeview(self, booking_data):
        #Adds booking data to the treeview in a new row.
        self.treeview.insert("", "end", values=(
            booking_data["username"], booking_data["pickup"], booking_data["dropoff"], booking_data["date_and_time"],
            booking_data["vehicle_type"], booking_data["pax"], booking_data["total_distance"], booking_data["total_cost"],
            booking_data["status"]
        ))
        
# ---------------------------------------------------------------------------- #
#        FUNCTIONS FOR CANCEL, SAVE, AND LOAD BOOKINGS IN A FILE               #
# ---------------------------------------------------------------------------- #
#################################PALITAN LAHAT TO SYEMPREEEEEEEEEEEEEEEEEEEE#########################
    def cancel_booking(self):
        
        selected = self.listbox.curselection()
        if selected:
            booking_id = int(self.listbox.get(selected).split(':')[0].split('#')[1])

            del self.bookings[booking_id]
            Booking.delete_file(f"booking_{booking_id}.json")
            self.listbox.delete(selected)

    def save_bookings(booking_window):
        for no, booking in booking_window.bookings.items():
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

# ---------------------------------------------------------------------------- #
#                                   FRONTEND                                   #
# ---------------------------------------------------------------------------- #

    booking_window = Toplevel(booking_window)
    booking_window.title("Ride Booking System")
    booking_window.iconbitmap("icons/RideEaseLogo.ico") 
    booking_window.resizable(False,False)

    # Ensure bookings are saved when the application closes
    booking_window.protocol("WM_DELETE_WINDOW", booking_window.on_closing)

    # User Entry
    user_label = Label(self.root, text="User:")
    user_label.grid(row=0, column=0)
    user_entry = Entry(self.root)
    user_entry.grid(row=0, column=1)

    # Vehicle Selection
    vehicle_label = Label(self.root, text="Vehicle Type:")
    vehicle_label.grid(row=1, column=0)
    vehicle_var = StringVar(self.root)
    vehicle_var.set("Car")
    vehicle_menu = OptionMenu(self.root, self.vehicle_var, *self.vehicles.keys())
    vehicle_menu.grid(row=1, column=1)

    # Start Location Entry
    start_label = Label(self.root, text="Start Location:")
    start_label.grid(row=2, column=0)
    start_entry = Entry(self.root)
    start_entry.grid(row=2, column=1)

    # End Location Entry
    end_label = Label(self.root, text="End Location:")
    end_label.grid(row=3, column=0)
    end_entry = Entry(self.root)
    end_entry.grid(row=3, column=1)

    # Distance Entry (Read-only)
    distance_label = Label(self.root, text="Distance:")
    distance_label.grid(row=4, column=0)
    distance_entry = Entry(self.root, state='readonly')
    distance_entry.grid(row=4, column=1)

    # Number of Passengers Entry
    passengers_label = Label(self.root, text="Number of Passengers:")
    passengers_label.grid(row=5, column=0)
    passengers_entry = Entry(self.root)
    passengers_entry.grid(row=5, column=1)

    # Book Button
    book_button = Button(self.root, text="Book Ride", command=self.book_ride)
    book_button.grid(row=6, column=0, columnspan=2)

    # Listbox for Bookings
    listbox = Listbox(self.root, width=50, height=10)
    listbox.grid(row=7, column=0, columnspan=2)
    listbox.bind('<Double-Button-1>', self.show_details)

    # Cancel Button
    cancel_button = Button(self.root, text="Cancel Booking", command=self.cancel_booking)
    cancel_button.grid(row=8, column=0, columnspan=2)

    booking_window.mainloop()

booking_window_open()
