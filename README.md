# FeedSanity

FeedSanity is a minimal, educational RSS reader with built-in data quality validation using Soda Core. It is backend-rendered using FastAPI, Python, and HTML (Jinja2 templates) — no JavaScript frameworks or frontend build tools. Check a live version at: [feedsanity.santiviquez.com](https://feedsanity.santiviquez.com/)


![Screen Recording 2025-07-09 at 14 29 46](https://github.com/user-attachments/assets/91d80186-3059-4a25-953f-b689bce5ad88)



## Features
- Input an RSS feed URL and view entries in a simple web interface
- Data is parsed, normalized, and validated using Soda Core with a YAML config
- Results show both feed entries and Soda Core validation log
- No database required — uses temporary CSV files

## Tech Stack
- FastAPI
- feedparser
- pandas
- Jinja2
- [Soda Core](https://github.com/sodadata/soda-core)

## Quickstart
1. Create an uv environment:
   ```
   uv venv --python 3.10
   ```
2. Activate the new environment:
   ```
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   uv pip install -r uv.lock
   ```
4. Run the app:
   ```bash
   uvicorn main:app --reload
   ```
5. Open your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Project Structure
```
feedsanity/
├── main.py
├── soda_checks/
│   └── checks.yml
├── templates/
│   ├── index.html
│   └── results.html
├── static/
│   └── style.css
├── requirements.txt
├── uv.lock
├── README.md
```

## License
MIT 
