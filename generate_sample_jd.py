"""
Run this script to generate a sample JD PDF for testing.
Usage (from project root, with venv active):
    python generate_sample_jd.py
"""
import subprocess, sys, os

# Auto-install fpdf2 if missing
try:
    from fpdf import FPDF
except ImportError:
    print("Installing fpdf2...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2"])
    from fpdf import FPDF


def create_sample_jd(output_path="sample_jd.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, "Job Description: Senior Python Backend Developer", ln=True)
    pdf.set_draw_color(100, 100, 255)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    # Meta info
    meta = [
        ("Company", "TechCorp Solutions Pvt. Ltd."),
        ("Location", "Bangalore, India (Hybrid)"),
        ("Experience", "3-6 Years"),
        ("Employment Type", "Full-Time"),
        ("Posted On", "June 2025"),
    ]
    pdf.set_font("Helvetica", "", 11)
    for label, value in meta:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(50, 8, f"{label}:")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, value, ln=True)

    pdf.ln(4)

    def section(title):
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Helvetica", "", 11)

    def bullet(text):
        pdf.cell(6, 7, "-")
        pdf.multi_cell(0, 7, text)

    # About the Role
    section("About the Role")
    pdf.multi_cell(
        0, 7,
        "We are looking for a Senior Python Backend Developer to design, build, and "
        "maintain high-performance APIs and microservices. You will collaborate closely "
        "with frontend teams, data engineers, and product managers to deliver scalable solutions."
    )

    # Responsibilities
    section("Key Responsibilities")
    for r in [
        "Design and develop RESTful APIs using FastAPI or Django REST Framework.",
        "Build and maintain microservices using Python 3.10+.",
        "Write clean, testable, and well-documented code.",
        "Optimize SQL/NoSQL database queries (PostgreSQL, MongoDB).",
        "Integrate third-party APIs and external services.",
        "Participate in code reviews and mentor junior developers.",
        "Collaborate with DevOps to deploy services on AWS/GCP.",
        "Monitor application performance and debug production issues.",
    ]:
        bullet(r)

    # Required Skills
    section("Required Skills")
    for s in [
        "Python (3.8+), FastAPI, Django",
        "PostgreSQL, MongoDB, Redis",
        "Docker, Kubernetes, CI/CD pipelines (GitHub Actions / Jenkins)",
        "REST API design, OAuth2 / JWT authentication",
        "Git, GitHub/GitLab branching workflows",
        "Unit and integration testing with pytest",
        "Linux command-line proficiency",
    ]:
        bullet(s)

    # Qualifications
    section("Qualifications")
    pdf.multi_cell(
        0, 7,
        "B.Tech / B.E. / M.Tech in Computer Science or a related field.\n"
        "3+ years of hands-on Python backend development experience.\n"
        "Strong understanding of software design patterns and SOLID principles."
    )

    # Nice to Have
    section("Nice to Have")
    for n in [
        "Experience integrating AI/ML APIs (OpenAI, Google Gemini, HuggingFace)",
        "Knowledge of message queues: Apache Kafka or RabbitMQ",
        "Familiarity with infrastructure-as-code (Terraform, Ansible)",
        "Prior experience with resume parsing or HR-tech products",
    ]:
        bullet(n)

    # Salary & Benefits
    section("Compensation & Benefits")
    pdf.multi_cell(
        0, 7,
        "Competitive salary: INR 15-30 LPA (based on experience)\n"
        "Health insurance, flexible working hours, remote-friendly\n"
        "Learning & development budget, stock options"
    )

    pdf.output(output_path)
    print(f"Sample JD PDF created: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    create_sample_jd("sample_jd.pdf")
