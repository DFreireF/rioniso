import argparse
import ezodf
from rioniso import ImportData

def main():
    scriptname = 'RionISO' 
    parser = argparse.ArgumentParser(description='Computing the isochronicity curve.')
    parser.add_argument('expdata', type=str, help='Input file of with the experimental data (npz format).')
    parser.add_argument('identdata', type=str, help='Input file from identification (ODS format).')

    # Importing data
    mydata = ImportData(args.identdata, args.expdata)
    experimental_data = mydata.experimental_data
    simulated_data = mydata.simulated_data


if __name__ == "__main__":
    main()
    
