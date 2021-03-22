class Parser:

    def __init__(self, msg):
        self.msg = msg

    def parse(self):
        if self.msg.endswith('joined the chat room.'):
            username = self.msg[1:self.msg.find('>')]
            res_type = 'join'
            return {'type': res_type, 'username': username}

        elif self.msg.startswith('Hi'):
            username = self.msg[self.msg.find('<') + 1: self.msg.find('>')]
            res_type = 'welcome'
            return {'type': res_type, 'username': username}

        elif self.msg.startswith('Here is the list of attendees:'):
            usernames = self.msg.split('\r\n')[1].split(',')
            usernames = [i.strip('<>') for i in usernames]
            res_type = 'list'
            return {'type': res_type, 'usernames': usernames}

        elif self.msg.startswith('Public message from'):
            msg_head, msg_body = self.msg.split('\r\n')
            msg_head = msg_head.split(',')
            msg_username = msg_head[0][msg_head[0].find('<') + 1: msg_head[0].find('>')]
            msg_len = msg_head[1][msg_head[1].find('<') + 1: msg_head[1].find('>')]
            msg_body = msg_body.strip('<>')
            res_type = 'public'
            return {'type': res_type, 'username': msg_username, 'length': msg_len, 'message': msg_body}

        elif self.msg.startswith('Private message'):
            msg_head, msg_body = self.msg.split('\r\n')
            msg_body = msg_body.strip('<>')
            msg_length = msg_head[msg_head.find('<') + 1: msg_head.find('>')]
            msg_from_username = msg_head[msg_head.find('from <') + 6:msg_head.find('> to')]
            users = [i.strip('<>') for i in msg_head[msg_head.find('to ') + 3: -1].split(',')]
            res_type = 'private'
            return {'type': res_type, 'username': msg_from_username, 'length': msg_length, 'message': msg_body}

        elif self.msg.endswith('left the chat room.'):
            msg_username = self.msg[1: self.msg.find('>')]
            res_type = 'leave'
            return {'type': res_type, 'username': msg_username}
