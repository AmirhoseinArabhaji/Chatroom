class User:
    """
    User class for saving client related data
    """
    def __init__(self, client_socket, addr, username):
        self.ip = addr[0]
        self.id = addr[1]
        self.username = username
        self.client_socket = client_socket

    def __str__(self):
        return self.username
