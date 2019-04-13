class Margins(object):
    def __init__(self, *args):
        self.top = top = int(args[0])
        if len(args) > 1:
            right = int(args[1])
            if len(args) > 2:
                bottom = int(args[2])
                if len(args) > 3:
                    left = int(args[3])
                else:
                    left = right
            else:
                bottom = top
                left = right
        else:
            right = bottom = left = top

        self.right = right
        self.bottom = bottom
        self.left = left
