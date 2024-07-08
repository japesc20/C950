import datetime
import re
import csv
from csv_reader import read_address_csv, read_distance_csv, read_package_csv
import Truck
from HashTable import Create_Hashtable
from Package import Package


# Assign data variables from csv_reader file
addresses_data = read_address_csv()
distances_data = read_distance_csv()
packages_data = read_package_csv()


# Create an object for each package
# Load all package objects to the hash table
def package_obj(filename, package_hashtable):
    try:
        # Open CSV file
        with open(filename, newline='') as data_package:
            package_info = csv.reader(data_package)

            # Iterate over each row in the CSV file
            for package in package_info:
                if package[5] == "9:00 AM":
                    package[5] = "09:00:00"
                elif package[5] == "10:30 AM":
                    package[5] = "10:30:00"
                # Unpack package data
                package_id, package_address, package_city, package_state, package_zip, \
                    package_deadline, package_weight = package[:7]  # Assuming 7 fields in CSV

                # Set initial status
                package_status = "At Hub"

                # Instantiate Package object with each given field
                p = Package(int(package_id), package_address, package_city, package_state,
                            package_zip, package_deadline, package_weight, package_status)

                # Insert package into hashtable
                package_hashtable.insert(int(package_id), p)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except csv.Error as e:
        print(f"Error reading CSV file '{filename}': {e}")


# Pulling address from csv
def retrieve_address(address_to_find):
    for package_address in addresses_data:
        # If address matches address in csv in [2]
        if address_to_find == package_address[2]:
            # Then return the package ID
            return int(package_address[0])
    # ValueError is address is not found
    raise ValueError(f"No package was found with address {address_to_find}")


# Calculating the address distances between each other
def addresses_distances(x, y):
    # Setting the distance variable from distance CSV
    distance_between = distances_data[x][y]

    # Handling missing distances
    if distance_between == '':
        distance_between = distances_data[y][x]
    if distance_between == '':
        return 0.0
    return float(distance_between)


# Verify valid time format for UI prompt
def is_valid_time_format(user_time):
    # Regular expression to match HH:MM format
    pattern = re.compile(r'^\d{2}:\d{2}$')
    return pattern.match(user_time)


# Create the first truck object
# Truck 1 = 16 packages (max), 18mph (max), load none,
# array of packages, initial mileage, Start at hub address, departure time
truck_1 = Truck.Truck(16, 18, None, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=8, minutes=0), datetime.timedelta(hours=0, minutes=0))

# Create second truck object
# 16 packages, 18 mph, load none, array of packages, initial mileage,
# start at hub address, departure time = 9:05am due to waiting on correct address for package
truck_2 = Truck.Truck(16, 18, None, [3, 6, 18, 24, 25, 26, 27, 28, 32, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=9, minutes=5), datetime.timedelta(hours=0, minutes=0))

# Create third truck object
# 16 packages, 18 mph, load none, array of packages, initial mileage,
# start at hub address, departure time = 10:20am due to packages arriving
truck_3 = Truck.Truck(16, 18, None, [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 33], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20), datetime.timedelta(hours=0, minutes=0))


# Create hash table
package_hashtable = Create_Hashtable()

# Load all package data into hash table
package_obj("CSVfiles/packages.csv", package_hashtable)


# Delivering packages method (Nearest Neighbor Algorithm)
def deliver_packages(truck):

    try:
        # Initialize a list to store packages en route list
        en_route = [package_hashtable.search(package_id) for package_id in truck.packages]

        # Clear the truck's packages list to append sorted packages
        truck.packages.clear()

        while en_route:

            # Initialize variables for the next closest address and package
            next_address = float('inf')
            next_package = None

            # Loop through each package in en_route list to find the nearest one
            for package in en_route:
                # Special handling for package 9 to update its address at 10:20am
                if package.package_id == 9 and truck.time >= datetime.timedelta(hours=10, minutes=20):
                    package.address = "410 S State St"
                    package.zip_code = "84111"

                distance = addresses_distances(retrieve_address(truck.address), retrieve_address(package.address))

                # Special handling for packages 6, 25, 28, 32
                if package.package_id in [6, 25, 28, 32] and next_address == float('inf'):
                    next_address = distance
                    next_package = package

                # Finds the next nearest package
                if distance < next_address:
                    next_address = distance
                    next_package = package

            # Add the closest package to the truck's delivery list and remove from en_route list
            truck.packages.append(next_package.package_id)
            en_route.remove(next_package)
            truck.mileage += next_address

            # Check if the truck exceeds the mileage limit
            if truck.mileage > 140:
                print("Warning: Distance limit exceeded!")
                return False

            # Update truck's address and time
            truck.address = next_package.address
            truck.time += datetime.timedelta(hours=next_address / 18)
            next_package.delivery_time = truck.time
            next_package.departure_time = truck.departure_time

        return True

    # Error handling for any missing package ID
    except KeyError as e:
        print(f"Error: Package ID {e.args[0]} not found in hashtable.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


# Method calls for each truck
deliver_packages(truck_1)
deliver_packages(truck_2)

# Ensure truck 2 does not leave until either truck 1 or 3 return to hub
truck_2.departure_time = min(truck_1.departure_time, truck_2.time)
deliver_packages(truck_3)


class Main:

    total_truck_mileage = truck_1.mileage + truck_2.mileage + truck_3.mileage

    # User Interface Begins

    print("\nWelcome To: ")
    print("WGUPS (Western Governors Univ. Parcel Service) Service Center\n")

    print("The overall mileage for all trucks is: ")
    print(total_truck_mileage)
    # print(f"Total mileage for Truck 1 is {truck_1.mileage}")
    # print(f"Total mileage for Truck 2 is {truck_2.mileage}")
    # print(f"Total mileage for Truck 3 is {truck_3.mileage}")

    while True:
        # Prompt the user to actually begin the program
        user_start = input("Do you want to continue? (y/n)\n")
        truck_num = ''

        if user_start.lower() == 'y':
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
                # User is prompted to view an individual package or all packages
                package_input = input(
                    "To view an individual package please type 'single'. To view all packages please type 'all'.\n")

                # Handle single package view
                if package_input == "single":
                    try:
                        single_input = input("Enter the numeric package ID\n")
                        package = package_hashtable.search(int(single_input))

                        # Update package status and delivery time based on user input time
                        package.updateStatus(time_delta)
                        package.updateDeliveryTime(time_delta)
                        # Update package 9 address
                        package.updatePack9(time_delta)

                        # Determine which truck the package belongs to
                        if package.package_id in truck_1.packages:
                            truck_num = 1
                        elif package.package_id in truck_2.packages:
                            truck_num = 2
                        elif package.package_id in truck_3.packages:
                            truck_num = 3

                        print(str(package) + f" with Truck {truck_num}")

                    except ValueError:
                        print("Invalid input. Exiting program.")
                        exit()

                # Handle view of all packages
                elif package_input == "all":
                    try:
                        for package_id in range(1, 41):
                            package = package_hashtable.search(package_id)

                            # Update package status and delivery time based on user input time
                            package.updateStatus(time_delta)
                            package.updateDeliveryTime(time_delta)
                            # Update package 9 address
                            package.updatePack9(time_delta)

                            # Determine which truck the package belongs to
                            if package.package_id in truck_1.packages:
                                truck_num = 1
                            elif package.package_id in truck_2.packages:
                                truck_num = 2
                            elif package.package_id in truck_3.packages:
                                truck_num = 3

                            print(str(package) + f" with Truck {truck_num}")

                    except ValueError:
                        print("Invalid input. Exiting program.")
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