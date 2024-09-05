

class Controller:
    def __init__(self):
        self.status = {}

    def start(self, group_id):
        if self.status.get(group_id):
            return True
        else:
            self.status[group_id] = True
            return False

    def end(self, group_id):
        self.status[group_id] = False


controller = Controller()
