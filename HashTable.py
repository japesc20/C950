class Create_Hashtable:

    # Initialize constructor with optional size parameter
    def __init__(self, size=20):
        # Initialize the hashtable list and append each with an empty bucket list
        self.table = []
        for i in range(size):
            self.table.append([])

    # Insert method that will double as an update method
    def insert(self, key, value):

        # Compute the bucket index for the given key
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Loop over each key:value pair
        # If matches update corresponding value and return True
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = value
                return True

        # If key value does not exist then insert item at end of list
        key_value = [key, value]
        bucket_list.append(key_value)
        return True

    # Search package method
    def search(self, key):

        # Compute the bucket index for the given key
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Iterate over each key value pair in the bucket and return if found
        # kv[0] = package ID
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]

        # Return none if key is not found
        return None

    # Delete package method
    def delete(self, key):

        # Compute the bucket index for the given key
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Iterate over each key value pair in the bucket and remove if found
        if key in bucket_list:
            bucket_list.remove(key)
