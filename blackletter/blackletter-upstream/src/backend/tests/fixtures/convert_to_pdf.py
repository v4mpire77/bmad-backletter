from fpdf import FPDF
import os

def text_to_pdf(txt_path, pdf_path):
    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Read and write text file content
    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Encode to avoid FPDF errors with special characters
            pdf.multi_cell(0, 5, txt=line.strip())
    
    # Save PDF
    pdf.output(pdf_path)

def convert_all_samples():
    fixtures_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Convert each .txt file to PDF
    for filename in os.listdir(fixtures_dir):
        if filename.endswith('.txt'):
            txt_path = os.path.join(fixtures_dir, filename)
            pdf_path = os.path.join(fixtures_dir, filename.replace('.txt', '.pdf'))
            text_to_pdf(txt_path, pdf_path)
            print(f"Created {pdf_path}")

if __name__ == "__main__":
    convert_all_samples()
