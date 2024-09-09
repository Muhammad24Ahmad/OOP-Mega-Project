import requests
import torch
import re
from Backend.config import api_url, max_words

class LLMDrugExtractor:

    def __init__(self, api_url=api_url , max_words=max_words):
        """
        Initialize the DrugExtractor with an API URL and max words per chunk.
        
        Parameters:
        - api_url: The API endpoint URL to send requests to.
        - max_words: The maximum number of words per chunk when splitting the text.
        """
        self.api_url = api_url
        self.max_words = max_words

    def chunk_text(self, text):
        """
        Split the input text into chunks of the specified maximum word count.
        
        Parameters:
        - text: The text to be chunked.
        
        Returns:
        - A list of text chunks.
        """
        words = text.split()
        chunks = [' '.join(words[i:i + self.max_words]) for i in range(0, len(words), self.max_words)]
        return chunks

    def get_response(self, prompt):
        """
        Get a response from the API by sending the prompt and handling the response.
        
        Parameters:
        - prompt: The prompt to send to the API.
        
        Returns:
        - The generated response from the API.
        """
        with torch.no_grad(), torch.inference_mode():
            response = requests.post(
                url=self.api_url,
                json={'prompt': prompt}
            )
            return response.json().get('response', '')

    def prepare_prompt(self, text_chunk):
        """
        Prepare the prompt for the API by formatting the system and user messages.
        
        Parameters:
        - text_chunk: The text chunk to be used in the prompt.
        
        Returns:
        - A list containing the system and user messages formatted for the API.
        """
        my_prompt = [
            {
                'role': 'system',
                'content': """
                You are an expert Data Analyst with 20 years of experience.
                Your task is to find and extract Drug names from the given text in the form of a Python list.
                OUTPUT FORMAT: In case you do not find any drugs in the text, then just return an empty Python list.
                IMPORTANT: YOU ARE NOT VERBOSE.
                """.strip().replace('\t', '')
            },
            {'role': 'user', 'content': text_chunk},
        ]
        return my_prompt

    def extract_drugs_from_responses(self, responses):
        """
        Extract drug names from the list of responses using regular expressions.
        
        Parameters:
        - responses: A list of responses containing possible drug names.
        
        Returns:
        - A list of extracted drug names.
        """
        all_drugs = []

        for response in responses:
            extracted_lists = re.findall(r"\[.*?\]", response)
            for item_list in extracted_lists:
                try:
                    drugs = eval(item_list)
                    if isinstance(drugs, list):
                        all_drugs.extend(drugs)
                except Exception as e:
                    print(f"Could not parse the list: {item_list}. Error: {e}")
        
        return all_drugs

    def extract_drugs_from_text(self, text):
        """
        Main method to chunk the text, send API requests, and extract drug names.
        
        Parameters:
        - text: The input text from which drug names are to be extracted.
        
        Returns:
        - A list of extracted drug names.
        """
        text_chunks = self.chunk_text(text)
        responses = []

        for chunk in text_chunks:
            prompt = self.prepare_prompt(chunk)
            response = self.get_response(prompt)
            responses.append(response)

        drugs = self.extract_drugs_from_responses(responses)
        return drugs


# Example Usage
# if __name__ == "__main__":
#     api_url = "http://172.16.101.171:8002/notes/"  # Replace with the actual API URL
#     text = "Sample text with drugs like Aspirin and Ibuprofen. We need to extract them."

#     extractor = LLMDrugExtractor(api_url)
#     extracted_drugs = extractor.extract_drugs_from_text(text)

#     print("Extracted Drugs:", extracted_drugs)
