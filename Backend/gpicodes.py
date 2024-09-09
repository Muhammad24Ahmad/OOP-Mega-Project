import pandas as pd
import re

class DrugGPIMapper:
    def __init__(self, csv_file_path):
        """
        Initialize the DrugGPIMapper with the CSV file path.
        
        Parameters:
        - csv_file_path: The file path to the CSV containing the GPI data.
        """
        self.csv_file_path = csv_file_path
        self.df = self._load_csv()

    def _load_csv(self):
        """
        Load the CSV file into a DataFrame and clean the gpiName column.
        
        Returns:
        - A pandas DataFrame with cleaned data.
        """
        df = pd.read_csv(self.csv_file_path)
        df['gpiName'] = df['gpiName'].str.strip()  # Clean the gpiName column
        return df

    def _clean_drug_list(self, drug_list):
        """
        Clean the drug names by removing non-alphabetical characters and filter duplicates.
        
        Parameters:
        - drug_list: A list of drug names.
        
        Returns:
        - A list of cleaned and unique drug names.
        """
        # Clean drug names by removing non-alphabetical characters
        cleaned_drug_list = [re.sub(r'[^a-zA-Z]', '', drug) for drug in drug_list]
        
        # Filter duplicates while maintaining case-insensitivity
        filtered_drugs = []
        for drug in cleaned_drug_list:
            if drug.lower() not in filtered_drugs:
                filtered_drugs.append(drug.lower())

        return filtered_drugs

    def _match_drug_with_gpi(self, drug):
        """
        Match a single drug with its GPI code from the DataFrame.
        
        Parameters:
        - drug: The drug name to match.
        
        Returns:
        - A dictionary containing the matched drug and its GPI code, or None if no match is found.
        """
        match = self.df[self.df['gpiName'].str.lower() == drug.lower()]

        if not match.empty:
            gpi_code = str(match['gpi'].values[0]).strip()[:8]  # Truncate GPI code to 8 digits
            gpi_code = gpi_code + '0' * (8 - len(gpi_code))  # Pad with zeroes if needed
            return {'Drug': drug.capitalize(), 'GPI': gpi_code}
        
        return None

    def match_drugs_with_gpi(self, drug_list):
        """
        Match a list of drugs with their corresponding GPI codes.
        
        Parameters:
        - drug_list: A list of drug names.
        
        Returns:
        - A sorted list of dictionaries with matched Drug and GPI keys.
        """
        cleaned_drugs = self._clean_drug_list(drug_list)
        matched_drugs = []

        for drug in cleaned_drugs:
            match = self._match_drug_with_gpi(drug)
            if match:
                matched_drugs.append(match)

        # Sort the matched drugs by GPI code
        matched_drugs = sorted(matched_drugs, key=lambda x: x['GPI'])
        
        return matched_drugs


# # Example Usage
# if __name__ == "__main__":
#     csv_file = "path_to_your_csv_file.csv"  # Replace with the actual path to your CSV file
#     drug_list = ["Aspirin", "Ibuprofen", "Metformin"]

#     drug_gpi_mapper = DrugGPIMapper(csv_file)
#     matched_drugs = drug_gpi_mapper.match_drugs_with_gpi(drug_list)

#     print("Matched Drugs with GPI Codes:", matched_drugs)
