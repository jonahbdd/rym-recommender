import requests
from bs4 import BeautifulSoup
import sys
import json

def main(username: str):
    """Get album recommendations based on RateYourMusic ratings."""
    sys.stdout.write(f"Fetching 5-star albums for user: {username}\n")
    sys.stdout.flush()
    
    url = f"https://rateyourmusic.com/collection/{username}/r5.0"
    sys.stdout.write(f"URL: {url}\n")
    sys.stdout.flush()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }

    try:
        sys.stdout.write("Sending request to RateYourMusic...\n")
        sys.stdout.flush()
        
        response = requests.get(url, headers=headers, timeout=10)
        sys.stdout.write(f"Got response with status code: {response.status_code}\n")
        sys.stdout.write(f"Response headers:\n{json.dumps(dict(response.headers), indent=2)}\n")
        sys.stdout.flush()
        
        if response.status_code == 403:
            sys.stdout.write("\nError: Access forbidden. RateYourMusic is blocking our request.\n")
            sys.stdout.write("This is likely due to their anti-scraping measures.\n")
            sys.stdout.write("\nTo fix this, we need to:\n")
            sys.stdout.write("1. Add proper rate limiting\n")
            sys.stdout.write("2. Handle CloudFlare protection\n")
            sys.stdout.write("3. Use their official API if available\n")
            sys.stdout.write("\nResponse preview:\n")
            sys.stdout.write(response.text[:500] + "\n")
            return
            
        if response.status_code != 200:
            sys.stdout.write(f"\nError: Could not fetch the profile (Status code: {response.status_code})\n")
            sys.stdout.write("Response preview:\n")
            sys.stdout.write(response.text[:500] + "\n")
            return

        sys.stdout.write("Parsing response...\n")
        sys.stdout.flush()
        
        # Print the first part of the response for debugging
        sys.stdout.write("\nFirst part of the response:\n")
        sys.stdout.write("-" * 80 + "\n")
        sys.stdout.write(response.text[:1000] + "\n")
        sys.stdout.write("-" * 80 + "\n")
        sys.stdout.flush()

    except requests.RequestException as e:
        sys.stdout.write(f"\nNetwork error: {str(e)}\n")
        sys.stdout.write(f"Error type: {e.__class__.__name__}\n")
    except Exception as e:
        sys.stdout.write(f"\nUnexpected error: {str(e)}\n")
        sys.stdout.write(f"Error type: {e.__class__.__name__}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stdout.write("Usage: python main.py USERNAME\n")
        sys.exit(1)
    main(sys.argv[1])
