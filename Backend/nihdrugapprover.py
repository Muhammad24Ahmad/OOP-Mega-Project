from Backend.webscraper import WebScraper
from Backend.nihdrugextractor import NIHDrugExtractor
from Backend.drugapprovalchecker import DrugApprovalChecker
from Backend.config import cancer_type_to_url2

class NIHDrugApprover:
    """
    A class to manage the extraction of approved drugs for specific cancer types from the NIH website 
    and check whether the drugs from a provided list are approved.
    """

    def __init__(self, cancer_type):
        """
        Initialize the NIHDrugApprover with the type of cancer to extract drugs for.

        Parameters:
        -----------
        cancer_type : str
            The type of cancer for which drug approvals need to be checked.
        """
        self.cancer_type = cancer_type
        self.url, self.section_title = self._get_cancer_drug_info()

    def _get_cancer_drug_info(self):
        """
        Determine the URL and section title based on the provided cancer type.

        Returns:
        --------
        tuple
            A tuple containing the URL of the NIH page and the relevant section title for drug extraction.

        Raises:
        -------
        ValueError:
            If an unknown cancer type is provided, this error is raised.
        """
        cancer_type_to_url = cancer_type_to_url2
        if self.cancer_type not in cancer_type_to_url:
            raise ValueError(f"Unknown cancer type: {self.cancer_type}")

        return cancer_type_to_url[self.cancer_type]

    def NIH_extract_drugs(self, matched_drug_gpi):
        """
        Scrape the NIH cancer treatment page for approved drugs and check them against the provided list.

        Parameters:
        -----------
        matched_drug_gpi : list
            A list of drugs with their GPI codes that need to be checked for approval.

        Returns:
        --------
        list
            A list of drugs that are approved by the NIH, filtered from the provided list.
        """
        scraper = WebScraper()
        html_content = scraper.scrape(url=self.url)
        extractor = NIHDrugExtractor(html_content)
        approved_drugs_from_NIH = extractor.extract_drugs(self.section_title)
        drugapprovechecker = DrugApprovalChecker(approved_drugs_from_NIH)
        final_approved_drugs = drugapprovechecker.check_approval(matched_drug_gpi)

        return final_approved_drugs
