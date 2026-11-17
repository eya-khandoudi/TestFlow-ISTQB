import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

SCREENSHOTS_DIR = r"c:\Users\Eya Khandoudi\Downloads\istqb\ISTQB\docs\screenshots"
ARTIFACT_DIR = r"C:\Users\Eya Khandoudi\.gemini\antigravity\brain\86fc9c4c-e6f5-410e-86a3-c9ce2182b962"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def get_driver():
    try:
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1440,900")
        driver = webdriver.Chrome(options=options)
        print("Using Chrome WebDriver")
        return driver
    except Exception as e:
        print(f"Chrome failed: {e}. Trying Edge...")
        edge_opts = EdgeOptions()
        edge_opts.add_argument("--headless=new")
        edge_opts.add_argument("--no-sandbox")
        edge_opts.add_argument("--disable-dev-shm-usage")
        edge_opts.add_argument("--disable-gpu")
        edge_opts.add_argument("--window-size=1440,900")
        driver = webdriver.Edge(options=edge_opts)
        print("Using Edge WebDriver")
        return driver

pages = [
    ("01_dashboard.png", "http://127.0.0.1:5000/"),
    ("02_requirements.png", "http://127.0.0.1:5000/requirements/"),
    ("03_test_cases.png", "http://127.0.0.1:5000/test-cases/"),
    ("04_test_case_detail.png", "http://127.0.0.1:5000/test-cases/4"),
    ("05_test_runs.png", "http://127.0.0.1:5000/test-runs/"),
    ("06_test_run_execution.png", "http://127.0.0.1:5000/test-runs/1"),
    ("07_defects_list.png", "http://127.0.0.1:5000/defects/"),
    ("08_defect_detail.png", "http://127.0.0.1:5000/defects/1"),
    ("09_rtm.png", "http://127.0.0.1:5000/rtm"),
    ("10_ieee829_report.png", "http://127.0.0.1:5000/report/1"),
    ("11_istqb_guide.png", "http://127.0.0.1:5000/istqb-guide"),
    ("12_new_test_case_form.png", "http://127.0.0.1:5000/test-cases/new"),
    ("13_log_defect_form.png", "http://127.0.0.1:5000/defects/new")
]

driver = get_driver()
driver.set_window_size(1440, 960)

for filename, url in pages:
    print(f"Capturing {url} -> {filename}")
    driver.get(url)
    time.sleep(1.2)  # Allow Chart.js and CSS rendering
    
    # Save to docs/screenshots
    doc_path = os.path.join(SCREENSHOTS_DIR, filename)
    driver.save_screenshot(doc_path)
    
    # Also save to artifact directory for markdown embedding
    art_path = os.path.join(ARTIFACT_DIR, filename)
    driver.save_screenshot(art_path)
    print(f"Saved: {doc_path} and {art_path}")

driver.quit()
print("All screenshots captured successfully!")
