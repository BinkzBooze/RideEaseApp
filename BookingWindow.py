from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview, Progressbar, Notebook
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog
from PIL import Image, ImageTk
import webbrowser
import json
import re
import requests
from Vehicle_Classes import Vehicle, Motorcycle, Car, Van
from BookingsClass import Booking
from datetime import datetime
import requests


def booking_window_open():

# ---------------------------------------------------------------------------- #
#                                    BACKEND                                   #
# ---------------------------------------------------------------------------- #

    api_key = "AIzaSyDVMXyo9XYUdOBjr9Kv0TLbpQiDVv2lds0" 

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
                distance_km = round(distance_value / 1000, 2) # convert to kilometers
                return distance_km
            else:
                raise ValueError(f"Error from API: {data['status']}")
        else:
            response.raise_for_status()

    def load_current_user():
        with open("Accounts.json", "r") as file:
            data = json.load(file)
        return data["current_user"]

    def switch_to_booking_tab():
        notebook.select(booking_tab)

    def switch_to_home_tab():
        notebook.select(home_tab)

    def switch_to_bookings_list_tab():
        notebook.select(bookings_list_tab)

    def motorcycle_button_clicked(event):
        global passenger_limit
        global vehicle
        passenger_limit = 1
        vehicle = Motorcycle()
        switch_to_booking_tab()

    def car_button_clicked(event):
        global passenger_limit
        global vehicle
        passenger_limit = 6
        vehicle = Car()
        switch_to_booking_tab()

    def van_button_clicked(event):
        global passenger_limit
        global vehicle
        passenger_limit = 12
        vehicle = Van()
        switch_to_booking_tab()
    
    def book_now_button_clicked(event):
        pickup_location = pickup_location_entry.get()
        dropoff_location = dropoff_location_entry.get()
        pax = pax_entry.get()

        if not pickup_location or not dropoff_location or not pax:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            pax_int = int(pax)
            if pax_int <= 0 or pax_int > passenger_limit:
                messagebox.showerror("Error", f"Pax must be between 1 and {passenger_limit}.")
                return
        except ValueError:
            messagebox.showerror("Error", "Pax must be a valid integer.")
            return

        # Handle successful booking
    def switch_to_booking_successful_tab():

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
        
    def validate_pickup_location():
        #Validates the pick-up address if it exists.


    def validate_dropoff_location():
        #Validates the drop off address if it exists.

    def validate_passenger_amount():
        #Validates if pax entered is less than or equal the capacity of selected vehicle.


    def book_now(pickup_location, dropoff_location, passenger_amount)
        #validates booking information and creates a new booking if valid.
        valid_pickup_location, pickup_msg = validate_pickup_location(pickup_location)
        valid_dropoff_location, dropoff_msg = validate_dropoff_location(dropoff_location)
        valid_passenger_amount, pax_msg = validate_passenger_amount(passenger_amount)

        if not valid_pickup_location:
            messagebox.showerror("Invalid Pick-up Address", pickup_msg, parent=booking_window)
            return False
        
        elif not valid_dropoff_location:
            messagebox.showerror("Invalid Drop off Address", dropoff_msg, parent=booking_window)
            return False
            
        elif not valid_passenger_amount:
            messagebox.showerror("Invalid Passenger Amount.", pax_msg, parent=booking_window)
            return False
            
        else:
            Booking(username, pickup, dropoff, date_and_time, vehicle_type, pax, total_distance, total_cost, status)
            Booking.to_dict()

    def book_button_clicked():
        #Retrieves booking information from entry fields and calls the book_now function.
        username = load_current_user()
        pickup = pickup_user_entry.get()
        dropoff = dropoff_user_entry.get()
        date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vehicle_type = vehicle.get_vehicle_type()
        total_distance = get_distance(pickup_user_entry.get(), dropoff_user_entry.get(), api_key )
        total_cost = vehicle.calculate_cost(int(total_distance))
        status = "ongoing"

        if book_now(username, pickup, dropoff, date_and_time, vehicle_type, total_distance, total_cost, status) == True:
            switch_to_booking_successful_tab()  #Transitions to 3rd tab, the "Successfully Booked" tab.

##########ALISIN ANG SELFFFFFFFFFFFF####################################################################

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
