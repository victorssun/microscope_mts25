# turn on all three motors
# for raw input: use control(), for function input use control2()
# raw input (two): motor, step -- moves
# raw input (three): motor, 'goto', position -- goes to
# close motors before exiting?

# motors need to be at rev. limit before turning off
# becareful of function names, pretty common

'''
functions list:
new_move() - in & out (includes time delay)
new_goto() - in & out
savemotors() - in
loadmotors() - in
control() - in
control2() - out (for inputs that can't use variables)
closemotors() - in & out

'''

import pyAPT, time, pickle

def _init_motors():
    # initilizes x, y, z motors
    x = pyAPT.MTS50(serial_number = 27001234)
    y = pyAPT.MTS50(serial_number = 27001328)
    z = pyAPT.MTS50(serial_number = 27001291)
    
    #motorlist = [x, y, z]
    '''
    for each in motorlist:
        each.max_velocity = velocity = 0.23
        each.max_acceleration = 0.45
    '''
    print x.position(), y.position(), z.position()
    return x, y, z #, motorlist

def new_move(motor, step, delay=False):
    # only used with control, adds delay
    time_delay = abs(step)/0.23 + 2 # assume 0.23 mm/s, plus 2 s extra
    motor.move(step)
    if delay == True:
        #time_delay = abs(step)/0.23 + 2 # assume 0.23 mm/s, plus 2 s extra
        time.sleep(time_delay) # TURN OFF FOR FASTER RESPONSE BUT WATCH FOR CONFLICTS

def new_goto(motor, newposition, delay=False):
    # only used with control, adds delay
    time_delay = abs(newposition - motor.position())/0.23 + 2
    motor.goto(newposition)
    if delay == True:
        time.sleep(time_delay)

def savemotors(filename='savexyz.pickle', delay=False):
    # save coords in pickle, and home motors to position 0
    # always run before turning off motors
    coords = [x.position(), y.position(), z.position()]
    print coords
    if raw_input(' pickle coords? (y/n): ') == 'y':
        pickle.dump(coords, open(filename, 'wb'))
        print(' saved coords')
    else:
        print(' not saved')
    homing = raw_input(' home xyz? (y/n): ')
    if homing == 'y':
        new_goto(z, 0.0000) # z first so no clashing
        for each in [x, y]:
            new_goto(each, 0.0000)
        if delay == True:
            longest = max([x.position(), y.position(), z.position()])
            time_delay = abs(longest)/0.23 + 2
            print time_delay
            time.sleep(time_delay)
        print(' homed coords: %f, %f, %f' %(x.position(), y.position(), z.position()))
    else:
        print(' not homed')

def loadmotors(filename='savexyz.pickle', delay=False):
    # print coords & homes motors back to previous position (from position 0, not rev. limit)
    # run after turning on motors to get back to position (if desired)
    coords = pickle.load(open(filename, 'rb'))
    print(' pickled coords: %f, %f, %f' %(coords[0], coords[1], coords[2]))
    if raw_input(' rev. home xyz? (y/n): ') == 'y':
        i = 0
        for each in [x, y, z]:
            new_goto(each, coords[i])
            i = i + 1
        if delay == True:
            time_delay = abs(max(coords))/0.23 + 2 # assume 0.23 mm/s with 2 s
            time.sleep(time_delay)
        print(' rev. homed: %f, %f, %f' %(x.position(), y.position(), z.position()))
    else: 
        print(' not rev. homed')

def control():
    # not enough time delay
    # default run: z down 0.01 mm
    motor = z
    step = .0100

    try:
        while True:
            inputs = raw_input(' input move (motor, step): ')
            inputs = inputs.split()
            if len(inputs) >= 2:
                if inputs[0] == 'x':
                    motor = x
                elif inputs[0] == 'y':
                    motor = y
                elif inputs[0] == 'z':
                    motor = z
                else:
                    print ' motor error'
    
                if len(inputs) == 3: # three inputs: go to position
                #if inputs[1] == 'goto':
                    newposition = float(inputs[2])
                    new_goto(motor, newposition)
                    print (' %s position: %f mm' %(inputs[0], motor.position()))
                elif len(inputs) == 2: # two inputs: move steps
                    step = float(inputs[1]) 
                    new_move(motor, step)
                    print (' %s position: %f mm' %(inputs[0], motor.position()))
            if len(inputs) == 0: # no input: repeat default/last new_move input
                new_move(motor, step)
                print (' r position: %f mm' %(motor.position()))
    except KeyboardInterrupt:
        print '\n control done'

def control2(motor, step, go=False):
    if motor == 'x' or motor == 1:
        motor = x
        motor_id = 'x'
    elif motor == 'y' or motor == 2:
        motor = y
        motor_id = 'y'
    elif motor == 'z' or motor == 3:
        motor = z
        motor_id = 'z'
    else:
        print ' motor error'
    if go == True:
        newposition = float(step)
        new_goto(motor, newposition)
        print (' %s position: %f mm' %(motor_id, motor.position()))
    elif go == False:
        step = float(step)
        new_move(motor, step)
        print (' %s position: %f mm' %(motor_id, motor.position()))

def closemotors():
    # is this really needed?
    for each in [x, y, z]:
        each.close()
        print ' motors closed'

### MAIN CODE

if __name__ == '__main__':
    # run directly for options to load, save, or control
    x, y, z = _init_motors()
    if raw_input(' load? (y/n): ') == 'y':
        loadmotors(delay=True)
        control()
    else:
        control()
    time.sleep(5)
    if raw_input(' save? (y/n): ') == 'y':
        savemotors(delay=True)
    closemotors()
    print('motorcontrol.py ran directly')
else: 
    x, y, z = _init_motors()
    print('motorcontrol.py imported. x, y, z')
