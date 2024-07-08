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
        if self.delivery_time is not None and isinstance(self.delivery_time, datetime.timedelta):
            if self.delivery_time < time_delta:
                self.status = "Delivered"
            elif self.departure_time is not None and self.departure_time < time_delta:
                self.status = "En Route"
            else:
                self.status = "At the Hub"

    def updateDeliveryTime(self, time_delta):
        if self.delivery_time is not None and isinstance(self.delivery_time, datetime.timedelta):
            if time_delta < self.delivery_time:
                self.delivery_time = "Unknown"

    def updatePack9(self, time_delta):
        if (self.package_id == 9) and (time_delta <= datetime.timedelta(hours=10, minutes=20)):
            self.address = "300 State St"
            self.zip_code = "84103"
        elif self.package_id == 9:
            self.address = "410 S State St"
            self.zip_code = "84111"