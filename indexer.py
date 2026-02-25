# FILE: indexer.py
# ROLE: Commercial version with Daily Limit enforcement for Google Indexing API.

import os
import json
import requests
from oauth2client.service_account import ServiceAccountCredentials

def log(message):
    print(f"[SYSTEM LOG] {message}")

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

def get_credentials():
    json_creds = os.getenv('GOOGLE_INDEXING_JSON')
    if not json_creds:
        log("⚠️ CRITICAL: GOOGLE_INDEXING_JSON is missing in Secrets.")
        return None
    
    try:
        info = json.loads(json_creds)
        return ServiceAccountCredentials.from_json_keyfile_dict(info, SCOPES)
    except Exception as e:
        log(f"❌ AUTH ERROR: {e}")
        return None

def submit_url(url, access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        content = {"url": url, "type": "URL_UPDATED"}
        
        r = requests.post(ENDPOINT, data=json.dumps(content), headers=headers)
        
        if r.status_code == 200:
            log(f"✅ SUCCESS: {url}")
            return True
        else:
            log(f"⚠️ API REFUSED {url}: {r.text}")
            return False
            
    except Exception as e:
        log(f"❌ ERROR processing {url}: {e}")
        return False

def main():
    # 1. تحديد الحد اليومي للباقة (يُجلب من Secrets أو يكون 20 افتراضياً)
    DAILY_LIMIT = int(os.getenv('DAILY_LIMIT', 20)) 
    urls_file = "urls.txt"
    
    if not os.path.exists(urls_file):
        log("❌ Error: urls.txt not found.")
        return

    # 2. قراءة الروابط من الملف
    with open(urls_file, "r") as f:
        all_urls = [line.strip() for line in f if line.strip().startswith("http")]

    if not all_urls:
        log("⚠️ No URLs to process.")
        return

    # 3. تطبيق نظام حدود الباقة
    total_found = len(all_urls)
    urls_to_process = all_urls[:DAILY_LIMIT] # أخذ الروابط ضمن الحد المسموح فقط
    skipped_count = total_found - len(urls_to_process)

    log(f"📊 Package Limit: {DAILY_LIMIT} URLs per run.")
    log(f"📂 Found in file: {total_found} URLs.")
    
    if skipped_count > 0:
        log(f"🚫 Plan Restriction: {skipped_count} URLs were skipped. Please upgrade your plan.")

    # 4. الحصول على صلاحيات الوصول لمرة واحدة
    creds = get_credentials()
    if not creds: return
    
    try:
        access_token = creds.get_access_token().access_token
    except Exception as e:
        log(f"❌ Failed to get access token: {e}")
        return

    # 5. البدء في الإرسال
    success_count = 0
    for url in urls_to_process:
        if submit_url(url, access_token):
            success_count += 1
        
    log("-" * 30)
    log(f"🏁 Final Report: {success_count} Success | {len(urls_to_process) - success_count} Failed")
    log(f"🚀 Powered by LatestAI Indexer Pro")

if __name__ == "__main__":
    main()
