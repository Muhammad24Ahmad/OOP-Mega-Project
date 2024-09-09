import os
from flask import Flask, render_template, request, flash, redirect, session, url_for, send_from_directory
from Backend.pdfhandler import PDFHandler
from Backend.drughandler import DrugHandler
from Backend.gpihandler import GPIHandler
from Backend.nihhandler import NIHHandler
from Backend.filegenerator import FileHandler
from Backend.config import UPLOAD_FOLDER


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define the upload folder path
UPLOAD_FOLDER = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    return render_template('demo.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)

    pdf_files = request.files.getlist('pdf_file')

    if not pdf_files or pdf_files[0].filename == '':
        flash('No selected files', 'danger')
        return redirect(request.url)

    # PDF Handler instance
    pdf_handler = PDFHandler(app.config['UPLOAD_FOLDER'])

    text_content = ""
    for pdf_file in pdf_files:
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            filepath = pdf_handler.save_pdf(pdf_file)
            flash(f'File {pdf_file.filename} uploaded and saved successfully!', 'success')
            text_content += pdf_handler.extract_text(filepath)
        else:
            flash(f'{pdf_file.filename} is not a valid PDF file', 'danger')
            return redirect(request.url)

    # Check which model option is selected
    session['model_option'] = request.form.get('modelOption')
    session.modified = True

    # Drug extraction
    extractor = DrugHandler(session['model_option'], text_content)
    result = extractor.extract_drugs()

    # GPI Code Extraction
    gpi_matcher = GPIHandler('filtered_drug_gpi.csv')
    matched_drug_gpi = gpi_matcher.match_drugs(result)

    # Save the matched drug list in the session
    session['matched_drug_gpi'] = matched_drug_gpi
    session.modified = True

    flash('Processing completed successfully!', 'success')
    return render_template('demo.html', matched_drug_gpi=session['matched_drug_gpi'])


@app.route('/nihcheck', methods=['POST'])
def nih_check():
    if 'matched_drug_gpi' not in session:
        flash('No drug data available. Please extract drugs first.', 'danger')
        return redirect(url_for('demo'))

    # Get the selected cancer type from the form
    cancer_type = request.form.get('carrierType')
    if cancer_type == "---Select a Cancer Type---":
        flash('Please select a cancer type.', 'danger')
        return render_template('demo.html', matched_drug_gpi=session['matched_drug_gpi'])

    session['cancer_type'] = cancer_type

    # NIH Approval Check
    nih_checker = NIHHandler(cancer_type)
    approved_list = nih_checker.get_approved_drugs(session['matched_drug_gpi'])

    # Save the matched drug list in the session
    session['approved_drug_list'] = approved_list
    session.modified = True
    flash('NIH Approval Check completed successfully!', 'success')

    return render_template('demo.html', approved_list=approved_list, cancer_type=cancer_type)


@app.route('/download', methods=['POST'])
def download():
    if 'approved_drug_list' not in session:
        flash('No drug data available. Please extract drugs first.', 'danger')
        return redirect(url_for('demo'))

    cancer_type = session['cancer_type']
    model_name = session['model_option']
    approved_drugs_list = session['approved_drug_list']
    extension = request.form.get('extension')


    # File Generation
    file_generator = FileHandler(approved_drugs_list, cancer_type, model_name)
    file_path = file_generator.generate_file(extension)

    folder = os.path.dirname(file_path)
    filename = os.path.basename(file_path)

    try:
        return send_from_directory(folder, filename, as_attachment=True)
    except FileNotFoundError:
        return "The requested file was not found on the server.", 404


if __name__ == "__main__":
    app.run(debug=True)
