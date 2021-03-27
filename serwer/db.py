class Customer(object):
    def __init__(self, customerID):
        self.customerID = customerID

class Location(object):
    def __init__(self, id, name, address, size):
        self.id = id
        self.name = name
        self.address = address
        self.size = size
        self.queue = []

    def __str__(self):
        return f'-----\nLokacja: {self.id}\nNazwa: {self.name}\nAdres:{self.address}\nRozmiar:{self.size}\nKolejka:{self.queue}\n---'

    def get_max_customers(self):
        if self.size <= 100:
            return self.size//15
        else:
            return self.size//20

    def add_to_queue(self, customer):
        for c in self.queue:
            if customer.customerID == c.customerID: 
                print("already in queue")
                return False
        if len(self.queue) < self.get_max_customers():
            self.queue.append(customer)
            return True
        else:
            print("queue is full")
            return False

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
        if locationID in self.locations.keys():
            print("Location already exists")
            return False
        self.locations[locationID] = Location(locationID, name, address, size)
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
    db.add_location(1, 'xyz', 'al', 1000)
    
    print(db.get_location(123123))
    print(db.get_location(1))

    customer_1 = Customer(1)
    customer_2 = Customer(2)
    customer_3 = Customer(3)

    k = db.get_location(123123)
    k.add_to_queue(customer_1)
    # db.get_location(123123).add_to_queue(customer_3)
    # db.get_location(123123).add_to_queue(customer_2)

    print(db.get_location(1))
    print(db.get_location(123123))