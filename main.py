import os
import uuid
import shutil
import tempfile
import re
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import feedparser
import pandas as pd
import subprocess

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SODA_CHECKS_YML = os.path.join("soda_checks", "checks.yml")

def parse_soda_output(output):
    """Parse Soda Core output to extract check statuses"""
    checks = []
    lines = output.split('\n')
    
    for line in lines:
        # Look for check results
        if '✓' in line or '✗' in line:
            # Extract check name and status
            if '✓' in line:
                status = 'passed'
                check_name = line.split('✓')[0].strip()
            else:
                status = 'failed'
                check_name = line.split('✗')[0].strip()
            
            checks.append({
                'name': check_name,
                'status': status
            })
    
    # If no specific checks found, look for summary
    if not checks:
        if 'All checks passed' in output:
            checks.append({'name': 'All checks', 'status': 'passed'})
        elif 'Some checks failed' in output or 'FAILED' in output:
            checks.append({'name': 'Some checks', 'status': 'failed'})
    
    return checks

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/validate", response_class=HTMLResponse)
def validate(request: Request, feed_url: str = Form(...)):
    # Parse RSS feed
    feed = feedparser.parse(feed_url)
    entries = feed.entries
    if not entries:
        return templates.TemplateResponse("results.html", {
            "request": request,
            "entries": [],
            "log": "No entries found or invalid feed URL.",
            "checks": []
        })
    # Normalize to DataFrame
    df = pd.DataFrame([
        {
            "title": e.get("title", ""),
            "summary": e.get("summary", ""),
            "published": e.get("published", ""),
            "link": e.get("link", ""),
        }
        for e in entries
    ])

    print(df[['summary']].head(3))
    # Run Soda Core in-process
    try:
        from soda.scan import Scan
        scan = Scan()
        scan.set_scan_definition_name("rss_feed_scan")
        scan.set_data_source_name("pandas")
        scan.add_pandas_dataframe(dataset_name="feed", pandas_df=df.head(3), data_source_name="pandas")
        scan.add_sodacl_yaml_file(SODA_CHECKS_YML)
        scan.execute()
        log = scan.get_logs_text()
        checks = parse_soda_output(log)
    except Exception as e:
        log = f"Error running Soda Core: {e}"
        checks = []
    # Render results
    return templates.TemplateResponse("results.html", {
        "request": request,
        "entries": df.to_dict(orient="records")[:3],  # Only show last 3 entries
        "log": log,
        "checks": checks
    })