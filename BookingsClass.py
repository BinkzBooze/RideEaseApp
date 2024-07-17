import sqlite3
from Vehicle_Classes import Car, Van, Motorcycle

# Creation of User's Booking Information
class Booking:
    booking_number = 1

    def __init__(self, user, pickup_location, dropoff_location, date_and_time, pax, vehicle, total_distance, status, number=None):
        if number is not None:
            self.booking_number = number
            Booking.booking_number = max(Booking.booking_number, number + 1)
        else:
            self.booking_number = Booking.booking_number
            Booking.booking_number+= 1

        self.user = user
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.date_and_time = date_and_time
        self.pax = pax
        self.vehicle = vehicle
        self.total_distance = total_distance
        self.total_cost = self.vehicle.calculate_cost(total_distance)
        self.status = status

    @staticmethod
    def save_to_db(self, db_filename):
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
            Booking_Number INTEGER PRIMARY KEY,
            Username TEXT,
            Pickup_Location TEXT,
            Dropoff_Location TEXT,
            Date_and_Time TEXT,
            Pax INTEGER,
            Vehicle_Type TEXT,
            Total_Distance REAL,
            Total_Cost REAL,
            Status TEXT,
        )''')
        cursor.execute('''INSERT INTO bookings (
            Booking_Number, Username, Pickup_Location, Dropoff_Location, Date_and_Time, Pax, Vehicle_Type, Total_Distance, Total_Cost, Status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',(
            self.booking_number,
            self.user,
            self.pickup_location,
            self.dropoff_location,
            self.date_and_time,
            self.pax,
            self.vehicle.__class__.__name__,
            self.total_distance,
            self.total_cost,
            self.status
        ))
        conn.commit()
        conn.close()

    def delete_from_db(self, booking_number, db_filename):
        conn = sqlite3.connect(db_filename)
        c = conn.cursor()
        c.execute('DELETE FROM bookings WHERE booking_number = ?', (booking_number,))
        conn.commit()
        conn.close()

    @classmethod
    def from_db(cls, booking_id, db_filename):
        conn = sqlite3.connect(db_filename)
        c = conn.cursor()
        c.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,))
        row = c.fetchone()
        conn.close()
        if row:
            vehicle_map = {
                'Car': Car(),
                'Van': Van(),
                'Motorcycle': Motorcycle()
            }
            return cls(
                booking_number=row[0],
                user=row[1],
                pickup_location=row[2],
                dropoff_location=row[3],
                date_and_time=row[4],
                pax=row[5],
                vehicle=vehicle_map[row[6]],
                total_distance=row[7],
                total_cost=row[8],
                status=row[9],
            )
        return None
