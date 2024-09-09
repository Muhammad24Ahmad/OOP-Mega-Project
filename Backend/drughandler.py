from Backend.ner import NERDrugExtractor
from Backend.llm import LLMDrugExtractor

from Backend.config import chunk_size

class DrugHandler:
    """
    A class to handle drug extraction from text content using different models.

    Parameters:
    -----------
    model_option : str
        The model to use for extraction ('NER' or 'LLM').
    text_content : str
        The text content from which drugs need to be extracted.
    """

    def __init__(self, model_option, text_content):
        """
        Initializes the DrugHandler with the specified model and text content.

        Parameters:
        -----------
        model_option : str
            The extraction model option ('NER' or 'LLM').
        text_content : str
            The input text content for drug extraction.
        """
        self.model_option = model_option
        self.text_content = text_content

    def extract_drugs(self):
        """
        Extracts drugs from the provided text using the specified model.

        If 'NER' is selected, it uses the NER (Named Entity Recognition) model to extract drugs.
        If 'LLM' is selected, it chunks the text and uses a language model to generate responses for extraction.

        Returns:
        --------
        list
            A list of extracted drugs based on the selected model.

        Raises:
        -------
        ValueError
            If the model_option is not 'NER' or 'LLM'.
        """
        if self.model_option == 'NER':
            # Use the NERDrugExtractor class
            extractor = NERDrugExtractor()  # Initialize the NER extractor
            result = extractor.extract_drugs(self.text_content, chunk_size)  # Extract drugs
        elif self.model_option == 'LLM':
            llm = LLMDrugExtractor()
            chunks = llm.chunk_text(self.text_content)
            all_responses = []
            for chunk in chunks:
                prompt = llm.prepare_prompt(chunk)
                response = llm.get_response(prompt)
                all_responses.append(response)
            result = llm.extract_drugs_from_responses(all_responses)
        else:
            raise ValueError("Invalid model option selected")
        
        return result
