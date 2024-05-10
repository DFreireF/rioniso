import argparse
import ezodf
from rioniso import ImportData
from rioniso.model import *

def main():
    scriptname = 'RionISO' 
    parser = argparse.ArgumentParser(description='Computing the isochronicity curve.')
    parser.add_argument('expdata', type=str, help='Input file of with the experimental data (npz format).')
    parser.add_argument('identdata', type=str, help='Input file from identification (ODS format).')

    args = parser.parse_args()
    
    # Importing data
    mydata = ImportData(args.identdata, args.expdata)
    experimental_data = mydata.experimental_data
    simulated_data = mydata.simulated_data

    # Calculating iso curve experimental data
    iso_data = calculate_iso_inputs(imported_data.simulated_data, 
                                imported_data.experimental_data, xspan=6e3)
    


if __name__ == "__main__":
    main()
