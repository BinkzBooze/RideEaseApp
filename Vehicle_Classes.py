# Creation of Parent Class (Vehicle)
class Vehicle:
    """ A class representing a vehicle with attributes and methods to calculate trip costs and provide vehicle details.

    Attributes:
        vehicle_type (str): The type of the vehicle (e.g., 'Car', 'Van').
        cost_per_km (float): The cost per kilometer for this vehicle type.
        capacity (int): The maximum number of passengers the vehicle can carry.

    Methods:
        calculate_cost(km):
            Calculates the total cost of a trip based on the distance traveled in kilometers.
        
        get_vehicle_type():
            Returns the type of the vehicle.
    """
    
    def __init__(self, vehicle_type, cost_per_km, capacity):
        self.cost_per_km = cost_per_km
        self.capacity = capacity
        self.vehicle_type = vehicle_type

    def calculate_cost(self, km):
        return 50.00 if km <= 2 else round(50 + (km - 2) * self.cost_per_km, 2)
    
    def get_vehicle_type(self):
        return self.vehicle_type

# Creation of Child Classes (Car, Van, Motorcycle), then overriding cost per km and capacity.
class Car(Vehicle):
    def __init__(self):
        super().__init__(vehicle_type="Car", cost_per_km=15, capacity=6)

class Van(Vehicle):
    def __init__(self):
        super().__init__(vehicle_type="Van", cost_per_km=30, capacity=12)

class Motorcycle(Vehicle):
    def __init__(self):
        super().__init__(vehicle_type="Motorcycle", cost_per_km=10, capacity=1)
