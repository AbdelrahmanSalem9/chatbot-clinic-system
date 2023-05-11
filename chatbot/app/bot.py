from .query_handler import QueryHandler
from nltk.chat.util import Chat, reflections

# TODO: Prioirty of words in the user input


class Bot:
    def __init__(self):
        self.handler = QueryHandler()
        self.rules = [
            (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
            (r'what is your name?', ['My name is ChatBot.', 'I am ChatBot.']),
            (r'how are you?', [
             'I am doing well, thank you!', 'I am fine, thank you!']),
            (r'bye|goodbye|see you', ['Goodbye!', 'See you later.']),
            # (r'modify|change|adjust|reform', [
            #  "Sure, I will help you to modify an appointment now, provide me with the appointment ID."]),
            (r'(.*)', ['I am sorry, I did not understand.']),

        ]
        self.chat = Chat(self.rules, reflections)

        self.appointment_keywords = (
            'appointment', 'designation', 'scheduling', 'schedule')
        self.doctor_keywords = ('doctor', 'doc', 'physician', 'Dr.', 'ph')
        self.modify_keywords = ('modify', 'change', 'adjust', 'reform')
        self.delete_keywords = ('delete', 'remove', 'cancel')
        self.specialities_keywords = (
            "specialities", "speciality", "specialty")

    def get_response(self, user_input):
        if any(s in user_input for s in self.delete_keywords):
            return self.handler.delete_appointment_query(user_input)
        elif any(s in user_input for s in self.modify_keywords):
            return self.handler.modify_appointment_query(user_input)
        elif any(s in user_input for s in self.appointment_keywords):
            return self.handler.new_appointment_query()
        elif any(s in user_input for s in self.specialities_keywords):
            return self.handler.speciality_query()
        if any(s in user_input for s in self.doctor_keywords):
            return self.handler.doctor_query(user_input)
        else:
            return self.chat.respond(user_input)
