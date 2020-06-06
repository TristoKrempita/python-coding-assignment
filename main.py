from KPI import KPI
import urllib.request
import json


def get_data():
    """
    Get CSV data from API by using a GET request and deserialize to a dictionary.
    Split the CSV data by '\n' to get an array of records.
    :return: Every row of the dataset except the first one
    """

    url_data = "http://lameapi-env.ptqft8mdpd.us-east-2.elasticbeanstalk.com/data"
    web_url = urllib.request.urlopen(url_data)
    data = web_url.read()
    encoding = web_url.info().get_content_charset('utf-8')
    web_json = json.loads(data.decode(encoding))

    data = web_json['data'].split('\n')

    if data == ['']:
        raise Exception('Connection to server failed')
    return data[1:]


def limit_data(data, start, stop):
    """
    Take wanted subset of dataset
    :param data: Entire dataset array
    :param start: Start date string
    :param stop: Stop date string
    :return: Subset of the dataset from the one that contains the start
    string to the one that contains the stop string (inclusive).
    In case of repetition take first appearance of start and last appearance
    of stop.
    """
    first_index = last_index = -1
    for i, record in enumerate(data):
        if first_index == -1 and start in record:
            first_index = i

        if stop in record:
            last_index = i

        if stop in data[i-1] and stop not in data[i]:
            last_index = i
            break
    if first_index == -1 or last_index == -1:
        raise Exception("Limiting data failed. Try checking if start and stop parameters are in "
                        "the right order, correctly formatted or if they exist in the dataset.")
    return data[first_index:last_index]


def value_input(kpi_list, start, stop):
    """
    For each item in the kpi_list array cycle through every record and
    add its value to a newly created KPI object. Once the object has all
    the necessary data, calculate self.average and self.median fields.
    At the end display the results using a __repr__ function to print out
    a dictionary of values.
    :param kpi_list: An array of
    :param start: Start date string
    :param stop: Stop date string
    :return: Display dictionary made up of values from the KPI objects
    """
    data = get_data()
    limited_data = limit_data(data, start, stop)
    #   List of KPI objects needed to store values from kpi_list
    objects = [KPI() for _ in kpi_list]
    #   Dictionary to control which value from the individual record to take information from
    string_to_index = {
        "temperature": 1,
        "humidity": 2,
        "light": 3,
        "co2": 4,
        "occupancy": 6
    }

    for i, object in enumerate(objects):
        #   Establish index of the value in the record we will take information from
        record_index = string_to_index[kpi_list[i]]
        for j, record in enumerate(limited_data):
            #   Turn each record from CSV to array of values
            record = record.split(',')

            #   Turn all values into floats for calculations
            value = float(record[record_index])

            #   Save first and last value
            if j == 0:
                object.first_value = value
                #   Establish highest and lowest value by equating it to the first one
                object.establish_minimum(value)
            elif j == len(limited_data) - 1:
                object.last_value = value

            #   Add to sum for calculating the average and to the array for calculating the median
            object.sum += value
            object.arr.append(value)

            #   Check if current value is the highest or lowest saved value
            object.check_max(value)
            object.check_min(value)
        #   Use the sum and array from above to calculate average and median
        object.calculate_average(len(limited_data))
        object.calculate_median()
        object.calculate_percent_change()

    #   Print out results
    for kpi_result in objects:
        print(kpi_result)
