# C950: Data Structures and Algorithms II - Task 2
# Student ID: 010616446

import datetime
import re
import csv
import Truck
from HashTable import Create_Hashtable
from Package import Package


# Read the addresses CSV file
with open("CSVfiles/addresses.csv") as csvfile_add:
    csv_addresses = csv.reader(csvfile_add)
    csv_addresses = list(csv_addresses)

# Read the distances CSV file
with open("CSVfiles/distances.csv") as csvfile_dist:
    csv_distances = csv.reader(csvfile_dist)
    csv_distances = list(csv_distances)

# Read the packages CSV file
with open("CSVfiles/packages.csv") as csvfile_pack:
    csv_packages = csv.reader(csvfile_pack)
    csv_packages = list(csv_packages)


# Create an object for each package
# Load all package objects to the hash table
def package_obj(filename, package_hashtable):
    with open(filename) as data_package:
        package_info = csv.reader(data_package)
        for package in package_info:
            p_id = int(package[0])
            p_address = package[1]
            p_city = package[2]
            p_state = package[3]
            p_zip = package[4]
            p_deadline = package[5]
            p_weight = package[6]
            p_status = "At Hub"

            # Instantiate package object
            p = Package(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_weight, p_status)

            # Insert all data in new hash table
            package_hashtable.insert(p_id, p)

            # print(package)


# Pulling address from csv
def retrieve_address(address):
    for row in csv_addresses:
        if address in row[2]:
            return int(row[0])


# Calculate the distance between two addresses
def distance_between_addresses(x, y):
    distance = csv_distances[x][y]

    # Handling missing distances
    if distance == '':
        distance = csv_distances[y][x]
    if distance == '':
        return 0.0
    return float(distance)


# Verify valid time format for UI prompt
def is_valid_time_format(user_time):
    # Regular expression to match HH:MM format
    pattern = re.compile(r'^\d{2}:\d{2}$')
    return pattern.match(user_time)


# Create the first truck object
# Truck 1 = 16 packages (max), 18mph (max), load none,
# array of packages, initial mileage, Start at hub address, departure time
truck_1 = Truck.Truck(16, 18, None, [4, 7, 10, 12, 21, 23, 26, 29, 31, 34, 37, 40], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=8, minutes=0))

# Create second truck object
# 16 packages, 18 mph, load none, array of packages, initial mileage,
# start at hub address, departure time = 10:20 due to waiting on correct address for package
truck_2 = Truck.Truck(16, 18, None, [1, 3, 6, 13, 14, 15, 16, 18, 19, 20, 25, 28, 32, 36, 38], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Create third truck object
# 16 packages, 18 mph, load none, array of packages, initial mileage,
# start at hub address, departure time = 9:05am due to packages arriving
truck_3 = Truck.Truck(16, 18, None, [2, 5, 8, 9, 11, 17, 22, 24, 27, 30, 33, 35, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))


# Create hash table
package_hashtable = Create_Hashtable()

# Load all package data into hash table
package_obj("CSVfiles/packages.csv", package_hashtable)


# Delivering packages method (Nearest Neighbor Algorithm)
def deliver_packages(truck):

    # Initiated an empty list for packages that are en route (not delivered)
    en_route = []

    # Loop through packages from ID in hash table and append to en_route list
    for package_id in truck.packages:
        package = package_hashtable.search(package_id)
        en_route.append(package)

    # Clears package list from truck so sorted list can be appended
    truck.packages.clear()

    while len(en_route) > 0:

        # Initial values for next address and package
        next_address = 999
        next_package = None

        # Loop through each package in en_route list
        for package in en_route:

            # Package ID 25 & 6 are delayed until 9:05a but need to be delivered by 10:30a
            if package.package_id in [25, 6]:
                next_address = distance_between_addresses(retrieve_address(truck.address),
                                                          retrieve_address(package.address))
                next_package = package

            if distance_between_addresses(retrieve_address(truck.address),
                                          retrieve_address(package.address)) <= next_address:
                next_address = distance_between_addresses(retrieve_address(truck.address),
                                                          retrieve_address(package.address))
                next_package = package

        truck.packages.append(next_package.package_id)
        en_route.remove(next_package)
        truck.mileage += next_address

        # Warning message: If total mileage exceeded a max limit of 140 miles
        if truck.mileage > 140:
            print("Warning: Distance limit exceeded!")
            return False

        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.departure_time

    return True


# Method calls for each truck
deliver_packages(truck_1)
deliver_packages(truck_2)

# Ensure truck 2 does not leave until either truck 1 or 3 return to hub
truck_2.departure_time = min(truck_1.departure_time, truck_2.time)
deliver_packages(truck_3)


class Main:
    # User Interface Begins

    print("\nWelcome To: ")
    print("Western Governors University Parcel Service (WGUPS) Center \n")

    print("The overall mileage is: ")
    print(truck_1.mileage + truck_2.mileage + truck_3.mileage)
    # print(truck_1.mileage)
    # print(truck_2.mileage)
    # print(truck_3.mileage)

    while True:

        # Prompt the user to actually begin the program
        user_start = input("Do you want to continue? (y/n)\n")

        if user_start.lower() == "y":
            while True:
                # User is prompted to give a time with given format
                user_time = input("Enter the time to check on your package(s). Use the format, HH:MM\n")

                # Handle errors with wrong time format
                if is_valid_time_format(user_time):
                    try:
                        h, m = map(int, user_time.split(":"))
                        if 0 <= h < 24 and 0 <= m < 60:
                            time_delta = datetime.timedelta(hours=h, minutes=m)
                            break
                        else:
                            print(
                                "Invalid time. Hours must be between 00 and 23, and minutes must be between 00 and 59.")
                    except ValueError:
                        print("Invalid input. Please enter the time in HH:MM format.")
                else:
                    print("Invalid format. Please enter the time in HH:MM format.")

            try:
                # User is prompted to view one or all package(s)
                package_input = input(
                    "To view a individual package please type 'single'. To view all packages"
                    " please type 'all'.\n")

                # 'Single' requires package ID
                if package_input == "single":
                    try:
                        # Prompted to input package ID
                        single_input = input("Enter the numeric package ID\n")
                        package = package_hashtable.search(int(single_input))

                        # Retrieve package status -- else 'package is not found'
                        if package is not None:
                            package.updateStatus(time_delta)
                            print(str(package))
                        else:
                            print(f"Package with ID {single_input} not found.")

                    except ValueError:
                        print("Entry invalid. Closing program.")
                        exit()

                # 'all' will display all packages statuses
                elif package_input == "all":
                    try:
                        for package_id in range(1, 41):
                            package = package_hashtable.search(package_id)
                            package.updateStatus(time_delta)
                            print(str(package))
                    except ValueError:
                        print("Entry invalid. Closing program.")
                        exit()
                else:
                    exit()

            except ValueError:
                print("Invalid input. Please enter the time in HH:MM format.")
                exit()

        elif input != "y":
            print("Have a good day!")
            print("Program Exited")
            exit()