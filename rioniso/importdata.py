import ezodf
import re

'''
input: ODS file with:
---------------------------------------
Label | Harmonic | Simulated Frequency|
  .   |     .    |         .          |
  .   |     .    |         .          |
  .   |     .    |         .          |
---------------------------------------
'''

#imports the ods data
class ImportData(object):

    def __init__(self, simulated_data, experimental_data):
        self.simulated_data = np.array([])
        self.experimental_data = np.array([])
        self._import()

    def _import(self):
        self.simulated_data = import_identification_data(simulated_data)
        self.experimental_data = import_experimental_data(experimental_data)

    def import_identification_data(filename, sheet = 0, exclusion_list = None):
        odsinfo = ezodf.opendoc(filename)
        sheet = odsinfo.sheets[sheet_index]
        sheet_data = process_sheet(sheet, exclusion_list)
        processed_data = get_processed_data(sheet_data, unknown = unknown)
        return processed_data

    def process_sheet(sheet, exclusion_list):
        data = []
        # careful with the format of the ods. It must have 7 columns even if the 2nd is irrelevant,     modify
        for row in range(sheet.nrows()):
            if row in exclusion_list:
                continue

            row_data = [sheet[row, col].value for col in range(sheet.ncols()) if sheet[row, col].   value is not None]
            if row_data:
                # Ensure row_data has a consistent length
                row_data += [None] * (sheet.ncols() - len(row_data))
                data.append(row_data)
        # Convert to a 2D numpy array with dtype=object to handle mixed data types
        return np.array(data, dtype=object)

    def get_processed_data(sheet_data, unknown = None):
        names = sheet_data[:, 0]
        harmonics = sheet_data[:, 1].astype(int)
        f = sheet_data[:, 2].astype(float)

        names_latex = [convert_name(name) for name in names]

        data = np.column_stack([names_latex, harmonics, f])
        return data

    def convert_name(name):
        # Use regex to extract the atomic number, isotope name, and charge
        atomic_num, element, charge = re.findall(r"\d+|\D+", name)
        # Format the atomic number and charge as superscripts
        atomic_num = '$^{'+str(atomic_num)+'}$'
        charge = '$^{'+str(charge)+'+}$'
        # Form the element symbol by capitalizing the first letter of the isotope name
        element = element.capitalize()
        # Combine the superscripts and element symbol
        return atomic_num + element + charge

    def import_experimental_data(filename):
        expdata = np.load(filename)
        return expdata