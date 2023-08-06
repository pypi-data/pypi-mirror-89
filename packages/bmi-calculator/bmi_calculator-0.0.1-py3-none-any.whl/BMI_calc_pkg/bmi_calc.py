import decimal


def float_range(start, stop, step):
  while start < stop:
    yield float(start)
    start = decimal.Decimal(start)
    start += decimal.Decimal(step)

# print(list(float_range(0, 1, '0.1')))


class BMI:
    STATUS = {
        'Underweight': float_range(0, 18.5, '0.1'),
        'Normal weight': float_range(18.5, 24.9, '0.1'),
        'Overweight': float_range(25.0, 29.9, '0.1'),
        'Obesity class I': float_range(30.0, 34.9, '0.1'),
        'Obesity class II': float_range(35.0, 39.9, '0.1'),
    }

    def __init__(self, mass, height):
        self.mass = mass
        self.height = height

    def __str__(self):
        return str(self.check())

    def check(self):
        """Calculates the body mass index"""
        return round(self.mass/(self.height**2), 1)

    def report(self):
        for k, v in self.STATUS.items():
            if self.check() in v:
                return k
            elif self.check() > 40:
                return 'Obesity class III'
        return "Invalid mass or height input."


