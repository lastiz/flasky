class User:
    def __init__(self, email):
        email = email
    
    @property
    def email(self):
        return self.email
    @email.setter
    def email(self, val):
        self.email = val
        
u = User(email='lol@lol')

u.email = 1
print(u.email)