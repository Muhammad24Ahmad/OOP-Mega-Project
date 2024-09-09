class DrugApprovalChecker:
    """A class to check whether drugs are approved by the NIH for a specific cancer type."""

    def __init__(self, approved_drugs):
        """Initialize the checker with a list of NIH-approved drugs."""
        self.approved_drugs = set(drug.lower() for drug in approved_drugs)

    def check_approval(self, matched_drug_gpi):
        """
        Check if the drugs in matched_drug_gpi are approved.

        Parameters:
        - matched_drug_gpi: A list of dictionaries with 'Drug' and 'GPI' keys.

        Returns:
        - A list of dictionaries with 'Drug', 'GPI', and 'approval' (True/False) keys.
        """
        for entry in matched_drug_gpi:
            entry['approval'] = entry['Drug'].lower() in self.approved_drugs
        return matched_drug_gpi