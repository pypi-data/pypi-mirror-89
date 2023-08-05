import smtplib, ssl
from easySMS.errors import LoginError
from easySMS.errors import SendError

class Messenger:
    def __init__(self, email: str, password: str, smtp_server: str, port: int = 587) -> None:
        self.server = smtplib.SMTP(smtp_server, port)
        self.server.starttls()
        self.servers = {'att': 'txt.att.net', 
                        'tmobile': 'tmomail.net',
                        'verizon': 'vtext.com',
                        'virgin': 'vmobl.com',
                       }

        try:
            self.server.login(email, password)
        except:
            raise LoginError('couldnt sign into email. wrong credentials or google blocked login.')

    def sendSMS(self, number: str, message: str, service: str = None) -> None:
        if service == None:
            for defaultServ in self.servers.values():
                self.sendSMS(number, message, defaultServ)
        else:
            try:
                refused = self.server.sendmail('pysms', f"{number}@{service}", message)
                if len(refused) > 0:
                    raise SendError('recipient refused email')
            except:
                raise SendError('recipient refused email')
