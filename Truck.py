import datetime

class Truck:

    # Initiate Truck parameter constructor
    def __init__(self, capacity, speed, load, packages, mileage, address, departure_time, time):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.departure_time = departure_time
        self.time = departure_time

    # String method for Truck instance
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load, self.packages,
                                               self.mileage, self.address, self.departure_time)

    def update_truck_time(self, time_delta):
        self.time = time_delta