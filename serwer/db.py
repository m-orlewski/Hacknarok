class Customer(object):
    def __init__(self, customerID):
        self.customerID = customerID

class Location(object):
    def __init__(self, id, name, address, size, queue=[]):
        self.id = id
        self.name = name
        self.address = address
        self.size = size
        self.queue = queue

    def __str__(self):
        return f'-----\nLokacja: {self.id}\nNazwa: {self.name}\nAdres:{self.address}\nRozmiar:{self.size}\nKolejka:{self.queue}\n---'

    def get_max_customers(self):
        if self.size <= 100:
            return self.size//15
        else:
            return self.size//20

    def add_to_queue(self, customer):
        if customer.customerID in self.queue:
            print("already in queue")
            return
        if len(self.queue) < self.get_max_customers():
            self.queue.append(customer)
        else:
            print("queue is full")

    def remove_from_queue(self, customer):
        if customer.customerID not in self.queue:
            print("can't remove if you're not in queue")
        else:
            self.queue.remove(customer)

class DB(object):
    def __init__(self):
        self.locations = {}

    def add_location(self, locationID, name, address, size):
        #Sprawdz czy lokalizacja nie zostala juz dodana
        print(self.locations)
        if locationID in self.locations.keys():
            print("Location already exists")
            return False
        self.locations[locationID] = Location(locationID, name, address, size)
        print(self.locations)
        return True

    def get_location(self, locationID):
        if locationID in self.locations.keys():
            return self.locations[locationID]

    def get_all(self):
        return_data = []
        for location in self.locations.values():
            dc = {
                'name': location.name,
                'id': location.id,
                'address': location.address,
                'queue_size': len(location.queue),
                'max_size': location.get_max_customers()
            }
            return_data.append(dc)
        return return_data

if __name__ == "__main__":
    db = DB()
    db.add_location(123123, 'abc', 'ul', 120)
    
    print(db.get_all())