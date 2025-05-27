from mitmproxy import ctx
import re
from urllib.parse import urlparse
import os

class URLFilter:
    def __init__(self):
        self.ignored_domains = {'google.com', 'facebook.com',  'gstatic.com', 'youtube.com'}
        self.saved_urls = set()
        self.output_file = 'sites.txt'
        
        # Create or load existing URLs
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                self.saved_urls = set(line.strip() for line in f)

    def request(self, flow):
        pass

    def response(self, flow):
        if not flow.response or not flow.response.content:
            return

        # Get the response content as text
        content = flow.response.text
        
        # Find all URLs in href attributes
        urls = re.findall(r'href="(https://[^"]+)"', content)
        
        for url in urls:
            # Parse the URL to get the domain
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Skip if domain is in ignored list
            if any(ignored in domain for ignored in self.ignored_domains):
                continue
                
            # Add to set if not already saved
            if url not in self.saved_urls:
                self.saved_urls.add(url)
                # Save to file
                with open(self.output_file, 'a', encoding='utf-8') as f:
                    f.write(f"{url}\n")
                ctx.log.info(f"New URL saved: {url}")

addons = [
    URLFilter()
] 