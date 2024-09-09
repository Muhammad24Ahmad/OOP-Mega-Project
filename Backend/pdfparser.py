import pdfplumber
import re

class PDFTextExtractor:
    """
    A class for extracting, cleaning, and saving text from PDF files.
    """

    def __init__(self, pdf_path):
        """
        Initialize the PDFTextExtractor with the path of the PDF file.

        Parameters:
        -----------
        pdf_path : str
            The file path of the PDF from which text is to be extracted.
        """
        self.pdf_path = pdf_path
        self.cleaned_text = ""

    def clean_text(self, text):
        """
        Clean the extracted text by removing unwanted characters.

        Parameters:
        -----------
        text : str
            The raw text extracted from the PDF.

        Returns:
        --------
        str
            The cleaned text after removing unwanted characters.
        """
        # Replace newline characters with spaces
        text = text.replace('\n', ' ')

        # Define a regex pattern to keep only letters, numbers, and spaces
        pattern = r'[^a-zA-Z0-9 -]'

        # Remove unwanted characters based on the pattern
        self.cleaned_text = re.sub(pattern, '', text)
        return self.cleaned_text

    def extract_text(self):
        """
        Extract text from the PDF file.

        Returns:
        --------
        str
            The cleaned text extracted from the PDF.
        """
        text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            # Clean the extracted text
            self.cleaned_text = self.clean_text(text)
        except Exception as e:
            print(f"An error occurred while reading the PDF: {e}")
            self.cleaned_text = ""
        return self.cleaned_text

    def save_text_to_file(self, output_text_file="TextFromPDF.txt"):
        """
        Save the cleaned text to a text file.

        Parameters:
        -----------
        output_text_file : str, optional
            The file name for saving the cleaned text. Defaults to 'TextFromPDF.txt'.
        """
        if self.cleaned_text:
            try:
                with open(output_text_file, 'w', encoding='utf-8') as f:
                    f.write(self.cleaned_text)
                print(f"Text extracted from the PDF has been saved to '{output_text_file}'.")
            except Exception as e:
                print(f"An error occurred while saving the file: {e}")
        else:
            print("No text to save. Please extract text from the PDF first.")

    @staticmethod
    def read_text_file(file_path):
        """
        Read and return the content of a text file.

        Parameters:
        -----------
        file_path : str
            The file path of the text file to be read.

        Returns:
        --------
        str
            The content of the text file, or None if an error occurs.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"The file at {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage:
# if __name__ == "__main__":
#     pdf_extractor = PDFTextExtractor("sample.pdf")  # Replace 'sample.pdf' with your actual file path

#     # Extract text from PDF
#     extracted_text = pdf_extractor.extract_text()
#     print("Extracted Text:", extracted_text)

#     # Save the extracted text to a file
#     pdf_extractor.save_text_to_file("TextFromPDF.txt")

#     # Read and print the content of the saved text file
#     saved_content = PDFTextExtractor.read_text_file("TextFromPDF.txt")
#     print("Saved Content:", saved_content)
