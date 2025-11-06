# Internship Assistant

An open-source CLI tool to help CS students streamline job and internship applications responsibly.
# Internship Assistant Webapp

A **Streamlit-powered web application** that helps students search for internships, track applications, and generate personalized cover letters.  
Built with **Python, Streamlit, and ATS integrations (Ashby + Greenhouse)**.

---

## Features

- **Multi-ATS job search**  
  Searches internships across companies using **Ashby** and **Greenhouse** job boards.

-  **Smart filters**  
  Filter results by keywords (e.g., `"intern, software"`) and location (e.g., `"remote, Canada"`).

-  **Application tracker**  
  Saves all searched jobs into a CSV tracker for progress monitoring.

-  **Cover letter generator**  
  Generates tailored cover letters in **Markdown + PDF** from Jinja2 templates.

-  **Streamlit webapp**  
  Clean user interface with sidebar controls and interactive tables.

---


##  Installation

Clone the repository and set up a virtual environment:

bash
git clone https://github.com/SidratEvan/internship-assistant.git
cd internship-assistant
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

Run the Webapp
streamlit run app.py


Your browser will open at http://localhost:8501

Project Structure:
internship-assistant/
│── app.py                  # Streamlit webapp entrypoint
│── jobbot/                 # Core logic
│   ├── sources/            # ATS scrapers (Ashby, Greenhouse)
│   ├── utils.py            # Helpers (CSV tracker, config)
│   ├── filters.py          # Keyword/location scoring
│   ├── templating.py       # Cover letter generation
│── templates/              # Jinja2 templates (cover letters)
│── data/                   # Application tracker CSV
│── docs/                   # Letters, screenshots, demo files
│── config.yaml             # User config (name, email, projects, etc.)


Future Improvements

Expand to more ATS providers (Lever, Workday, etc.)

Add filtering in the UI (only internships, only remote)

Deploy online (Streamlit Cloud / HuggingFace Spaces) for anyone to use

🖥 One-click cover letter generation directly from results table

Author

Sk Sidratul Islam Priyo
📧 lcz982@usask.ca
⭐ If you find this useful, give the repo a star!



