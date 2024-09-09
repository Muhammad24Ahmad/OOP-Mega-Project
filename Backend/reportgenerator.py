from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os
import json

class ReportGenerator:
    """A class to generate reports in various formats."""

    def __init__(self, approved_drugs_list, cancer_type, model_name):
        """
        Initialize the ReportGenerator with the list of approved drugs, cancer type, and model name.

        Parameters:
        -----------
        approved_drugs_list : list
            A list of dictionaries containing information about approved drugs.
        cancer_type : str
            The type of cancer for which the report is being generated.
        model_name : str
            The name of the model used for generating the drug list.
        """
        self.approved_drugs_list = approved_drugs_list
        self.cancer_type = cancer_type
        self.model_name = model_name
        self.directory = 'Reports'
        if not os.path.exists(self.directory):
            print("Directory does not exist. Creating directory...")
            os.makedirs(self.directory)
    
    def create_pdf_report(self):
        """
        Creates a PDF report with the list of approved drugs.

        Returns:
        --------
        str
            The file path of the created PDF report.
        """
        filename = f"{self.cancer_type} Drugs Report by {self.model_name}.pdf"
        pdf_file_path = os.path.join(self.directory, filename)
        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        width, height = letter

        # Draw the heading at the top, centered
        c.setFont('Helvetica-Bold', 16)
        c.drawCentredString(width / 2, height - 40, f"{self.cancer_type} Drugs Report by {self.model_name}")

        # Define the table data with headers
        table_data = [['Serial No.', 'Drug Name', 'GPI Code']]
        for i, drug in enumerate(self.approved_drugs_list, start=1):
            table_data.append([i, drug['Drug'], drug['GPI']])

        # Create the table
        drug_table = Table(table_data, colWidths=[75, 250, 100])
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
        ])
        drug_table.setStyle(table_style)
        
        # Apply row-specific background color for rows where approval is False
        for i, drug in enumerate(self.approved_drugs_list, start=1):
            if not drug['approval']:
                drug_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.yellow)]))
        
        # Calculate the table width and position
        table_width, table_height = drug_table.wrap(0, 0)
        x = (width - table_width) / 2
        y = height - table_height - 60

        # Draw the table on the canvas
        drug_table.drawOn(c, x, y)

        # Save the PDF
        c.save()
        print(f"PDF created at {pdf_file_path}")
        return pdf_file_path

    def save_to_json_file(self):
        """
        Saves the list of approved drugs to a JSON file.

        Returns:
        --------
        str
            The file path of the created JSON file.
        """
        file_name = f"{self.cancer_type} Drugs Report by {self.model_name}.json"
        json_file_path = os.path.join(self.directory, file_name)
        try:
            with open(json_file_path, 'w') as json_file:
                json.dump(self.approved_drugs_list, json_file, indent=4)
            print(f"Data successfully written to {file_name}")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")
        return json_file_path
