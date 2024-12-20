from fpdf import FPDF

class ResumePDF(FPDF):
    def header(self):
        # Header with name and contact details
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 0, 0)  # Black text color
        self.cell(0, 10, "John Doe", ln=True, align='L')  # Replace with your name
        self.set_font("Arial", size=11)
        self.cell(0, 8, "123 Your Street, Your City, ST 12345", ln=True, align='L')
        self.cell(0, 8, "Phone: (123) 456-7890 ", ln=True, align='L')
        self.cell(0, 8, "Email: john.doe@example.com", ln=True, align='L')
        self.ln(10)

    def add_section_title(self, title):
        """Add a bold section title."""
        self.set_font("Arial", "B", 13)
        self.set_text_color(255, 0, 0) 
        self.cell(0, 8, title, ln=True, align='L')
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def add_bullet_point(self, text):
        """Add a bullet point."""
        self.set_font("Arial", size=10)
        self.cell(8)  # Indentation for bullets
        self.cell(0, 6, f"- {text}", ln=True)

    def add_paragraph(self, text):
        """Add a paragraph for section content."""
        self.set_font("Arial", size=10)
        self.multi_cell(0, 6, text)
        self.ln(3)

# Initialize PDF
pdf = ResumePDF()
pdf.set_left_margin(15)  # Set left margin to match your resume
pdf.set_right_margin(15)  # Set right margin
pdf.add_page()

# Header Section
pdf.set_y(45)  # Adjust vertical position for header alignment

# Skills Section
pdf.add_section_title("Skills")
skills = [
    "Python Programming",
    "Data Analysis & Visualization",
    "Machine Learning",
    "Web Development (HTML, CSS, JavaScript)"
]
for skill in skills:
    pdf.add_bullet_point(skill)
pdf.ln(5)

# Experience Section
pdf.add_section_title("Experience")
pdf.add_paragraph("JAN 2020 - PRESENT")
pdf.add_bullet_point("Software Engineer at ABC Corp")
experience_details = [
    "Developed scalable web applications using Python and Flask.",
    "Improved performance of data pipelines by 30% through optimized ETL scripts.",
    "Collaborated with cross-functional teams to deliver high-quality products."
]
for detail in experience_details:
    pdf.add_bullet_point(detail)
pdf.ln(5)

pdf.add_paragraph("JAN 2018 - DEC 2019")
pdf.add_bullet_point("Junior Developer at XYZ Solutions")
junior_experience = [
    "Built user-friendly interfaces with HTML, CSS, and JavaScript.",
    "Assisted in database design and maintenance.",
    "Tested applications for performance and security issues."
]
for exp in junior_experience:
    pdf.add_bullet_point(exp)
pdf.ln(5)

pdf.add_paragraph("JAN 2018 - DEC 2019")
pdf.add_bullet_point("Junior Developer at XYZ Solutions")
junior_experience = [
    "Built user-friendly interfaces with HTML, CSS, and JavaScript.",
    "Assisted in database design and maintenance.",
    "Tested applications for performance and security issues."
]
for exp in junior_experience:
    pdf.add_bullet_point(exp)
pdf.ln(0)

# Education Section
pdf.add_section_title("Education")
education_details = [
    "Bachelor of Technology in Computer Science, XYZ University (2015 - 2019)",
    "GPA: 3.8/4.0",
    "Relevant Courses: Data Structures, Algorithms, Machine Learning"
]
for edu in education_details:
    pdf.add_bullet_point(edu)
pdf.ln(0)

# Awards Section
pdf.add_section_title("Awards & Achievements")
awards = [
    "Dean's List for Academic Excellence (2017, 2018)",
    "First Place in Hackathon 2020 organized by TechWorld",
]
for award in awards:
    pdf.add_bullet_point(award)
pdf.ln(0)

# Save the PDF
pdf.output("Resume.pdf")
print("Resume PDF created successfully!")