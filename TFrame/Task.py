from threading import Thread

class Task(Thread):
    def __init__(self,func):
        self.func = func
    
    def run(self):
        self.func()