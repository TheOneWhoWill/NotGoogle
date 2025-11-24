import httpx
import asyncio
from normalize import normalize_webpage

async def test_normalized_website(url: str):
	# Add a user agent to avoid being blocked by some sites (like NYTimes)
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
	}
	# Increase timeout to 30 seconds and handle exceptions
	async with httpx.AsyncClient(headers=headers, timeout=1.0) as client:
		try:
			# Fetch the html content
			response = await client.get(url, follow_redirects=True)
			result = normalize_webpage(response.text)
			print(f"Normalized {url}: {len(result)} words")

		except httpx.RequestError as exc:
			print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
			return False

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
	for url in test_urls:
		await test_normalized_website(url)
	
if __name__ == "__main__":
	asyncio.run(run_tests())