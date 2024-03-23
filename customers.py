"""Customers at Ubermelon."""

#define a Customer class to use the object-oriented programming features of methods and attributes for customer instances, used for login purposes
class Customer:
    """Ubermelon customer."""

    #setting attributes by using self 
    def __init__(
            self,
            first_name,
            last_name,
            email,
            password,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    #handy for debugging, printing Customer instance object to terminal
    def __repr__(self):
        """Convenience method to show information about customer in console."""
        
        return (f"<Customer: {self.first_name, self.last_name}>")
    
#function to read data file, customers.txt
def read_customers_from_file(filepath):
    """Read customer information and populate dictionary of melon types."""

    