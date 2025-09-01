# text_extractor.py — REST-only Wikipedia extractor with Jina fallback
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

OUTPUT_FILE = "Selected_Document.txt"
TITLE = "Anime"
REST_PLAIN = f"https://en.wikipedia.org/api/rest_v1/page/plain/{TITLE}?redirect=true"
REST_SUMMARY = f"https://en.wikipedia.org/api/rest_v1/page/summary/{TITLE}?redirect=true"
JINA_READER = f"https://r.jina.ai/http://en.wikipedia.org/wiki/{TITLE}"

def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (RAG-StudentBot/1.0)",
        "Accept": "text/plain; charset=utf-8",
    })
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(403, 429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
        raise_on_redirect=False,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    return s

def write_output(text: str) -> None:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)

def fetch(url: str, session: requests.Session, label: str) -> str:
    try:
        r = session.get(url, timeout=20)
        if r.status_code == 200:
            txt = (r.text or "").strip()
            if txt:
                write_output(txt)
                print(f"✅ {label} succeeded → saved to {OUTPUT_FILE}")
                return txt
            print(f"⚠️ {label} returned empty content")
        else:
            print(f"❌ {label} failed: HTTP {r.status_code}")
    except requests.RequestException as e:
        print(f"❌ {label} error: {e}")
    return ""

def main():
    print("Running extractor from:", os.path.abspath(__file__))
    s = make_session()

    # 1) REST plaintext
    if fetch(REST_PLAIN, s, "REST plaintext"):
        return

    # 2) REST summary (JSON -> extract field)
    try:
        r = s.get(REST_SUMMARY, timeout=20, headers={"Accept": "application/json"})
        if r.status_code == 200:
            data = r.json()
            txt = (data.get("extract") or data.get("description") or "").strip()
            if txt:
                write_output(txt)
                print(f"✅ REST summary succeeded → saved to {OUTPUT_FILE}")
                return
        else:
            print(f"❌ REST summary failed: HTTP {r.status_code}")
    except Exception as e:
        print(f"❌ REST summary error: {e}")

    # 3) Jina text reader fallback
    if fetch(JINA_READER, s, "Jina text reader"):
        return

    write_output("")
    print("❌ All methods failed → wrote empty file.")

if __name__ == "__main__":
    main()
