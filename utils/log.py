class Logger:
    def __init__(self, re_misc):
        self.re_misc = re_misc

    def info(self, message):
        self.re_misc.SendMessage("INFO: " + message)
        
    def error(self, message):
        self.re_misc.SendMessage("ERROR: " + message)
