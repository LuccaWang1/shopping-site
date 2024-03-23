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
    """Read customer information and populate dictionary of melon types.
    
    Dictionary will be: {email: Customer(  )}. This format allows look up of a customer by email address.
    """

    customers = {}

    with open(filepath) as file:
        for line in file:
            (
                first_name,
                last_name,
                email,
                password
            ) = line.strip().split("|")

            customers[email] = Customer(
                first_name,
                last_name,
                email,
                password,
            )
    
    return customers

 
def get_by_email(email): #enabled by dict created by helper func above, look up customers by email
    """Get the customer's information from the dictionary of all customers of the Customer class when provided their email address."""

    return customers[email]

customers = read_customers_from_file("customers.txt") #using file that contains the customer data - and this customers variable is used by the helper function to get the customer by their email address above 