import os
import requests
import json
from dotenv import load_dotenv
import csv
import time
from datetime import datetime, timedelta
import re
from dateutil.relativedelta import relativedelta 

load_dotenv()

# Get API Key & URL from .env
search_api_key = os.getenv("SEARCH_API_KEY")
search_url = os.getenv("SEARCH_URL")

if not search_api_key or not search_url:
    raise ValueError("❌ Missing SEARCH_API_KEY or SEARCH_URL in .env file")

csv_filename = "clt-jobs.csv"
fieldnames = ["Title", "Company", "Location", "Posted Date", "Job Link", "Job Highlights"]

categories = [
    # STEM related
    "science jobs",
    "technology jobs",
    "engineering jobs",
    "mathematics jobs",
    "STEM jobs",
    "biologist jobs",
    "chemist jobs",
    "physicist jobs",
    "software engineer jobs",
    "data scientist jobs",
    "mechanical engineer jobs",
    "electrical engineer jobs",
    "civil engineer jobs",
    "mathematician jobs",
    "statistician jobs",
    "actuary jobs",
    "artificial intelligence jobs",
    "machine learning jobs",
    "robotics jobs",
    "environmental scientist jobs"

    # Business & Finance
    "accounting jobs",
    "finance jobs",
    "auditor jobs",
    "bookkeeping jobs",
    "investment analyst jobs",
    "banking jobs",
    "tax accountant jobs",
    "loan officer jobs",
    
    # Sales & Marketing
    "sales representative jobs",
    "marketing jobs",
    "digital marketing jobs",
    "advertising jobs",
    "public relations jobs",
    "copywriter jobs",
    "social media manager jobs",
    "brand manager jobs",
    
    # Healthcare & Medical
    "registered nurse jobs",
    "doctor jobs",
    "pharmacist jobs",
    "physical therapist jobs",
    "occupational therapist jobs",
    "dentist jobs",
    "radiologic technologist jobs",
    "medical assistant jobs",
    "home health aide jobs",
    "speech-language pathologist jobs",
    "mental health counselor jobs",
    
    # Education & Training
    "teacher jobs",
    "professor jobs",
    "tutor jobs",
    "school counselor jobs",
    "special education teacher jobs",
    "curriculum developer jobs",
    "instructional designer jobs",
    
    # Customer Service & Support
    "customer service representative jobs",
    "call center jobs",
    "technical support jobs",
    "help desk jobs",
    "client relations jobs",
    
    # Human Resources & Administration
    "human resources jobs",
    "recruiter jobs",
    "training coordinator jobs",
    "payroll specialist jobs",
    "administrative assistant jobs",
    "office manager jobs",
    "data entry jobs",
    
    # Legal & Compliance
    "lawyer jobs",
    "paralegal jobs",
    "legal assistant jobs",
    "compliance officer jobs",
    "court reporter jobs",
    
    # Hospitality & Travel
    "hotel manager jobs",
    "event planner jobs",
    "flight attendant jobs",
    "travel agent jobs",
    "concierge jobs",
    "restaurant manager jobs",
    "chef jobs",
    "bartender jobs",
    "housekeeping jobs",
    
    # Construction & Skilled Trades
    "electrician jobs",
    "plumber jobs",
    "carpenter jobs",
    "welder jobs",
    "HVAC technician jobs",
    "construction manager jobs",
    "roofing jobs",
    "mason jobs",
    
    # Transportation & Logistics
    "truck driver jobs",
    "delivery driver jobs",
    "logistics coordinator jobs",
    "warehouse manager jobs",
    "supply chain analyst jobs",
    "freight broker jobs",
    "bus driver jobs",
    
    # Arts, Media & Design
    "graphic designer jobs",
    "video editor jobs",
    "photographer jobs",
    "interior designer jobs",
    "fashion designer jobs",
    "actor jobs",
    "musician jobs",
    "film director jobs",
    
    # Retail & Consumer Services
    "cashier jobs",
    "store manager jobs",
    "merchandiser jobs",
    "retail associate jobs",
    "buyer jobs",
    "personal shopper jobs",
    
    # Manufacturing & Production
    "factory worker jobs",
    "quality control inspector jobs",
    "manufacturing supervisor jobs",
    "assembler jobs",
    "machinist jobs",
    
    # Government & Public Services
    "police officer jobs",
    "firefighter jobs",
    "postal worker jobs",
    "social worker jobs",
    "city planner jobs",
    "military jobs",
    
    # Agriculture & Natural Resources
    "farmer jobs",
    "agronomist jobs",
    "fisherman jobs",
    "forester jobs",
    "landscaper jobs",
    
    # Energy & Utilities
    "solar panel installer jobs",
    "wind turbine technician jobs",
    "oil rig worker jobs",
    "power plant operator jobs",
    "water treatment specialist jobs"
]

six_months_ago = (datetime.today() - timedelta(days=180)).strftime("%m/%d/%Y")
today_str = datetime.today().strftime("%m/%d/%Y")

BASE_PARAMS = {
    "engine": "google_jobs",
    "q": "Electrical",  # Overridden in fetch_jobs
    "location": "Charlotte, North Carolina, United States",
    "tbs": f"cdr:1,cd_min:{six_months_ago},cd_max:{today_str}",
    "api_key": search_api_key,
    "num": 50,  # Jobs per request
}

def convert_posted_at_to_date(posted_at_str):
    """Convert relative posted_at string to a formatted date."""
    today = datetime.today()

    day_match = re.match(r"(\d+) day[s]? ago", posted_at_str)
    week_match = re.match(r"(\d+) week[s]? ago", posted_at_str)
    month_match = re.match(r"(\d+) month[s]? ago", posted_at_str)
    year_match = re.match(r"(\d+) year[s]? ago", posted_at_str)

    if day_match:
        days = int(day_match.group(1))
        result_date = today - timedelta(days=days)
    elif week_match:
        weeks = int(week_match.group(1))
        result_date = today - timedelta(weeks=weeks)
    elif month_match:
        months = int(month_match.group(1))
        result_date = today - relativedelta(months=months)
    elif year_match:
        years = int(year_match.group(1))
        result_date = today - relativedelta(years=years)
    else:
        return "N/A"

    return result_date.strftime("%m/%d/%Y")

def fetch_jobs(job_category):
    """Fetch job listings for a given category."""
    all_jobs = []
    params = BASE_PARAMS.copy()
    params["q"] = job_category

    next_page_token = None
    pages_read = 0

    while True:
        if next_page_token:
            params["next_page_token"] = next_page_token
        else:
            params.pop("next_page_token", None)

        try:
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            print(f"🔍 API Response: {response.text}")
            break

        jobs_data = response.json()
        jobs = jobs_data.get("jobs", [])

        if not jobs:
            print("✅ No more jobs found, stopping pagination.")
            break

        all_jobs.extend(jobs)
        print(f"✅ Retrieved {len(jobs)} jobs")

        next_page_token = jobs_data.get("pagination", {}).get("next_page_token")

        if not next_page_token:
            print(f"✅ No more pages available\nRead from {pages_read} pages\nStopping pagination.")
            break

        pages_read += 1
        time.sleep(2)

    return all_jobs

def save_jobs_to_csv(jobs):
    """Append job listings to the CSV file."""
    with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for job in jobs:
            posted_at_raw = job.get("detected_extensions", {}).get("posted_at", "N/A")
            formatted_date = convert_posted_at_to_date(posted_at_raw)

            writer.writerow({
                "Title": job.get("title"),
                "Company": job.get("company_name"),
                "Location": job.get("location"),
                "Posted Date": formatted_date,
                "Job Link": job.get("apply_link", "N/A"),
                "Job Highlights": job.get("job_highlights", "N/A")
            })
    print(f"📁 Appended {len(jobs)} jobs to {csv_filename}\n\u200B\n")

def main():
    """Main function to execute job scraping and saving."""
    print(f"🌐 Using API URL: {search_url}")

    # Initialize CSV with headers if it doesn't exist
    if not os.path.exists(csv_filename):
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
        print(f"📄 Created {csv_filename} with headers")

    for job_category in categories:
        print(f"Searching for jobs under category: {job_category}")
        jobs = fetch_jobs(job_category)
        if jobs:
            save_jobs_to_csv(jobs)
        else:
            print("⚠️ No jobs found for category:", job_category)

if __name__ == "__main__":
    main()