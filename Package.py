import datetime

class Package:

    # Initiate package parameter constructor
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    # String method for Package instance
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.city, self.state, self.zip_code, self.deadline, self.weight, self.delivery_time, self.status)


# Updating status of package
    # If delivery time is less than time difference it is recorded at "Delivered", is greater than currently en route,
    # otherwise package is currently still at Hub.
    def updateStatus(self, time_delta):
        if self.delivery_time is not None and self.delivery_time < time_delta:
            self.status = "Delivered"
        elif self.departure_time is not None and self.departure_time < time_delta:
            self.status = "En Route"
        else:
            self.status = "At the Hub"
