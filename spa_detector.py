# A lot of websites on the internet are Single Page Applications (SPA) built with frameworks like React, Angular, or Vue.js.
# These SPAs dynamically load content using JavaScript, which can pose challenges for web scrapers that rely on static HTML parsing.
# This module provides functionality to detect if a webpage is an SPA by analyzing its HTML structure and JavaScript usage.
# In my opinion we should've just stuck with PHP and server side rendering but oh well...
# It's not like you're actually fetching more content initially. If you want SPA performance you can make it server side rendered SPA.
# This should save us a lot of cpu cycles and bandwidth by avoiding unnecessary JS rendering for non-SPA pages.

from bs4 import BeautifulSoup

def detect_spa(html: BeautifulSoup | str) -> bool:
	if isinstance(html, str):
		soup = BeautifulSoup(html, 'html.parser')
	else:
		soup = html
	# Check for common SPA indicators
	# 1. Presence of specific div IDs or classes used by popular frameworks
	spa_roots = ['root', 'app', '__next', 'mount']
	for root_id in spa_roots:
		if soup.find(id=root_id) and len(soup.get_text()) < 500:
			return True
	
	# Check for suspiciously low amount of text content
	for script in soup.find_all('script'):
		# Remove script tags to avoid counting JS code as text
		script.extract()

	text_content = soup.get_text(strip=True)
	if len(text_content) < 300:
		return True
	
	# Check for noscript tags indicating JS reliance
	noscript = soup.find('noscript')
	if noscript and "javascript" in noscript.get_text().lower():
		return True
		
	return False