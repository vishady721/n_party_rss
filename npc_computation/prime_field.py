FIELD_ORDER = 13

class PrimeFieldElement:    
    def __init__(self, value):
        self.value = value % FIELD_ORDER
    
    def __add__(self, other):
        return PrimeFieldElement((self.value + other.value) % FIELD_ORDER)
    
    def __mul__(self, other):
        return PrimeFieldElement((self.value * other.value) % FIELD_ORDER)

    def __sub__(self, other):
        return PrimeFieldElement((self.value - other.value) % FIELD_ORDER)

    def __neg__(self):
        return PrimeFieldElement(-self.value % FIELD_ORDER)

    def __eq__(self, other):
        return (self.value == other.value)
    
    def __repr__(self):
        return str(self.value)