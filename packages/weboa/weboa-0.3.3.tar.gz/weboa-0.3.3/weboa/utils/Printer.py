from .Console_Color import *

class Printer:

    @staticmethod
    def _dolog(text):
        try:
            with open("log.txt","r") as f:
                log_txt = f.read()
        except:
            pass
        with open("log.txt","w") as f:
            f.write(text)

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
        Printer._dolog(color+" [Log] "+str(text))        

    @staticmethod
    def info(text):
        color = Console_Color("info").color
        Printer._dolog(color+" [Info] "+str(text))