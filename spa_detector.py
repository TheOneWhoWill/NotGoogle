# A lot of websites on the internet are Single Page Applications (SPA) built with frameworks like React, Angular, or Vue.js.
# These SPAs dynamically load content using JavaScript, which can pose challenges for web scrapers that rely on static HTML parsing.
# This module provides functionality to detect if a webpage is an SPA by analyzing its HTML structure and JavaScript usage.
# In my opinion we should've just stuck with PHP and server side rendering but oh well...
# It's not like you're actually fetching more content initially. If you want SPA performance you can make it server side rendered SPA.
# This should save us a lot of cpu cycles and bandwidth by avoiding unnecessary JS rendering for non-SPA pages.
# Note: This isn't perfect and may yield false positives/negatives, but it should work well enough to filter out most SPAs and save resources.

from bs4 import BeautifulSoup, Tag
import re

from normalize import extract_clean_text

# Constants for SPA detection thresholds
MIN_TEXT_LENGTH_SPA = 1200
MIN_PURE_TEXT_NON_SPA = 300
FRAMEWORK_SIGNATURES = [
	r'react', r'vue', r'angular', r'next', r'nuxt', r'gatsby', 
	r'bundle\.js', r'main\.[a-z0-9]+\.js', r'chunk', r'vendor',
	r'polymer', r'yt-player', r'ember', r'svelte'
]
SPA_ROOTS = ['root', 'app', '__next', 'mount', 'trello-root', 'react-root', 'main-app']

def detect_spa(html: BeautifulSoup | str) -> bool:
	if isinstance(html, str):
		# Quick check for non-HTML content to avoid parser warnings and overhead
		if html.lstrip().startswith(('<?xml', '{', '[')):
			return False

		soup = BeautifulSoup(html, 'html.parser')
	else:
		soup = html

	# Check if the soup is html
	if not soup.find('html') or not soup.find('body'):
		return False

	# If there is no JS then it's definitely not an SPA
	script_tags = soup.find_all('script')
	if not script_tags:
		return False
	
	# Check for noscript tag indicating JS is required
	has_blocking_noscript = False
	noscript = soup.find('noscript')
	if noscript:
		noscript_text = noscript.get_text(strip=True).lower()
		if 'enable javascript' in noscript_text or 'javascript is required' in noscript_text:
			has_blocking_noscript = True
	
	has_framework_js = False
	for script in script_tags:
		src = script.get('src', '')
		if src and any(re.search(sig, src, re.IGNORECASE) for sig in FRAMEWORK_SIGNATURES):
			has_framework_js = True
			break

	# Aggressive check: If framework JS or blocking noscript is found, assume SPA.
	# This favors false positives (rendering static sites) over false negatives (missing SPA content).
	if has_framework_js or has_blocking_noscript:
		return True

	# Check for common SPA indicators
	# Presence of specific div IDs or classes used by popular frameworks
	for root_id in SPA_ROOTS:
		root_element: Tag | None = soup.find(id=root_id)
		if root_element:
			root_text = root_element.get_text(strip=True)
			if len(root_text) < MIN_TEXT_LENGTH_SPA:
				return True

	text_content = extract_clean_text(soup)

	if len(text_content) < MIN_PURE_TEXT_NON_SPA:
		return True

	return False