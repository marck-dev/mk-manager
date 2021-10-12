#!/usr/env Python
import os

DICT = {
    'conn': 'conectado',
    'disconn': 'desconectado',
    'port': 'Puerto',
    'status': 'Estado',
    'position': 'Posición'
}
E_CHAR = "\033"
EXIT_CHAR = 'q'



def get_devices():
    data = os.popen("xrandr -q | grep -i '[aA-zZ]*-[0-9] [c|d]' -o")
    data = data.readlines()
    devices = [] # {port: _____, status: _____ }
    for line in data:
        arr_data = line.split()
        if len(arr_data) < 2:
            continue
        tmp= {
            'port': arr_data[0],
            'status': DICT['conn'] if arr_data[1] == 'c' else DICT['disconn'],
            '_status': arr_data[1] == 'c'
        }
        devices.append(tmp)
    return devices


# --------------------------------------------------------------------
#                        ______     _       _   
#                        | ___ \   (_)     | |  
#                        | |_/ / __ _ _ __ | |_ 
#                        |  __/ '__| | '_ \| __|
#                        | |  | |  | | | | | |_ 
#                        \_|  |_|  |_|_| |_|\__|
# --------------------------------------------------------------------

# PRINT EXIT INFO                       
def print_exit():
    print("To quit type q or Control-C")


# PRINT DEVICES LIST
def print_device_list(devices):    
    print('\n\033[0;36m%5s%10s %20s\033[36:1m' % ('ID', DICT['port'], DICT['status']))
    print("-"*40)
    print("\033[0m", end="")
    for i,device in enumerate(devices):
        if device['_status']:
            print("\033[0m%5d%10s \033[32;1m%20s\033[0m" % (i,device['port'], device['status']))
        else:
            print("\033[0m%5d%10s \033[31;1m%20s\033[0m" % (i,device['port'], device['status']))
    print('\033[36:1m', end='')
    print("-"*40, end="\033[0m\n")


# PRINT POSITION LIST
def print_positions(target, base, poss):
    os.system('clear')
    print('\n\033[0;36m%-5s%10s \033[36:1m' % ('ID', DICT['position']))
    print("-"*40)
    print("\033[0m", end="")
    for i,pos in enumerate(poss):
        print("\033[0m%-5d %10s \033[0m" % (i, "{} {} {}".format(target['port'],pos,base['port'])))
    print('\033[36:1m', end='')
    print("-"*40, end="\033[0m\n")


# PRINT ROATION LIST
def print_rotate(poss):
    os.system('clear')
    print('\n\033[0;36m%-5s%10s \033[36:1m' % ('ID', DICT['position']))
    print("-"*40)
    print("\033[0m", end="")
    for i,pos in enumerate(poss):
        print("\033[0m%-5d %10s \033[0m" % (i, pos))
    print('\033[36:1m', end='')
    print("-"*40, end="\033[0m\n")

# --------------------------------------------------------------------
#             _____ _____ _      _____ _____ _____ 
#            /  ___|  ___| |    |  ___/  __ \_   _|
#            \ `--.| |__ | |    | |__ | /  \/ | |  
#             `--. \  __|| |    |  __|| |     | |  
#            /\__/ / |___| |____| |___| \__/\ | |  
#            \____/\____/\_____/\____/ \____/ \_/
# --------------------------------------------------------------------

def select_device(devices):
    print_device_list(devices)
    print_exit()
    print("Select the display ID: ", end="")
    id = input()
    check_if_exit(id)
    if not id:
        id = 0
    if int(id) >= len(devices):
        print("\033[0;31mID {} is invalid!".format(id))
        exit(0x001d)
    return devices[int(id)]

def select_position(target, base):
    poss = ["right of", "left of", "above", "below", "same as"]
    print_positions(target, base, poss)
    print_exit()
    id = input('Select the position id of the display: ')
    check_if_exit(id)
    id = int(id)
    if id >= len(poss):
        print("\033[0;31mID {} is invalid!".format(id))
        exit(0x001e)
    return poss[id]

def select_rotation():
    rotations=["normal","inverted","left","right"]
    os.system('clear')
    print_rotate(rotations)
    print_exit()
    id = input('Select the rotation id [0]: ')
    if not id:
        return False
    check_if_exit(id)
    id = int(id)
    return rotations[id]


def check_if_exit(data):
    if data == EXIT_CHAR:
        exit(0)
    try:
        data = int(data)
    except Exception as e:
        print("\033[0;31mChars are invalid, only number are allowed!\033[0m")


def build_command(target, auto=True, 
                  base=False,
                  position=False,
                  primary=False,
                  rotate=False):
    # os.system('clear')
    print('Building the command')
    cmd = 'xrandr --output %s' % target['port']
    if auto:
        cmd = cmd + " --auto"
    if base and position:
        cmd = cmd + " --{} {}".format(position.replace(' ', '-'), base['port'])
    if primary:
        cmd = cmd + " --primary"
    if rotate:
        cmd = cmd + " --rotate {}".format(rotate)
    print("Command to run: {}".format(cmd))
    print('Running the commnad...')
    out = os.popen(cmd)
    print("\n".join(out.readlines()))
    print('Finish.')
    return {
            'target': target,
            'base': base,
            'rotate': rotate,
            'primary': primary,
            'auto': auto,
            'position':position
            }
    

def main():
    devices = get_devices()
    base_index = 0
    auto = True
    os.system('clear')
    target = select_device(devices)
    # print("="*80)
    os.system('clear')
    print("Select the base display, default is 0\n")
    base = select_device(devices)
    if not base:
        base = devices[base_index]
    position = select_position(target, base)
    rotation = select_rotation()
    os.system('clear')
    primary = input("Make {} as primary display [y/n]:".format(target['port']))
    primary = primary == 'y'
    os.system('clear')
    return  build_command(target,auto,base,position, primary, rotation)
