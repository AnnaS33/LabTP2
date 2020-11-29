import json
from jsonschema import validate

END_CHARACTER = "\0"
TARGET_ENCODING = "utf-8"


class Message(object):

    def __init__(self, **kwargs):
        self.id=None
        self.quit = False
        self.Number = None
        self.win=None
        self.idCl=None
        self.Save=None
        self.Load = None
        self.__dict__.update(kwargs)#устанавливает атрибуты в словарь

    def marshal(self):
        return (json.dumps(self.__dict__) + END_CHARACTER).encode(TARGET_ENCODING)#Кодируем сообщение
    def marshal2(self):
        return (self.__dict__)
