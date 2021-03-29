import socket
import threading
from Parser import Parser
from User import User

# server will listen on this port
PORT = 10001
# all connected clients will be stored in this list
connected_users = []


def get_username_of_client(client_socket):
    """
    gets client socket and return its username
    """
    for client in connected_users:
        if client.client_socket == client_socket:
            return client.username


def join_member(client_socket, addr, username):
    """
    add new client to connected users
    and send message to other clients
    """
    # create a user object with username and its client socket and addr
    user = User(client_socket, addr, username)
    # add user to connected users
    connected_users.append(user)

    # create message that has to be send and encode it
    msg = f'<{user.username}> joined the chat room.'.encode('utf-8')
    # send message to other clients that are connected to server
    for client in connected_users:
        # send member joined message to all user except the user that joined now
        if client.username != username:
            client.client_socket.send(msg)
            # send list of all users to update on client side
            # list_members(client.client_socket)

    # send message for newly joined user and list of other members
    msg = f'Hi <{username}>, welcome to the chat room.'
    print(msg)
    client_socket.send(msg.encode('utf-8'))


def leave_member(username):
    """
    send leave message to all users
    """
    # create message that has to be send and encode it
    msg = f'<{username}> left the chat room.'.encode('utf-8')
    print(msg)
    # send message to all users except the new client that connected
    for client in connected_users:
        if client.username != username:
            client.client_socket.send(msg)
            # list_members(client.client_socket)


def list_members(client_socket):
    """
    send list of all members to client
    """
    # create message that has to be send
    msg = 'Here is the list of attendees:\r\n'
    msg += ','.join('<' + user.username + '>' for user in connected_users)

    print(msg)
    client_socket.send(msg.encode('utf-8'))


def public_message(client_socket, msg_len, message):
    """
    send public message to all clients
    """
    # get username of the client that send the message
    username = get_username_of_client(client_socket)
    # create message and send to all user
    msg = f'Public message from <{username}>, length=<{msg_len}>:\r\n<{message}>'
    print(msg)
    for user in connected_users:
        user.client_socket.send(msg.encode('utf-8'))


def private_message(client_socket, msg_len, message, usernames):
    """
    send private message to specified username
    """
    username = get_username_of_client(client_socket)
    # create message that has to be send
    msg = f'Private message, length=<{msg_len}> from <{username}> to '
    msg += ','.join(['<' + username + '>' for username in usernames]) + '\r\n' + f'<{message}>'

    print(msg)
    # send message to wanted users
    for client in connected_users:
        # check if user in in usernames list
        if client.username in usernames:
            client.client_socket.send(msg.encode('utf-8'))


def check_type(info_dict, client_socket, addr):
    """
    check for the type of te message
    and call the proper function
    """
    # get type of message and remove it
    msg_type = info_dict.pop('type')

    # check for type of job that has to be done
    if msg_type == 'join':
        join_member(client_socket, addr, info_dict.get('username'))

    elif msg_type == 'leave':
        username = get_username_of_client(client_socket)
        leave_member(username)

    elif msg_type == 'list':
        list_members(client_socket)

    elif msg_type == 'public':
        public_message(client_socket, info_dict.get('length'), info_dict.get('message'))

    elif msg_type == 'private':
        private_message(client_socket, info_dict.get('length'), info_dict.get('message'), info_dict.get('users'))


def remove_client(client_socket):
    """
    remove a user from connected user
    and when a user remove message will send to all connected users
    """
    disconnected_user = ''

    for user in connected_users:
        # find a user with specified client socket
        if user.client_socket == client_socket:
            # save username for sending message to other users
            disconnected_user = user.username[:]
            # pop user from list
            connected_users.remove(user)

    # send message to all clients that are connected
    leave_member(disconnected_user)


def listen_for_client(client_socket, addr):
    """
    keeps listening for a message from client_socket
    """
    while True:
        try:
            # keep listening for a message from 'client_socket'
            msg = client_socket.recv(1024).decode('utf-8')
            # print all messages that come from clients
            print(msg)
            # create a parser object and pass the message to parser
            msg_obj = Parser(msg)
            # call parse method to parse the message and a get a dictionary of message content
            info_dict = msg_obj.parse()
            # check for different types of message types and do the wanted job
            check_type(info_dict, client_socket, addr)

        except Exception as e:
            # client no longer connected
            # remove client from connected users list
            remove_client(client_socket)
            break


def main():
    # create a TCP socket
    sckt = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # bind the socket to the host address which is 127.0.0.1
    sckt.bind((socket.gethostname(), PORT))
    # listen for upcoming connections
    sckt.listen(10)

    print(f'server is listening on port {PORT}!')

    while True:
        # accept request from a client
        client_socket, addr = sckt.accept()
        # start a new thread that listens for each client's messages
        t = threading.Thread(target=listen_for_client, args=(client_socket, addr))
        # make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
        # start the thread
        t.start()


if __name__ == '__main__':
    main()
