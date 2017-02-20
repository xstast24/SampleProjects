import time
# import csv


class Flights:
    count = 0
    flights = []

    def __init__(self, flight_data):
        Flights.count += 1

        self.data = flight_data.rstrip('\n')
        self.transfers = []
        self.sequences = []
        # save flight details
        flight_data = flight_data.split(',')
        self.id = flight_data[4].rstrip('\n')
        self.source = flight_data[0]
        self.dest = flight_data[1]
        # time of take off and arriving is in seconds since epoque
        self.start = time.mktime(time.strptime(flight_data[2], '%Y-%m-%dT%H:%M:%S'))
        self.end = time.mktime(time.strptime(flight_data[3], '%Y-%m-%dT%H:%M:%S'))

    def save_transfers(self):
        """
        Find all possible transfers for the current flight. Save them to the list of transfers as Flights instance.
        """
        for possible_transfer in Flights.flights:
            # transfer time is limited to 1-4 hours
            if self.end + 3600 <= possible_transfer.start <= self.end + 4*3600 and self.dest == possible_transfer.source:
                self.transfers.append(possible_transfer)

    def get_sequences(self, prev_flights=None, prev_destinations=None):
        if prev_flights is None:
            prev_flights = [self.data]
        if prev_destinations is None:
            prev_destinations = [self.source]
        # TODO add previous destinations control
        # for every available transfer
        for transfer in self.transfers:
            #if transfer.dest not in prev_destinations:
                print(prev_flights + [transfer.data])
                transfer.get_sequences(prev_flights + [transfer.data], prev_destinations + [transfer.source])


# open file
csv = open('input.csv', 'r')
csv = csv.readlines()
del(csv[0])

# get all Flights
for line in csv:
    Flights.flights.append(Flights(line))

# load all available transfers for each flight
for flight in Flights.flights:
    flight.save_transfers()

# print all sequences
for flight in Flights.flights:
    flight.get_sequences()
    print('================================================================================================================\n')
