class UserNotFoundException(Exception):
    def __init__(self):
        self.message = "User details not found"
        super().__init__(self.message)


class TaskNotFoundException(Exception):
    def __init__(self):
        self.message = "Task details not found"
        super().__init__(self.message)       

class DuplicateFileException(Exception):

    def __init__(self):
        self.message = "Document with this name already exists."
        super().__init__((self.message))  


class FileNotFoundException(Exception):

    def __init__(self):
        self.message = "Requested document does not exist"
        super().__init__((self.message))  