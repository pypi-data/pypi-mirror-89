class BMI:
    def __init__(self, mass, height):
        self.mass = mass
        self.height = height

    def __str__(self):
        return str(self.check())

    def check(self):
        """
        Calculates the body mass index
        height in metres and mass in kg
        """
        return round(self.mass/(self.height**2), 1)

    def report(self):
        if self.check() > 0 and self.check() < 18.5:
            return 'Underweight'
        elif self.check() > 18.5 and self.check() < 24.9:
            return 'Normal weight'
        elif self.check() > 25.0 and self.check() < 29.9:
            return 'Overweight'
        elif self.check() > 30.0 and self.check() < 34.9:
            return 'Obesity class I'
        elif self.check() > 35.0 and self.check() < 39.9:
            return 'Obesity class II'
        elif self.check() > 40:
            return 'Obesity class III'
        else:
            return 'Invalid mass or height input.'


"""uncomment the following code to test"""
# eroms = BMI(75, 1.83) 
# print(eroms.report())

