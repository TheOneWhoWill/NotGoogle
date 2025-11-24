import re
from bs4 import BeautifulSoup

JUNK_TAGS = ["script", "style", "noscript", "svg", "path", "canvas", "head", "meta", "link"]

def extract_clean_text(html: BeautifulSoup | str) -> str:
	if isinstance(html, str):
		soup = BeautifulSoup(html, 'html.parser')
	else:
		soup = html

	# Remove script, style, and junk tags
	for tag in soup(JUNK_TAGS):
		tag.extract()

	return soup.get_text(strip=True)

def normalize_webpage(html: BeautifulSoup | str) -> list[str]:
	if isinstance(html, str):
		soup = BeautifulSoup(html, 'html.parser')
	else:
		soup = html

	clean_text = extract_clean_text(soup)
	# Split into each word removing spaces, newlines, tabs, and punctuation
	words = re.findall(r'\b\w+\b', clean_text)
	words = [word.lower() for word in words if word]
	return words