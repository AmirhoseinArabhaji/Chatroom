class Parser:
    """
    Parser class for parsing message received from clients
    and return a standard response
    """

    def __init__(self, msg):
        self.msg = msg

    def parse(self):
        if self.msg.startswith('Hello <'):
            username = self.msg.split()[1].strip('<>')
            req_type = 'join'
            return {'type': req_type, 'username': username}

        elif self.msg == 'Please send the list of attendees.':
            req_type = 'list'
            return {'type': req_type}

        elif self.msg.startswith('Public message, length=<'):
            msg_head, msg_body = self.msg.split('\r\n')
            msg_len = int(msg_head[24:-2])
            msg_body = msg_body.strip('<>')
            req_type = 'public'
            return {'type': req_type, 'length': msg_len, 'message': msg_body}

        elif self.msg.startswith('Private message'):
            msg_head, msg_body = self.msg.split('\r\n')
            msg_len = int(msg_head[msg_head.find('<') + 1: msg_head.find('>')])
            # split and strip usernames list
            users = [i.strip('<>') for i in msg_head[msg_head.find('to ') + 3: -1].split(',')]
            msg_body = msg_body.strip('<>')
            req_type = 'private'
            return {'type': req_type, 'length': msg_len, 'message': msg_body, 'users': users}

        elif self.msg == 'Bye.':
            req_type = 'leave'
            return {'type': req_type}
