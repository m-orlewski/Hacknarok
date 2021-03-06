import math, time


class Location(object):
    def __init__(self, id, name, address, coords, size):
        self.id = id
        self.name = name
        self.address = address
        self.coords = coords
        self.size = size
        self.queue = []
        self.wait_time = 0
        self.inside = []
        self.times = {}
        self.client_count = 0
        self.time_all_clients = 0


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

    def switch_user(self, customer):
        #If the user in queue and scans the code, he's going inside
        if customer in self.queue and customer not in self.inside:
            self.inside.append(customer)
            self.queue.remove(customer)
            self.times[customer] = time.time()
            return True
        #If the user is inside and scans the code, he's leaving
        elif customer in self.inside and customer not in self.queue:
            self.inside.remove(customer)
            self.client_count += 1
            self.time_all_clients += time.time() - self.times[customer]
            return True

    def estimated_time_wait(self):
        if self.client_count:
            time = int(math.ceil((self.get_queue_size()+1) * int(math.ceil(self.time_all_clients/self.client_count/60))))
            hours = time//60
            minutes = time%60
            time = "{:02d}:{:02d}".format(hours, minutes)
            print("-"* 30)
            print(time)
            print("-"* 30)
            return time
        else:
            return "TBE"

class DB(object):
    def __init__(self):
        self.locations = {}

    def add_location(self, locationID, name, address, coords, size):
        if locationID in self.locations.keys():
            print("Location already exists")
            return False
        self.locations[locationID] = Location(locationID, name, address, coords, size)
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
                'coords': location.coords,
                'queue_size': len(location.queue),
                'inside': len(location.inside),
                'time': location.estimated_time_wait(),
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


    