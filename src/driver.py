import datetime as dt

class Driver:
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    driver_id : int
        primary key
    first_name : str
        driver's first name
    last_name : str
        driver's last name
    number : int
        driver's car number
    dob : datetime
        driver's date of birth
    nationality : str
        driver's nationality
    country : str
        driver's designated home country
    code : str
        driver code, usually an abbreviation of thier last name for display in broadcasting graphics
    ref : str
        reference term for the driver, usually their last name

    Methods
    -------
    age(to_date=datetime.today())
        returns the drivers age at the specified date. default returns their age at the current date
        calculates by subtracting to_date.year from self.dob.year and if self.dob.month is greater than to_date.month subtract 1
    """

    def __init__(self, driver_id, first_name, last_name, number, dob, nationality, country, code='', ref=''):
        self.driver_id = driver_id
        self.first_name = first_name
        self.last_name = last_name
        self.number = number
        self.dob = dob
        self.nationality = nationality
        self.country = country
        self.code = code
        self.ref = ref

    def age(self, to_date=dt.datetime.today()):
        return to_date.year - self.dob.year - ((to_date.month, to_date.day) < (self.dob.month, self.dob.day))