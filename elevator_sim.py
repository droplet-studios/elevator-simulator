"""
Roughly simulates the time people spend waiting for an elevator and reaching their destination floor.
It also can model how having more or less elevators can affect wait times.
"""

import time, random, itertools, os, sys, csv, threading, pandas

floors = []
elevators = []
people = []
finished = []

user_set = {
    'elevators': 2,
    'floors': 10,
    'people_interval': 15,
    'elevator_speed': 3,
    'trips': 5
}

class Person():
    """
    This class handles data relevant to each person
    """

    id_iter = itertools.count()
    
    def __init__(self):
        self.elevator_id = 0
        self.person_id = next(self.id_iter)
        self.start_floor_id = random.randint(0, len(floors) - 1)
        self.dest_floor_id = random.randint(0, len(floors) - 1)
        while self.start_floor_id == self.dest_floor_id:
            self.dest_floor_id = random.randint(0, len(floors) - 1)
        self.start_time = time.time()
    
    def total(self):
        self.total_time = time.time() - self.start_time
        return self.total_time
    
class Elevator():
    """
    This class handles data relevant to each elevator
    """
    
    id_iter = itertools.count()

    def __init__(self):
        self.passengers = []
        self.getting_on = []
        self.getting_off = []
        self.current_floor = 0
        self.going_up = True
        self.elevator_id = next(self.id_iter)
        self.trips = 0

class Floor():
    """
    This class handles data relevant to each floor
    """

    id_iter = itertools.count()

    def __init__(self):
        self.waiting = []
        self.elevator_arrived = False
        self.floor_id = next(self.id_iter)

def get_values(key):
    """
    This processes the user-set parameters, ensuring valid data entry and using default values when appropriate.
    """

    user_input = input(f'Enter the following parameter: \'{key}\' (\'Enter\' for default value of {user_set[key]})\n> ')
    if user_input == '':
        user_input = user_set[key]
    try:
        user_input = int(user_input)
        if user_input <= 0:
            raise ValueError
        user_set[key] = user_input
    except ValueError:
        get_values(key)
    return user_set[key]

def add_person(loop=True):
    """
    This function adds people to random floors. It can loop automatically and keep adding people when appropriate.
    """

    new_person = Person()
    people.append(new_person)
    #print(f'Adding new person with start floor: {new_person.start_floor_id}')
    floors[new_person.start_floor_id].waiting.append(new_person)
    #print(floors[new_person.start_floor_id].waiting)

    if loop:
        time.sleep(user_set['people_interval'])
        add_person()

def prep():
    """
    This function handles user-set parameters and initially updating the display.
    """

    for i in range(get_values('elevators')):
        elevators.append(Elevator())
    for i in range(get_values('floors')):
        floors.append(Floor())
    get_values('people_interval')
    get_values('elevator_speed')
    get_values('trips')

    for i in range(5):
        add_person(loop=False)

    update_display()

def move_elevator(id):
    """
    This function moves the elevator between floors, and switches directions at the top and bottom.
    When appropriate, it automatically calls the update_elevator() function, which in turn calls move_elevator()
    """

    elevator = elevators[id]
    time.sleep(user_set['elevator_speed'])

    if elevator.going_up:
        if elevator.current_floor < (len(floors) - 1):
            elevator.current_floor += 1
        else:
            elevator.current_floor -= 1
            elevator.going_up = False
    else:
        if elevator.current_floor > 0:
            elevator.current_floor -= 1
        else:
            elevator.current_floor += 1
            elevator.going_up = True
    
    if elevator.current_floor == 0:
        elevator.trips += 1

    #print(f'Current floor: {elevator.current_floor}')
    update_display()

    if elevator.trips < user_set['trips']:
        # keep moving elevator only if hasn't reached trip limit
        if not floors[elevator.current_floor].elevator_arrived:
            update_elevator(id, elevator.current_floor)
        else:
            move_elevator(id) # skips floor if elevator already has arrived
    else:
        print(f'Elevator {id} has finished; when all elevators finished, press \'Ctrl + C\' to exit')

def update_elevator(id, floor_id):
    """
    This function handles onboarding and offboarding people from the elevator when appropriate.
    This means that the elevator only onboards and offboards people on the origin and destination floors respectively.
    It also skips floors when another elevator is already on the floor.
    """

    elevator = elevators[id]
    floor = floors[floor_id]

    floor.elevator_arrived = True # other elevator(s) won't stop while onboarding/offboarding happening

    # offboard
    for person in elevator.passengers:
        #print(f'Passenger destination: {person.dest_floor_id}')
        if person.dest_floor_id == elevator.current_floor:
            finished.append(person)
            elevator.getting_off.append(person)
            time.sleep(random.uniform(1,2))
    for person in elevator.getting_off:
        elevator.passengers.remove(person)
    elevator.getting_off = []

    # onboard
    for person in floor.waiting:
        if floor.floor_id == len(floors) - 1:
            pass # skipping passenger pickup for opposite direction doesn't apply at top and bottom
        elif floor.floor_id == 0:
            pass
        elif elevator.going_up and (person.dest_floor_id < floor.floor_id):
                continue    # don't pick up passengers if the elevator is going the wrong direction
        elif not elevator.going_up and (person.dest_floor_id > floor.floor_id):
                continue
        #print(f'Going up: {elevator.going_up}, destination: {person.dest_floor_id}, floor: {floor.floor_id}')   
        elevator.passengers.append(person)
        elevator.getting_on.append(person)
        time.sleep(random.uniform(1,2))
    for person in elevator.getting_on:
        floor.waiting.remove(person)
    elevator.getting_on = []

    floor.elevator_arrived = False

    update_display()
    move_elevator(id)

def update_display():
    """
    Use pandas module to put elevator and floor status into table (visually simulates a high rise building).
    This runs every time a person is added, the elevator moves, or people are onboarded/offboarded. 
    It clears the console every time to have only the most recent table printed.
    """

    os.system('cls' if os.name == 'nt' else 'clear')

    data = {
        'floor': [floor.floor_id for floor in reversed(floors)],
        'waiting': [len(floor.waiting) for floor in reversed(floors)]
    }
    for i in range(len(elevators)):
        data[f'elevator {i}'] = []
        for floor in reversed(floors):
            if floor.floor_id == elevators[i].current_floor:
                data[f'elevator {i}'].append(len(elevators[i].passengers))
            else:
                data[f'elevator {i}'].append('')
    df = pandas.DataFrame(data)
    print(df.to_string(index=False))

    #print([(person.start_floor_id, person.dest_floor_id) for person in floors[9].waiting])

def main():
    threads = []
    
    # use multithreading to run multiple elevators concurrently
    try:
        prep()
        for i in range(len(elevators)):
            threads.append(threading.Thread(target=move_elevator, args=(i,), daemon=True))
        for thread in threads:
            time.sleep(random.random())
            thread.start()
    except KeyboardInterrupt:
        print('')
        print('Exiting...')
        sys.exit()

    # run the following after 'Ctrl + C', which only works after the other processes have exited
    try:
        add_person()
    except KeyboardInterrupt:
        for thread in threads:
            thread.join()

        # print average wait time of finished passengers
        average = sum([person.total() for person in finished]) / len(finished)
        print(f'Average wait time of {average} seconds')

        # save data into csv spreadsheet
        current_time = time.time()
        with open(f'elevator_sim_{current_time}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['person_id', 'total_wait'])
            for person in people:
                writer.writerow([person.person_id, person.total()])
            csvfile.close()
            print(f'Saved data in \'elevator_sim_{current_time}.csv\'')

        print('')
        print('Exiting...')
        sys.exit()

main()