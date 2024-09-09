api_url = "http://172.16.101.171:8002/notes/"

max_words=1000

model_checkpoint="scibert2"

chunk_size = 512

UPLOAD_FOLDER = 'uploads'

cancer_type_to_url2 = {
            'Colon Cancer': (
            'https://www.cancer.gov/about-cancer/treatment/drugs/colorectal', 'Drugs Approved for Colon Cancer'),
            'Lung Cancer': ('https://www.cancer.gov/about-cancer/treatment/drugs/lung',
                            'Drugs Approved for Non-Small Cell Lung Cancer'),
            'Breast Cancer': (
            'https://www.cancer.gov/about-cancer/treatment/drugs/breast', 'Drugs Approved to Treat Breast Cancer'),
            'Prostate Cancer': (
            'https://www.cancer.gov/about-cancer/treatment/drugs/prostate', 'Drugs Approved for Prostate Cancer'),
            'Multiple Myeloma': ('https://www.cancer.gov/about-cancer/treatment/drugs/multiple-myeloma',
                                 'Drugs Approved for Multiple Myeloma and Other Plasma Cell Neoplasms')
        }
