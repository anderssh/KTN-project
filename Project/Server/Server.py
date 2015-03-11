# -*- coding: utf-8 -*-
import SocketServer
import json
import time
from time import gmtime, strftime

#---------------------------------------------

class ServerResponse():
    
    def __init__(self, timestamp, response, content, sender):
        
        self.timestamp = timestamp
        self.response = response
        self.content = content
        self.sender = sender

    def format(self):

        representation = {  'timestamp' : self.timestamp,
                            'response'  : self.response,
                            'content'   : self.content,
                            'sender'    : self.sender }

        return json.dumps(representation)

#---------------------------------------------

connections = []
history     = []

#---------------------------------------------

class User():
    
    def __init__(self):
        self.username = ''
        self.logged_in = False

    def is_logged_in(self):
        return self.logged_in

    def login(self, username):
        self.username = username
        self.logged_in = True

    def logout(self):
        self.username = ''
        self.logged_in = False

    def get_username(self):
        return self.username

def is_username_valid(username):
    return username.isalnum()

def is_username_taken(username):
    for conn in connections:
        if (conn.user.get_username() == username):
            return True;

    return False;

#---------------------------------------------

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle_login(self, requested_username):

        if (not is_username_valid(requested_username)):

            server_response = ServerResponse(strftime("%a, %d %b %Y %H:%M:%S", gmtime()), 'error', 'You must provide a valid username. Please use only [a-z], [A-Z] and 0-9.', 'server')
            self.connection.send(server_response.format())

        elif (is_username_taken(requested_username)):

            server_response = ServerResponse(strftime("%a, %d %b %Y %H:%M:%S", gmtime()), 'error', 'The username is already taken, please use another one.', 'server')
            self.connection.send(server_response.format())

        else:

            self.user.login(requested_username)
            
            if (not self in connections):
                connections.append(self)

            history_formatted = []
            for history_entry in history:
                history_formatted.append(str(history_entry.sender) + ': ' + str(history_entry.content))

            server_response_info = ServerResponse(strftime("%a, %d %b %Y %H:%M:%S", gmtime()), 'info', 'Logged in as ' + str(requested_username), 'server')
            self.connection.send(server_response_info.format())

            time.sleep(0.100)

            server_response_history = ServerResponse(strftime("%a, %d %b %Y %H:%M:%S", gmtime()), 'history', history_formatted, 'server')
            self.connection.send(server_response_history.format())

    #---------------------------------------------

    def handle_logout(self):

        self.user.logout()

        # Send info to all
        server_response = ServerResponse(strftime("%a, %d %b %Y %H:%M:%S", gmtime()), 'info', 'User ' + self.user.get_username() + ' has logged out.', 'server')

        for conn in connections:
            if (conn.user.is_logged_in()):
                conn.connection.send(server_response.format());

        server_response = ServerResponse(strftime("%a, %d %b %Y %H:%M:%S", gmtime()), 'info', 'Logged out.', 'server')
        self.connection.send(server_response.format())

    #---------------------------------------------

    def handle_msg(self, content):
        
        if self.user.is_logged_in():

            print 'Server: handle message.'

            timestamp = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
            response = "message"
            content  = content
            sender   = self.user.get_username()

            server_response = ServerResponse(timestamp, response, content, sender)
            history.append(server_response)

            # Send to all
            for conn in connections:
                if (conn.user.is_logged_in()):
                    conn.connection.send(server_response.format());

        else:
            server_response = ServerResponse(strftime("%a, %d %b %Y %H:%M:%S", gmtime()), 'error', 'You must login to send messages. Type help for more info.', 'server')
            self.connection.send(server_response.format())

    #---------------------------------------------

    def handle_names(self):

        if (self.user.is_logged_in()):
        
            names = ''

            for conn in connections:
                if (conn.user.is_logged_in()):
                    names = names + conn.user.get_username() + '\n'

            timestamp = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
            response = "info"
            content  = names
            sender   = 'server'

            server_response = ServerResponse(timestamp, response, content, sender)
            self.connection.send(server_response.format())
        else:
            server_response = ServerResponse(strftime("%a, %d %b %Y %H:%M:%S", gmtime()), 'error', 'You must login to view the names.', 'server')
            self.connection.send(server_response.format())

    #---------------------------------------------

    def handle_help(self):

        print 'Inne i help'

        timestamp = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
        response = "info"
        content = "Instructions: \n\
            'login <username>' logs you in with the selected username \n\
            'msg <message>' sends youre message to everyone \n \
            'help' Displays this help message \n\
            'names' Displays the name of all logged in users\n\
            'logout' Logs you out of the chat room \n\
        "
        sender = "server"

        server_response = ServerResponse(timestamp, response, content, sender)
        self.connection.send(server_response.format())

    #---------------------------------------------

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        self.user = User()

        # Loop that listens for messages from the client
        while True:

            received_string = self.connection.recv(4096)
            
            message = json.loads(received_string)

            request = message['request']
            content = message['content']

            print 'The request is: ' + request

            if request == 'login':
                self.handle_login(content)
            elif request == 'logout':
                self.handle_logout()
            elif request == 'msg':
                self.handle_msg(content)
            elif request == 'names':
                self.handle_names()
            elif request == 'help':
                self.handle_help()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
