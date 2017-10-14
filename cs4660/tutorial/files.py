"""Files tests simple file read related operations"""
from io import open

class SimpleFile(object):
    """SimpleFile tests using file read api to do some simple math"""

    def __init__(self, file_path):
        self.numbers = []
        """
        TODO: reads the file by path and parse content into two
        dimension array (numbers)
        """
        f = open(file_path, encoding='utf-8')
        lines = f.readlines()    # unicode, not bytes
        
        self._arr = []
       
        for line in lines:
            string_list = line.split()
            int_list = []
            for s in string_list:
                int_list.append(int(s))
            self._arr.append(int_list)
        f.close()


    def get_mean(self, line_number):
        """
        get_mean retrieves the mean value of the list by line_number (starts
        with zero)
        """
        return sum (self._arr[line_number]) / float(len(self._arr[line_number]))

    def get_max(self, line_number):
        """
        get_max retrieves the maximum value of the list by line_number (starts
        with zero)
        """
        return max(self._arr[line_number])

    def get_min(self, line_number):
        """
        get_min retrieves the minimum value of the list by line_number (starts
        with zero)
        """
        return min(self._arr[line_number])

    def get_sum(self, line_number):
        """
        get_sum retrieves the sumation of the list by line_number (starts with
        zero)
        """
        return sum(self._arr[line_number])
