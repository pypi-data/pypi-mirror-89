import time
import shutil
import os

from .progress_bar import ProgressBar
from .util import clear

class Dashboard():
    def __init__(self, progress):
        super().__init__()

        self.display = False
        self.metrics = progress.metrics
        self.params = progress.params
        self._build(metrics=self.metrics, params=self.params)
    
    def update(self):
        columns, lines = shutil.get_terminal_size((80, 20))
        clear()
        if self.progress_bar is not None:
            self.progress_bar.update(self.metrics['step']/self.params['num_batches'], width=columns)
            
    def start(self):
        while self.display:
            self.update()
            time.sleep(0.25)

    def _build(self, metrics: dict, params: dict):
        self.progress_bar = ProgressBar() if 'step' in metrics and 'num_batches' in params else None
