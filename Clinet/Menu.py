import os

"""
menu for CLI
"""


def menu_options():
    print('[1] join chat')
    print('[2] private message (not implemented on client)')
    print('[3] list of members')
    print('[0] exit')


def menu():
    while True:
        os.system('clear')
        menu_options()
        option = int(input('Enter option: '))
        print(f'You chose {option}')
        return option
