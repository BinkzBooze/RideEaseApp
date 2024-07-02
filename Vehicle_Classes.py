############################DAGDAGAN YUNG RECEIPT###############

# Creation of Parent Class (Vehicle)
class Vehicle:
    def __init__(self, vehicle_type, cost_per_km, capacity):
        self.cost_per_km = cost_per_km
        self.capacity = capacity

    def calculate_cost(self, km):
        return 50.00 if km <= 2 else round(50 + (km - 2) * self.cost_per_km, 2)
    
    def get_vehicle_type(vehicle_type):
        return vehicle_type

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

    


