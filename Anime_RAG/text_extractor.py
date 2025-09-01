# text_extractor.py — original-style scraper that works for
# https://en.wikipedia.org/wiki/Anime (with UA + REST fallback)

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup


def make_session() -> requests.Session:
    """
    Create a requests Session with retries and a real User-Agent.
    Wikipedia often 403-blocks the default Python UA.
    """
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
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
    with open("Selected_Document.txt", "w", encoding="utf-8") as f:
        f.write(text)


def fetch_and_extract(url: str) -> str:
    """
    Fetch the page at `url`, parse with BeautifulSoup, extract all <p> tags
    within <div class='mw-parser-output'>, join with blank lines, write to
    Selected_Document.txt (UTF-8), print a success/failure message, and
    return the extracted text.

    If the HTML fetch is blocked (e.g., 403) or yields no paragraphs,
    fall back to the Wikipedia REST plaintext endpoint for the same title.
    """
    session = make_session()

    # ---- Try HTML route (original behavior) ----
    try:
        r = session.get(url, timeout=20)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            container = soup.find("div", class_="mw-parser-output")
            if container:
                paras = container.find_all("p")
                extracted = "\n\n".join(
                    p.get_text(strip=True) for p in paras if p.get_text(strip=True)
                ).strip()
                if extracted:
                    write_output(extracted)
                    print("Success: HTML retrieved and written to Selected_Document.txt")
                    return extracted
                else:
                    print("HTML retrieved but no paragraphs extracted; using REST fallback...")
            else:
                print("Could not find article content container; using REST fallback...")
        else:
            print(f"Failed to retrieve the page. HTTP Status Code: {r.status_code}. Using REST fallback...")
    except requests.RequestException as e:
        print(f"HTML fetch error: {e}. Using REST fallback...")

    # ---- REST plaintext fallback (keeps file-writing contract) ----
    try:
        # Convert /wiki/Title -> Title for REST
        if "/wiki/" in url:
            title = url.split("/wiki/", 1)[1]
        else:
            title = url.rstrip("/").rsplit("/", 1)[-1]

        rest_url = f"https://en.wikipedia.org/api/rest_v1/page/plain/{title}?redirect=true"
        r2 = session.get(
            rest_url,
            timeout=20,
            headers={"Accept": "text/plain; charset=utf-8"},
        )
        if r2.status_code == 200:
            text = r2.text.strip()
            write_output(text)
            print("Success: REST plaintext fallback wrote Selected_Document.txt")
            return text
        else:
            print(f"REST fallback failed. HTTP Status Code: {r2.status_code}")
    except requests.RequestException as e:
        print(f"REST fallback error: {e}")

    # If both methods fail, write an empty file (original contract) and report
    write_output("")
    print("Failed: no content written (HTML blocked and REST failed).")
    return ""


def main():
    # Hardcoded URL (your requested change)
    url = "https://en.wikipedia.org/wiki/Anime"
    fetch_and_extract(url)


if __name__ == "__main__":
    main()