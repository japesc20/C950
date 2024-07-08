import csv


# Read the addresses CSV file
def read_address_csv():
    with open("CSVfiles/addresses.csv") as csvfile_add:
        csv_addresses = csv.reader(csvfile_add)
        return list(csv_addresses)


# Read the distances CSV file
def read_distance_csv():
    with open("CSVfiles/distances.csv") as csvfile_dist:
        csv_distances = csv.reader(csvfile_dist)
        return list(csv_distances)


# Read the packages CSV file
def read_package_csv():
    # Read the packages CSV file
    with open("CSVfiles/packages.csv") as csvfile_pack:
        csv_packages = csv.reader(csvfile_pack)
        return list(csv_packages)
