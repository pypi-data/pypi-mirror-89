from .Console_Color import *

class Printer:

    @staticmethod
    def warning(text):
        color = Console_Color("warning").color
        print(color, "[Warning]", text)

    @staticmethod
    def error(text):
        color = Console_Color("error").color
        print(color, "[Error]", text)

    @staticmethod
    def log(text):
        color = Console_Color("log").color
        with open("log.txt","w") as f:
            f.write(color+" [Log] "+str(text))

    @staticmethod
    def info(text):
        color = Console_Color("info").color
        with open("log.txt","w") as f:
            f.write(color+" [Info] "+str(text))