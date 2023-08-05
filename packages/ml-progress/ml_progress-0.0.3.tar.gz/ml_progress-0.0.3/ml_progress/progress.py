from threading import Thread

from .dashboard import Dashboard

class Progress():
    def __init__(self, params={}, metrics={}):
        super().__init__()

        self.params = params
        self.metrics = metrics

        self.dashboard = Dashboard(self)
        self.thread = Thread(target=self.dashboard.start)
    
    def start(self):
        self.dashboard.display = True
        self.thread.start()
    
    def stop(self):
        self.dashboard.display = False
        self.thread.join()
