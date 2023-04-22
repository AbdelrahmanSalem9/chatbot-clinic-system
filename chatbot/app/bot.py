from .query_handler import QueryHandler
from nltk.chat.util import Chat, reflections 
# import re


class Bot:
    def __init__(self):
        self.handler = QueryHandler()
        self.rules = [
            (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
            (r'what is your name?', ['My name is ChatBot.', 'I am ChatBot.']),
            (r'how are you?', ['I am doing well, thank you!', 'I am fine, thank you!']),
            (r'appointment|appointee|fitting|scheduling|schedule', ['Sure, I can help you with that, please provide your full name']),
            (r'bye|goodbye|see you', ['Goodbye!', 'See you later.']),
            (r'(.*)', ['I am sorry, I did not understand.']),
        ]
        self.chat = Chat(self.rules, reflections)

        # TODO: change to dynamic definition
        self.appointment_keywords = {'appointment', 'designation', 'appointee', 'fitting', 'scheduling','schedule'}      
        self.doctor_keywords = {'doctor', 'doc', 'physician','Dr.','ph'}
        self.working_hours_keywords = {'working', 'hours','avaliable.', 'open'}

    def get_response(self, user_input):
        if any(s in user_input for s in self.doctor_keywords):
            return self.handler.doctor_query()
        elif any(s in user_input for s in self.appointment_keywords):
            return self.handler.appointment_query()
        elif any(s in user_input for s in self.working_hours_keywords):
            return self.handler.working_hours_query()
        else:
            return self.chat.respond(user_input)
