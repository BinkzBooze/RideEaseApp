import json
import os
import uuid
from Vehicle_Classes import Car, Van, Motorcycle

# Creation of User's Booking Information
class Booking:
    _customer_no = 1

    def __init__(self, user, pickup_location, dropoff_location, date_and_time, pax, vehicle, total_distance, total_cost, status, number=None, booking_id=None):
        if number is not None:
            self.no = number
            Booking._customer_no = max(Booking._customer_no, number + 1)
        else:
            self.no = Booking._customer_no
            Booking._customer_no += 1

        self.booking_id = booking_id if booking_id else str(uuid.uuid4())
        self.user = user
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.date_and_time = date_and_time
        self.pax = pax
        self.vehicle = vehicle
        self.total_distance = total_distance
        self.total_cost = self.vehicle.calculate_cost(total_distance)
        self.status = status

    def to_dict(self):
        return {
            'Date and Time': self.date_and_time,
            'Customer No.': self.no,
            'ID': self.booking_id,
            'Name': self.user,
            'Vehicle': type(self.vehicle).__name__,
            'Pax': self.pax,
            'Pick Up Address': self.pickup_location,
            'Drop Off Address': self.dropoff_location,
            'Distance Travelled': self.total_distance,
            'Total Cost': self.total_cost,
            'Status': self.status
        }

    @staticmethod
    def save_to_file(booking, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(booking.to_dict(), indent=4))

    @staticmethod
    def delete_file(filename):
        os.remove(filename)

    @staticmethod
    def from_dict(data):
        vehicle_map = {
            'Car': Car(),
            'Van': Van(),
            'Motorcycle': Motorcycle()
        }
        return Booking(
            date_and_time=data['Date and Time'],
            number=data['Customer No.'],
            booking_id=data['ID']  ,
            user=data['Name'],
            vehicle=data['Vehicle'],
            pax=data['Pax'],
            pickup_location=data['Pick Up Address'],
            dropoff_location=data['Drop Off Address'],
            total_distance=data['Distance Travelled'],
            total_cost=data['Total Cost'],
            status=data['Status']
        )
        