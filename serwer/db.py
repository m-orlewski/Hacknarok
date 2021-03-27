class Location(object):
    def __init__(self, id, name, address, size):
        self.id = id
        self.name = name
        self.address = address
        self.size = size
        self.queue = []
        self.wait_time = 0
        self.inside = []

    def __str__(self):
        return f'-----\nLokacja: {self.id}\nNazwa: {self.name}\nAdres: {self.address}\nRozmiar: {self.size}\nKolejka: {self.queue}\nW kolejce: {self.get_queue_size()}\n-----'

    def get_max_customers(self):
        if self.size <= 100:
            return self.size//15 if self.size//15 > 0 else 1
        else:
            return self.size//20

    def get_queue_size(self):
        return len(self.queue)

    def add_to_queue(self, customer):
        if customer in self.queue:
            print("already in queue")
            return False
        self.queue.append(customer)
        return True

    def remove_from_queue(self, customer):
        if customer not in self.queue:
            print("can't remove if you're not in queue")
            return False
        else:
            self.queue.remove(customer)
            return True
            
    def went_inside(self, customer):
        if customer not in self.inside or customer not in self.queue:
            print("Not in queue and not inside")
            return False
        self.inside.append(customer)
        self.queue.remove(customer)
        return True

    def left(self, customer):
        if customer not in self.inside or customer not in self.queue:
            print("Not in queue and not inside")
            return False
        self.inside.remove(customer)
        return True

class DB(object):
    def __init__(self):
        self.locations = {}

    def add_location(self, locationID, name, address, size):
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

    def queue_index(self, customerID):
        for location in self.locations.values():
            if customerID in location.queue:
                return (location.id, location.queue.index(customerID)+1, location.wait_time)
        return 0

    def get_all(self):
        return_data = []
        for location in self.locations.values():
            dc = {
                'name': location.name,
                'id': location.id,
                'address': location.address,
                'queue_size': len(location.queue),
                'inside': len(location.inside),
                'max_size': location.get_max_customers()
            }
            return_data.append(dc)
        return return_data



if __name__ == "__main__":
    db = DB()
    db.add_location(123123, 'abc', 'ul', 120)
    db.add_location(123123, 'abc', 'ul', 120)
    db.add_location(1, 'xyz', 'al', 1000)
    
    print(db.get_location(123123))
    print(db.get_location(1))

    customer_1 = Customer(1)
    customer_2 = Customer(2)
    customer_3 = Customer(3)

    db.get_location(123123).add_to_queue(customer_1)
    db.get_location(123123).add_to_queue(customer_3)
    db.get_location(123123).add_to_queue(customer_2)

    print(db.get_location(1))
    print(db.get_location(123123))

    print(db.queue_index(customer_1.customerID))
    print(db.queue_index(customer_2.customerID))
    print(db.queue_index(customer_3.customerID))


    