from models import LWMInterface
from models import Persistence


class Model:

    def __init__(self):
        self.lwm_interface = LWMInterface()
        self.persistence = Persistence()
