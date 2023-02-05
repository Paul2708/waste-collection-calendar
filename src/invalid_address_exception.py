class InvalidAddressException(Exception):

    def __init__(self, street, street_number):
        self.street = street
        self.street_number = street_number
        super().__init__(f'The address {street} {street_number} is not covered by the endpoint')
