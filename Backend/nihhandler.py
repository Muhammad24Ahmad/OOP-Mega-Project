from Backend.nihdrugapprover import NIHDrugApprover

class NIHHandler:
    """
    A class that acts as a handler to facilitate the extraction of NIH-approved drugs
    for a specific cancer type using the NIHDrugApprover.
    """

    def __init__(self, cancer_type):
        """
        Initialize the NIHHandler with the type of cancer for which drug approvals need to be retrieved.

        Parameters:
        -----------
        cancer_type : str
            The type of cancer for which NIH-approved drugs will be extracted.
        """
        self.cancer_type = cancer_type

    def get_approved_drugs(self, matched_drug_gpi):
        """
        Retrieve the approved drugs for the specified cancer type, 
        after matching them with the provided GPI codes.

        Parameters:
        -----------
        matched_drug_gpi : list
            A list of drugs with their GPI codes that will be checked for approval against NIH data.

        Returns:
        --------
        list
            A list of drugs that are approved by NIH for the specified cancer type.
        """
        ApprovedNIHdrugs = NIHDrugApprover(self.cancer_type)
        return ApprovedNIHdrugs.NIH_extract_drugs(matched_drug_gpi)
