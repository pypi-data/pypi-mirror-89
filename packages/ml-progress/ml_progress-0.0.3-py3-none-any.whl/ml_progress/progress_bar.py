import sys

class ProgressBar():
    def __init__(self):
        super().__init__()

    def update(self, progress: float, width=25, height=1):
        width = width - 7 # make room for constant outputs (e.g. |)
        solid = u"\u2588"*int(progress*width)
        empty = " "*(width-int(progress*width))
        sys.stdout.write("%3d%% " % (int(progress*100)))
        for line in range(height):
            if line > 0:
                sys.stdout.write("     ")
            sys.stdout.write("|%s%s|\n" % (solid, empty))