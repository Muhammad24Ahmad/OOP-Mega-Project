from bs4 import BeautifulSoup


class NIHDrugExtractor:
    """A class to extract drug information from the scraped HTML."""

    def __init__(self, html_content):
        """Initialize the extractor with the scraped HTML content."""
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_drugs(self, section_title):
        """
        Extract the list of drugs from the given section of the HTML content.

        Parameters:
        - section_title: The title of the section to look for (e.g., 'Drugs Approved for Colon Cancer').

        Returns:
        - A list of drugs found under the given section.
        """
        section = self.soup.find('h2', text=section_title)
        if section:
            drugs_list = section.find_next('ul')
            drugs = [li.get_text() for li in drugs_list.find_all('li')]
            return drugs
        return []