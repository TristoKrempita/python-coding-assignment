import argparse
from main import value_input

#   Parser to pare command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--kpi_list', required=True)
parser.add_argument('--start', required=True)
parser.add_argument('--stop', required=True)
args = parser.parse_args()

#   Call to function using the CSV from --kpi_list argument and splitting them into an array
value_input(kpi_list=[i for i in args.kpi_list.split(',')], start=args.start, stop=args.stop)
