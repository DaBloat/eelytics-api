class Account:
    def __init__(self, fn, ln, suf, usr, em, pas, pfp):
        self.first_name = fn
        self.last_name = ln
        self.suffix = suf
        self.username = usr
        self.email = em
        self.password = pas
        self.profile_pic = pfp
        
    def __str__(self):
        return f"Hi! I'm {self.first_name} {self.last_name} {self.suffix}, you can call me {self.username} and my email is {self.email} with hashed password of {self.password}"

if __name__ == '__main__':
    a = Account('Jason', 'Medina', 'IV', 'JMedina', 'jasonmedina.official@gmail.com', 'kunwarimaangasperoinde', 'image.jpg')
    print(a)
    