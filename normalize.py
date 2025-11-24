import re
from bs4 import BeautifulSoup

JUNK_TAGS = ["script", "style", "noscript", "svg", "path", "canvas", "head", "meta", "link"]
PADDING_WORDS = [
	"the", "and", "is", "in", "to", "of", "a", "that", "it", "on", "for", "as", "with",
	"this", "by", "an", "be", "are", "at", "from", "or", "but", "not", "have", "has",
	"was", "were", "they", "you", "he", "she", "we", "all", "their", "my", "your",
]

def extract_clean_text(html: BeautifulSoup | str) -> str:
	if isinstance(html, str):
		soup = BeautifulSoup(html, 'html.parser')
	else:
		soup = html

	# Remove script, style, and junk tags
	for tag in soup(JUNK_TAGS):
		tag.extract()

	return soup.get_text(separator=" ", strip=True)

def tokenize_text(text: str) -> list[str]:
	# Split into each word removing spaces, newlines, tabs, and punctuation
	words = re.split(r'\W+', text)
	words = [word.lower() for word in words if word]
	return words

def normalize_webpage(html: BeautifulSoup | str) -> list[str]:
	if isinstance(html, str):
		soup = BeautifulSoup(html, 'html.parser')
	else:
		soup = html

	clean_text = extract_clean_text(soup)
	# Split into each word removing spaces, newlines, tabs, and punctuation
	words = tokenize_text(clean_text)
	words = [word for word in words if word not in PADDING_WORDS]
	words = list(set(words))  # Unique words only
	# print(words)
	return words