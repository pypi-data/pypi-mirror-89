class SMSError(Exception):
    pass

class LoginError(SMSError):
    def __init__(self, message: str):
        self.message = message

class SendError(SMSError):
    def __init__(self, message: str):
        self.message = message
