import asyncio
from normalize import normalize_webpage
from scraper import scrape_with_httpx

async def test_normalized_website(url: str, words: set[str]):
	response = await scrape_with_httpx(url)
	result = normalize_webpage(response.full_text)
	words.update(result)
	print(f"Normalized {url}: {len(result)} words")

async def run_tests():
	# Test cases for normalization
	test_urls = [
		"https://www.wikipedia.org/",
		"https://www.nytimes.com/",
		"https://news.ycombinator.com/",
		"https://www.gnu.org/",
		"https://www.linux.org/",
		"https://www.kernel.org/",
		"https://docs.python.org/3/",
		"https://craigslist.org/",
		"https://www.w3.org/TR/html5/",
		"https://gutenberg.org/",
		"https://lite.cnn.com/en",
		"https://motherfuckingwebsite.com/",
		"https://berkshirehathaway.com/",
		"https://stallman.org/",
		"https://developer.mozilla.org/en-US/",
		"https://doc.rust-lang.org/book/",
		"https://arxiv.org/",
		"https://www.snopes.com/",
	]
	words: set[str] = set()
	for url in test_urls:
		await test_normalized_website(url, words)
	print(f"Total unique words across all sites: {len(words)}")
	
if __name__ == "__main__":
	asyncio.run(run_tests())