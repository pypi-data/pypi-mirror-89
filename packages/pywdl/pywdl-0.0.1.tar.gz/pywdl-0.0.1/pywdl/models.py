
class Document:
    """

    """
    def __init__(self):
        self.version = 'development'
        self.workflow = None
        self.tasks = []


class Workflow:
    """

    """
    def __init__(self):
        self.inputs = []
        self.scatters = []
        self.conditionals = []
        self.calls = []


class Task:
    """

    """
    def __init__(self):
        self.inputs = []
        self.runtime = []
        self.command = None
        self.outputs = []


class Call:
    def __init__(self):
        pass
