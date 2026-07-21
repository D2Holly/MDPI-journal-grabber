# MDPI-journal-grabber
This script connects to the Crossref REST API to grab all volumes from an open source MDPI journal. The default for this script is to search the Remote Sensing journal [https://www.mdpi.com/journal/remotesensing], find the most recent 30 issues from the most recent volumes, and parse metadata (title, URL, volume, and issue).


## Features
- **REST API Integration**: Sends filtered, sorted queries to Crossref's API with customizable payload parameters.
- **Robust Parsing**: Safely traverses nested JSON structures (resource $\rightarrow$ primary $\rightarrow$ URL) with defensive default fallbacks.
- **Rate-Limit Safe**: Implements execution delays (time.sleep) between printed outputs to respect downstream consumers and terminal rate limits.
- **Polite API Requests**: Incorporates custom User-Agent headers in compliance with Crossref API best practices.

---
## Requirements
**Python**: 3.9+

**Dependencies**: requests, pytest (for testing)

## Setup & Installation
1. Clone the repo via terminal 
```
git clone https://github.com/D2Holly/ArXiv-Research-Project.git
cd crossref-article-fetcher
```
2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  
# On Windows use: venv\Scripts\activate
```
3. Install requirements
```
pip install -r requirements.txt
```
4. Edit the headers dictionary in app.py main() to include your own contact email inside the User-Agent string as requested by Crossref guidelines:
```
headers = {
    "User-Agent": "MyDataScienceProject/1.0 (mailto:your-email@example.com)"
}
```

---   
## Usage
Run the script directly in your terminal:
```
python3 app/app.py
```

### Sample Output
```
Title: Machine Learning Applications in Remote Sensing
URL: https://doi.org/10.3390/rs12010001
Volume: 12
Issue: 1

Title: Deep Learning for Satellite Image Classification
URL: https://doi.org/10.3390/rs12010002
Volume: 12
Issue: 1
```

---
## Running Tests
The tests in tests/test_ap.py use pytest along with monkeypatch to mock the Crossref REST API requests.

Execute tests in the terminal with:
```
pytest tests/test_app.py
```

---   
## Future Implementations
Functionality with the Google NotebookLM Enterprise API
- Create a new notebook and add all of the URLs of the found issues as sources
- Return URL of new notebook

---
