# Easy-SMS 

A simple Python package that allows you to send text messages to any number. Goal: Be extremely simple. The package requires your email credentials as it uses SSL to send the text messages.

## USAGE

```
from messenger import Messenger
m = Messenger('email@gmail.com', 'password', 'smtp.gmail.com')
m.sendSMS('1234567890', 'this is a message')
```
