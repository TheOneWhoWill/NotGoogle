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

	# Remove script and style tags
	for script in soup(["script", "style", "noscript"]):
		# Remove script tags to avoid counting JS code as text
		script.extract()

	# Check for common SPA indicators
	# Presence of specific div IDs or classes used by popular frameworks
	spa_roots = ['root', 'app', '__next', 'mount']
	for root_id in spa_roots:
		root_element = soup.find(id=root_id)
		if root_element:
			root_text = root_element.get_text(strip=True)
			# If the root element has very little text, it's likely an SPA
			has_interactive = root_element.find(['form', 'input', 'button', 'select'])
			if len(root_text) < 50 and not has_interactive:
				return True


	text_content = soup.get_text(strip=True)
	if len(text_content) < 300:
		has_inputs = soup.find(['input', 'button', 'select', 'textarea'])

		if not has_inputs:
			return True
		
	return False