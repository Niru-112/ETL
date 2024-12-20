from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def generate_resume(output_pdf_path):
    # Create a PDF canvas object
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    
    # Set up some basic font styles
    c.setFont("Helvetica", 12)

    # Title: Resume Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 750, "Your Name")
    c.setFont("Helvetica", 12)
    c.drawString(100, 735, "Contact Information: Email | Phone | LinkedIn")

    # Personal Information Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 700, "Personal Information")
    c.setFont("Helvetica", 12)
    c.drawString(100, 685, "Date of Birth: MM/DD/YYYY")
    c.drawString(100, 670, "Address: Your Address Here")
    
    # Objective Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 630, "Objective")
    c.setFont("Helvetica", 12)
    c.drawString(100, 615, "A brief description of your career goals and aspirations.")

    # Education Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 570, "Education")
    c.setFont("Helvetica", 12)
    c.drawString(100, 555, "Degree | University Name | Graduation Year")
    c.drawString(100, 540, "Relevant coursework: List relevant courses.")

    # Experience Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 500, "Experience")
    c.setFont("Helvetica", 12)
    c.drawString(100, 485, "Job Title | Company Name | Duration")
    c.drawString(100, 470, "- Responsibilities and achievements go here.")
    
    # Skills Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 430, "Skills")
    c.setFont("Helvetica", 12)
    c.drawString(100, 415, "List your technical skills (e.g., Python, Java, etc.).")
    
    # End the PDF
    c.showPage()
    c.save()

    print(f"Resume generated successfully and saved as {output_pdf_path}")

# Example usage
output_pdf_path = 'resume_template.pdf'  # Path to save the generated resume
generate_resume(output_pdf_path)
