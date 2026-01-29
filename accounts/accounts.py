class Accounts:
    def __init__(self, fn, ln, suf, em, pas):
        self.first_name = fn
        self.last_name = ln
        self.suffix = suf
        self.email = em
        self.password = pas
        
    def __str__(self):
        return f"Hi! I'm {self.first_name} {self.last_name} {self.suffix} and my email is {self.email} with hashed password of {self.password}"

if __name__ == '__main__':
    a = Accounts('Jason', 'Medina', 'IV', 'jasonmedina.official@gmail.com', 'kunwarimaangasperoinde')
    print(a)
    