"""
PDF Resume to HTML Converter
This script extracts text from a PDF resume and converts it to a styled HTML file.
"""

import PyPDF2
import os
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""


def parse_resume_sections(text):
    """
    Parse common resume sections from extracted text.
    
    Args:
        text (str): Extracted resume text
        
    Returns:
        dict: Dictionary containing parsed resume sections
    """
    sections = {
        'header': '',
        'contact': '',
        'summary': '',
        'experience': '',
        'education': '',
        'skills': '',
        'projects': '',
        'other': ''
    }
    
    # Basic parsing - customize based on your resume structure
    lines = text.split('\n')
    current_section = 'header'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect section headers
        if 'CONTACT' in line.upper() or 'EMAIL' in line.upper():
            current_section = 'contact'
        elif 'EXPERIENCE' in line.upper() or 'WORK' in line.upper():
            current_section = 'experience'
        elif 'EDUCATION' in line.upper():
            current_section = 'education'
        elif 'SKILLS' in line.upper():
            current_section = 'skills'
        elif 'PROJECT' in line.upper():
            current_section = 'projects'
        elif 'SUMMARY' in line.upper() or 'OBJECTIVE' in line.upper():
            current_section = 'summary'
        else:
            sections[current_section] += line + '\n'
    
    return sections


def create_html_resume(sections, output_path='resume.html'):
    """
    Create a styled HTML resume from parsed sections.
    
    Args:
        sections (dict): Dictionary containing resume sections
        output_path (str): Output HTML file path
    """
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume - Ariel Olea</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Cambria', 'Calibri', serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        
        .header {
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .contact-info {
            font-size: 0.95em;
            color: #555;
        }
        
        .contact-info a {
            color: #3498db;
            text-decoration: none;
        }
        
        .contact-info a:hover {
            text-decoration: underline;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .job, .education-entry, .project-entry {
            margin-bottom: 20px;
        }
        
        .job-title, .degree, .project-title {
            font-weight: bold;
            font-size: 1.1em;
            color: #2c3e50;
        }
        
        .company, .school, .project-info {
            font-style: italic;
            color: #555;
            margin-bottom: 5px;
        }
        
        .date {
            color: #7f8c8d;
            font-size: 0.95em;
            margin-bottom: 8px;
        }
        
        .description, .details {
            margin-left: 20px;
            color: #333;
            line-height: 1.8;
        }
        
        .description ul, .details ul {
            list-style-position: inside;
            margin-top: 10px;
        }
        
        .description li, .details li {
            margin-bottom: 8px;
            margin-left: 20px;
        }
        
        .skills-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        
        .skill-tag {
            background-color: #ecf0f1;
            color: #2c3e50;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.95em;
            border-left: 3px solid #3498db;
        }
        
        .summary-text {
            line-height: 1.8;
            color: #333;
            font-size: 1em;
        }
        
        @media print {
            body {
                background-color: white;
                padding: 0;
            }
            
            .container {
                box-shadow: none;
                padding: 20px;
            }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .section-title {
                font-size: 1.2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Ariel Olea</h1>
            <div class="contact-info">
                <p>📧 Email: <a href="mailto:olea.ariel.ariate@gmail.com">olea.ariel.ariate@gmail.com</a></p>
                <p>📍 Location: [Your Location]</p>
                <p>🔗 <a href="#">LinkedIn</a> | <a href="#">GitHub</a></p>
            </div>
        </div>
"""
    
    # Add Summary Section
    if sections['summary'].strip():
        html_content += f"""
        <div class="section">
            <h2 class="section-title">Professional Summary</h2>
            <div class="summary-text">
                {sections['summary'].strip()}
            </div>
        </div>
"""
    
    # Add Experience Section
    if sections['experience'].strip():
        html_content += f"""
        <div class="section">
            <h2 class="section-title">Professional Experience</h2>
            <div class="description">
                {sections['experience'].strip()}
            </div>
        </div>
"""
    
    # Add Education Section
    if sections['education'].strip():
        html_content += f"""
        <div class="section">
            <h2 class="section-title">Education</h2>
            <div class="details">
                {sections['education'].strip()}
            </div>
        </div>
"""
    
    # Add Skills Section
    if sections['skills'].strip():
        html_content += f"""
        <div class="section">
            <h2 class="section-title">Skills</h2>
            <div class="skills-list">
                {sections['skills'].strip()}
            </div>
        </div>
"""
    
    # Add Projects Section
    if sections['projects'].strip():
        html_content += f"""
        <div class="section">
            <h2 class="section-title">Projects</h2>
            <div class="description">
                {sections['projects'].strip()}
            </div>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML resume created successfully: {output_path}")


def convert_pdf_to_html(pdf_path, output_html='resume.html'):
    """
    Main function to convert PDF resume to HTML.
    
    Args:
        pdf_path (str): Path to the PDF resume file
        output_html (str): Output HTML file path
    """
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found at {pdf_path}")
        return False
    
    print(f"📄 Reading PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("❌ Failed to extract text from PDF")
        return False
    
    print("🔄 Parsing resume sections...")
    sections = parse_resume_sections(text)
    
    print("🎨 Creating HTML resume...")
    create_html_resume(sections, output_html)
    
    return True


if __name__ == "__main__":
    # Configuration
    PDF_PATH = "Ariel_Olea_Resume.pdf"  # Change this to your PDF filename
    OUTPUT_HTML = "resume.html"
    
    # Convert PDF to HTML
    success = convert_pdf_to_html(PDF_PATH, OUTPUT_HTML)
    
    if success:
        print(f"\n✨ Resume conversion complete!")
        print(f"📁 Output file: {OUTPUT_HTML}")
