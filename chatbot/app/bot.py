from .models import Doctor
import re


class Bot:
    def __init__(self):
        # self.syns = {'hello': {'hello', 'hullo', 'hi', 'howdy', 'how do you do'}, 'doctor': {'Doctor', 'doc', 'doctor up', 'mend', 'sophisticate',
        #  'MD', 'medico', 'touch on', 'bushel', 'restore', 'physician', 'Dr.', 'Doctor of the Church', 'doctor', 'fix', 'repair', 'furbish up'}}
        self.keywords_dict = {
            'greet': re.compile('.*\\bhello\\b.*|.*\\bhullo\\b.*|.*\\bhi\\b.*|.*\\bhowdy\\b.*|.*\\bhow do you do\\b.*'),
            'doctor': re.compile('.*\\bDoctor\\b.*|.*\\bdoc\\b.*|.*\\bdoctor up\\b.*')
        }
        self.responses = {
            'greet': self.greeting_query,
            'doctor': self.doctor_query,
            'fallback': self.fallback_query,
        }

    def doctor_query(self, doctor_id=1):
        doctor = Doctor.objects.get(pk=doctor_id)
        return f"Doctor {doctor.name} is a {doctor.specialty} and is available {doctor.availability}"

    def greeting_query(self):
        return "Hello! How can I help you?"

    def fallback_query(self):
        return "I dont quite understand. Could you repeat that?"

    def get_response(self, user_input):
        matched_intent = 'fallback'
        for intent, pattern in self.keywords_dict.items():
            if re.search(pattern, user_input):
                matched_intent = intent
                print(intent)
        return self.responses[matched_intent]()
