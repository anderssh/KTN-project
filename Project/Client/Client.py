# -*- coding: utf-8 -*-
import socket
from MessageReceiver import * 
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = host
        self.server_port = server_port

        self.messageReceiver = MessageReceiver(self, self.connection)

        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.messageReceiver.start()

        while True:
            user_message = raw_input()
            self.send_payload(user_message)

    def disconnect(self):
        pass

    def receive_message(self, message):

        # TODO: Handle incoming message
        message = json.loads(message);

        timestamp     = message['timestamp']
        response      = message['response']
        content       = message['content']
        sender        = message['sender']

        if (response == 'history'):
            for history_entry in content:
                print(history_entry)

        elif (response == 'message'):
            print(sender + ': ' + content)
        else:
            print(content)


    def send_payload(self, data):

        request = data.split(' ',1)[0]
        content = data[len(request):]
        content = content.strip()

        formatted_data = {"request" : request, "content" : content} 
        formatted_data = json.dumps(formatted_data)

        self.connection.send(formatted_data)


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
