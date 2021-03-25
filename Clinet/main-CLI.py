import socket
import threading
from Menu import menu
from Parser import Parser

# client will send message on this port
PORT = 10004


def join_chat(sckt):
    username = input('write your username: ')
    msg = f'Hello <{username}>'.encode('utf-8')
    sckt.send(msg)


def leave_chat(sckt):
    msg = 'Bye.'.encode('utf-8')
    sckt.send(msg)


def members_list(sckt):
    msg = 'Please send the list of attendees.'.encode('utf-8')
    sckt.send(msg)


def check_type(info_dict):
    # get type of message and remove it from dictionary
    print('diction: ', info_dict)
    msg_type = info_dict.pop('type')

    if msg_type == 'join':
        username = info_dict.get('username')
        print(f'<{username}> joined the chat room.')

    elif msg_type == 'welcome':
        username = info_dict.get('username')
        print(f'Hi <{username}>, welcome to the chat room.')

    elif msg_type == 'list':
        print('Here is the list of attendees:')
        print(','.join(['<' + username + '>' for username in info_dict.get('usernames')]))

    elif msg_type == 'public':
        print(f'<{info_dict.get("username")}>: {info_dict.get("message")}')

    elif msg_type == 'private':
        print(f'private message from <{info_dict.get("username")}> to you: {info_dict.get("message")}')

    elif msg_type == 'leave':
        print(f'<{info_dict.get("username")}> left the chat room.')


def write_public_message(sckt):
    print('Public Chat (write \'quit\' to main menu)')
    while True:
        text = input()
        if text == 'quit':
            break
        else:
            text_length = len(text.encode('utf-8'))
            msg = f'Public message, length=<{text_length}>:\r\n<{text}>'.encode('utf-8')
            sckt.send(msg)


def listen_for_message(s):
    while True:
        # receive message and decode it
        msg = s.recv(1024).decode('utf-8')
        print('RAW_MESSAGE: ' + msg)  # TODO
        # create a parser object and pass the message to parser
        msg_obj = Parser(msg)
        # call parse method to parse the message and a get a dictionary of message content
        info = msg_obj.parse()
        # check for different types of message types and do the wanted job
        check_type(info)


def main():
    # creating a TCP socket
    sckt = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # connect to specified server
    sckt.connect((socket.gethostname(), PORT))

    # creating a thread that listens to server and processes incoming messages
    t = threading.Thread(target=listen_for_message, args=(sckt,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

    while True:
        # call menu and get selected option
        option = menu()
        if option == 1:
            # join public chat
            join_chat(sckt)
            # write message in public chat
            write_public_message(sckt)
            # if the loop inside 'write_public_message' function breaks user wants to quit public chat
            # and we call leave chat to send leave message to server
            leave_chat(sckt)
        elif option == 2:
            # send private message
            pass
        elif option == 3:
            # send request to get list of members
            members_list(sckt)
        elif option == 0:
            # exit
            exit()


if __name__ == '__main__':
    main()
