from Backend.pdfparser import PDFTextExtractor
import os

class PDFHandler:
    """
    A class responsible for handling PDF-related operations, including saving uploaded PDFs 
    and extracting text from them.
    """

    def __init__(self, upload_folder):
        """
        Initialize the PDFHandler with a specific folder where PDF files will be saved.

        Parameters:
        -----------
        upload_folder : str
            The directory path where uploaded PDF files will be stored.
        """
        self.upload_folder = upload_folder

    def save_pdf(self, pdf_file):
        """
        Save the uploaded PDF file to the designated upload folder.

        Parameters:
        -----------
        pdf_file : FileStorage
            The PDF file object uploaded by the user.

        Returns:
        --------
        str
            The full file path where the PDF was saved.
        """
        filepath = os.path.join(self.upload_folder, pdf_file.filename)
        pdf_file.save(filepath)
        return filepath

    def extract_text(self, filepath):
        """
        Extract text from the specified PDF file using the PDFTextExtractor class.

        Parameters:
        -----------
        filepath : str
            The path of the PDF file from which the text needs to be extracted.

        Returns:
        --------
        str
            The extracted text content from the PDF.
        """
        pdf_extractor = PDFTextExtractor(filepath)
        return pdf_extractor.extract_text()
