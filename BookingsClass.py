import sqlite3
from Vehicle_Classes import Car, Van, Motorcycle

# Creation of User's Booking Information
class Booking:

    def __init__(self, user, pickup_location, dropoff_location, date_and_time, pax, vehicle, total_distance, total_cost, status, booking_number=None):
        self.booking_number = booking_number
        self.user = user
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.date_and_time = date_and_time
        self.pax = pax
        self.vehicle = vehicle
        self.total_distance = total_distance
        self.total_cost = total_cost
        self.status = status

    def save_to_db(self, db_filename, db_tablename):
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{db_tablename}" (
                "Booking No." INTEGER PRIMARY KEY AUTOINCREMENT,
                "Username" TEXT,
                "Pickup Address" TEXT,
                "Dropoff Address" TEXT,
                "Date and Time" TEXT,
                "Vehicle Type" TEXT,
                "Pax" INTEGER,
                "Total Distance" REAL,
                "Total Cost" REAL,
                "Status" TEXT
        )''')
        cursor.execute(f'''INSERT INTO "{db_tablename}" (
            "Booking No.", "Username", "Pickup Address", "Dropoff Address", "Date and Time", "Pax", "Vehicle Type", "Total Distance", "Total Cost", "Status"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',(
            self.booking_number,
            self.user,
            self.pickup_location,
            self.dropoff_location,
            self.date_and_time,
            self.pax,
            self.vehicle,
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
    def from_db(cls, booking_number, db_filename, db_tablename):
        conn = sqlite3.connect(db_filename)
        c = conn.cursor()
        c.execute(f'SELECT * FROM "{db_tablename}" WHERE "Booking No." = ?', (booking_number,))
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
