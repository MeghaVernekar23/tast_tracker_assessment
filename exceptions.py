class UserNotFoundException(Exception):
    def __init__(self):
        self.message = "User details not found"
        super().__init__(self.message)


class TaskNotFoundException(Exception):

    def __init__(self):
        self.message = "Task details not found"
        super().__init__(self.message)       