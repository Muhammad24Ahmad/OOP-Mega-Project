from Backend.reportgenerator import ReportGenerator

class FileHandler:
    """
    Handles the generation of files for approved drugs based on the specified cancer type
    and model name.
    """

    def __init__(self, approved_drugs_list, cancer_type, model_name):
        """
        Initialize the FileHandler with a list of approved drugs, cancer type, and model name.

        Parameters:
        -----------
        approved_drugs_list : list
            A list of dictionaries containing drug information.
        cancer_type : str
            The type of cancer for which the drugs are approved.
        model_name : str
            The name of the model used for drug extraction.
        """
        self.approved_drugs_list = approved_drugs_list
        self.cancer_type = cancer_type
        self.model_name = model_name

    def generate_file(self, extension):
        """
        Generate a file (PDF or JSON) based on the approved drugs.

        Parameters:
        -----------
        extension : str
            The file format to generate ('pdf' for PDF, other formats default to JSON).

        Returns:
        --------
        str
            The file path of the generated report.
        """
        reportgenerator = ReportGenerator(self.approved_drugs_list, self.cancer_type, self.model_name)
        if extension == 'pdf':
            return reportgenerator.create_pdf_report()
        else:
            return reportgenerator.save_to_json_file()
