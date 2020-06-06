from statistics import median


class KPI:
    def __init__(self):
        self.first_value = 0
        self.last_value = 0
        self.average = 0
        self.median = 0
        self.mode = 1
        self.sum = 0
        self.highest = 0
        self.lowest = 0
        self.percent_change = ""
        self.arr = []

    def calculate_average(self, amount):
        """
        Calculate average by diving sum of all values and the amount of records
        Set the internal average variable to the average
        :param amount: Number of values (number of records those values were taken from)
        :return: None
        """
        self.average = self.sum/amount

    def calculate_median(self):
        """
        Calculate median by sorting the internal array and finding the middle value
        Set the internal median variable to the median
        :return: None
        """
        self.median = median(self.arr)

    def check_max(self, value):
        """
        If the current value is larger than the internal one change internal to current
        :param value: Current value of the record that's being analyzed
        :return: None
        """
        if value > self.highest:
            self.highest = value

    def check_min(self, value):
        """
        If the current value is smaller than the internal one change internal to current
        :param value: Current value of the record that's being analyzed
        :return: None
        """
        if value < self.lowest:
            self.lowest = value

    def establish_minimum(self, value):
        """
        Set the internal highest and lowest variables to the value from the first record
        :param value: Initial value taken from the first record
        :return: None
        """
        self.highest = self.lowest = value

    def calculate_percent_change(self):
        """
        Calculate percent change by taking the absolute value of (A2-A1)/A1, A2 being the final state and
        A1 being the initial state.
        Multiply by 100 to get percentage and limit decimal numbers to 3.
        If the first value is zero return "NaN"
        :return: None
        """
        self.percent_change = f"{abs((self.last_value-self.first_value)/self.first_value)*100:.3f}%" \
            if self.first_value else "NaN"

    def __repr__(self):
        """
        Internal method used to print out information about the object
        :return: Dictionary of current internal values turned into a string
        """
        output = {
                "percent_change": self.percent_change,
                "last_value": self.last_value,
                "first_value": self.first_value,
                "lowest": self.lowest,
                "highest": self.highest,
                "mode": self.mode,
                "average": round(self.average, 5),
                "median": round(self.median, 5)
                }
        return str(output)

