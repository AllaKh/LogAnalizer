# Log Analyzer

A Python-based utility to open and analyze JSON log files, generate a summary of the results, and send the output via email.

---

## 🚀 Features

- 📂 Opens and parses JSON log files
- 🔍 Analyzes log data for key metrics and issues
- 📧 Sends the analysis results to a specified email address
- 📝 Customizable log structure and analysis rules

---

## 🧰 Requirements

- Python 3.7+
- `smtplib`, `email` (built-in)
- `json` (built-in)
- Optional: `dotenv` for managing email credentials securely

Install additional packages with:

```bash
pip install -r requirements.txt

---

## 🛠️ Usage

```bash
python log_analyzer.py /path/to/logfile.json
