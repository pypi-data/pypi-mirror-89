from saysomething.data import data
import random
class SaySomething:
    def __init__(self):
        self.data = data
    def say(self, topic = 'jokes'):
        if topic not in self.data: topic = 'jokes'
        return random.choice(self.data[topic])