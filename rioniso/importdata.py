import ezodf
import re
import numpy as np

'''
input: ODS file with:
---------------------------------------
Label | Harmonic | Simulated Frequency|
  .   |     .    |         .          |
  .   |     .    |         .          |
  .   |     .    |         .          |
---------------------------------------
'''

class ImportData(object):

    def __init__(self):
        self.simulated_data = np.array([])
        self.experimental_data = np.array([])

    @classmethod
    def _import(cls, simulated_data_file: str, experimental_data_file: str, simulated_sheet: int = 0) -> 'ImportData':
        obj = cls()
        obj.simulated_data = obj.import_identification_data(simulated_data_file, simulated_sheet)
        obj.experimental_data = obj.import_experimental_data(experimental_data_file)
        return obj

    def import_identification_data(self, filename, sheet_index, exclusion_list = []):
        try:
            odsinfo = ezodf.opendoc(filename)
            sheet = odsinfo.sheets[sheet_index]
            sheet_data = self.process_sheet(sheet, exclusion_list)
            processed_data = self.get_processed_data(sheet_data)
            return processed_data
        except Exception as e:
            raise ImportError(f"Failed to import data from {filename}: {e}")

    def process_sheet(self, sheet, exclusion_list = []):
        data = []
        # name | harmonics | simulated frequency #
        for row in range(1, sheet.nrows()):
            if row in exclusion_list:
                continue

            row_data = [sheet[row, col].value for col in range(sheet.ncols()) if sheet[row, col].value is not None]
            if row_data:
                # Ensure row_data has a consistent length
                row_data += [None] * (sheet.ncols() - len(row_data))
                data.append(row_data)
        # Convert to a 2D numpy array with dtype=object to handle mixed data types
        return np.array(data, dtype=object)

    def get_processed_data(self, sheet_data, names_index = 0, harmonics_index = 1, frequency_index = 2):
        names = sheet_data[:, names_index]
        harmonics = sheet_data[:, harmonics_index].astype(int)
        f = sheet_data[:, frequency_index].astype(float)
        names_latex = [convert_name(name) for name in names]
        data = np.column_stack([names_latex, harmonics, f])
        return data

    def import_experimental_data(self, filename):
        try:
            expdata = np.load(filename)
            return expdata
        except Exception as e:
            raise ImportError(f"Failed to load experimental data from {filename}: {e}")

def convert_name(name):
    # Use regex to extract the atomic number, isotope name, and charge
    atomic_num, element, charge = re.findall(r"\d+|\D+", name)
    atomic_num = '$^{'+str(atomic_num)+'}$'
    charge = '$^{'+str(charge)+'+}$'
    element = element.capitalize()
    return atomic_num + element + charge