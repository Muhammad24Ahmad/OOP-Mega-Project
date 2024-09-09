from transformers import (AutoModelForTokenClassification, AutoTokenizer, pipeline)
import re
from Backend.config import model_checkpoint, chunk_size

class NERDrugExtractor:
    """
    A class to extract drug-related entities from text using a NER model.
    """

    def __init__(self, model_checkpoint=model_checkpoint, num_labels=5):
        """
        Initialize the NERDrugExtractor with the specified model and tokenizer.

        Parameters:
        -----------
        model_checkpoint : str
            The model to use for token classification.
        num_labels : int
            The number of labels for the NER model.
        """
        self.model_checkpoint = model_checkpoint
        self.num_labels = num_labels
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_checkpoint, num_labels=self.num_labels,
                                                                     id2label={0: 'O', 1: 'B-DRUG', 2: 'I-DRUG', 3: 'B-EFFECT', 4: 'I-EFFECT'})
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_checkpoint)
        self.pipeline = pipeline(task="ner", model=self.model, tokenizer=self.tokenizer)
    
    def split_into_chunks(self, text, chunk_size=chunk_size):
        """
        Split text into chunks of specified size for NER processing.

        Parameters:
        -----------
        text : str
            The text to split.
        chunk_size : int
            Size of each chunk.

        Returns:
        --------
        list
            List of text chunks.
        """
        if chunk_size <= 0:
            raise ValueError("Chunk size must be a positive integer")
        
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    def extract_drugs(self, text, chunk_size=chunk_size):
        """
        Extract drug entities from text using NER.

        Parameters:
        -----------
        text : str
            The text from which to extract drugs.
        chunk_size : int
            Size of chunks to process.

        Returns:
        --------
        list
            A list of extracted drug names.
        """
        chunks = self.split_into_chunks(text, chunk_size)
        all_ner_results = []

        for chunk in chunks:
            ner_results = self.pipeline(chunk)
            all_ner_results.extend(ner_results)

        return self._process_entities(all_ner_results)
    
    def _process_entities(self, all_ner_results):
        """
        Process the extracted NER entities.

        Parameters:
        -----------
        all_ner_results : list
            The results from the NER pipeline.

        Returns:
        --------
        list
            A list of processed drug entities.
        """
        word_entities = []
        current_word = ""
        current_label = ""
        start_idx, end_idx = -1, -1

        for entity in all_ner_results:
            if entity['entity'] == "I-DRUG" and current_label == "B-DRUG":
                if entity['word'].startswith("##"):
                    current_word += entity['word'][2:]  # Combine sub-token
                else:
                    current_word += entity['word']
                end_idx = entity['end']

            elif entity['entity'] == "I-EFFECT" and current_label == "B-EFFECT":
                if entity['word'].startswith("##"):
                    current_word += entity['word'][2:]  # Combine sub-token
                else:
                    current_word += entity['word']
                end_idx = entity['end']

            else:
                if current_word:  # Save the previous word and its label
                    word_entities.append({
                        "word": current_word,
                        "label": current_label,
                        "start": start_idx,
                        "end": end_idx
                    })
                current_word = entity['word']
                current_label = entity['entity']
                start_idx = entity['start']
                end_idx = entity['end']

        if current_word:
            word_entities.append({
                "word": current_word,
                "label": current_label,
                "start": start_idx,
                "end": end_idx
            })

        return self._filter_drugs(word_entities)

    def _filter_drugs(self, word_entities):
        """
        Filter drug-related entities from the processed entities.

        Parameters:
        -----------
        word_entities : list
            A list of processed NER entities.

        Returns:
        --------
        list
            A list of drug names.
        """
        Drugs = []
        current_drug = ""
        current_start = None

        for entity in word_entities:
            if entity['label'] == 'B-DRUG':  # Beginning of a new drug
                if current_drug:
                    Drugs.append({
                        "word": current_drug,
                        "label": 'DRUG',
                        "start": current_start,
                        "end": entity['start'] - 1
                    })
                current_drug = entity['word']
                current_start = entity['start']
            elif entity['label'] == 'I-DRUG':  # Continuation of the current drug
                current_drug += entity['word']
            else:
                if current_drug:
                    Drugs.append({
                        "word": current_drug,
                        "label": 'DRUG',
                        "start": current_start,
                        "end": entity['start'] - 1
                    })
                current_drug = ""
                current_start = None

        if current_drug:
            Drugs.append({
                "word": current_drug,
                "label": 'DRUG',
                "start": current_start,
                "end": word_entities[-1]['end']
            })

        return [drug['word'].lower() for drug in Drugs]


# # Example Usage
# if __name__ == "__main__":
#     text = "Sample text to extract drugs like Aspirin and Ibuprofen for testing purposes."

#     extractor = NERDrugExtractor()
#     drugs = extractor.extract_drugs(text)

#     print("Extracted Drugs:", drugs)
