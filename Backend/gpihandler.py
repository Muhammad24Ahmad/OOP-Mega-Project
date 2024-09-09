from Backend.gpicodes import DrugGPIMapper

class GPIHandler:
    """
    Handles GPI (Generic Product Identifier) code mapping for a list of drugs using a provided CSV file.
    """

    def __init__(self, csv_file_path):
        """
        Initialize the GPIHandler with the path to the GPI codes CSV file.

        Parameters:
        -----------
        csv_file_path : str
            The file path of the CSV containing GPI codes.
        """
        self.csv_file_path = csv_file_path

    def match_drugs(self, drugs_list):
        """
        Match the drugs in the provided list with their corresponding GPI codes.

        Parameters:
        -----------
        drugs_list : list
            A list of drugs for which GPI codes need to be matched.

        Returns:
        --------
        list
            A list of dictionaries where each entry contains the drug name and the matched GPI code.
        """
        gpicodes = DrugGPIMapper(self.csv_file_path)
        return gpicodes.match_drugs_with_gpi(drugs_list)
