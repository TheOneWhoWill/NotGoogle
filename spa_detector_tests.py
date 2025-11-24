import httpx
import spa_detector

async def test_detect_spa(url: str, expected: bool):
	# Add a user agent to avoid being blocked by some sites (like NYTimes)
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
	}
	# Increase timeout to 30 seconds and handle exceptions
	async with httpx.AsyncClient(headers=headers, timeout=1.0) as client:
		try:
			# Fetch the html content
			response = await client.get(url, follow_redirects=True)
			result = spa_detector.detect_spa(response.text)
			return result == expected
		except httpx.RequestError as exc:
			print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
			return False

async def run_tests():
	# Test cases for SPA detection
	# These websites are known as SPAs or not SPAs as of 11/24/2025
	test_cases = [
		# Known SPAs (Should be True)
		("https://crunchyroll.com/", True),
		("https://open.spotify.com/", True),
		("https://trello.com/", True),
		("https://react.dev/", True),
		("https://www.youtube.com/", True), # Heavy SPA
		("https://open.spotify.com/", True), # Classic heavy SPA
        ("https://discord.com/app", True), # The actual app, not the marketing site
        ("https://www.figma.com/", True), # Canvas-based application
        ("https://web.whatsapp.com/", True), # Heavy client-side logic
        ("https://linear.app/login", True), # Modern "app-feel" login

		# Text-Heavy Static Sites (Easy)
		("https://www.wikipedia.org/", False),
		("https://www.nytimes.com/", False),
		("https://news.ycombinator.com/", False), # HackerNews: Tiny text, but pure HTML tables
		("https://www.gnu.org/", False), # Pure static HTML
		("https://www.linux.org/", False), # Static HTML
		("https://www.kernel.org/", False), # Linux kernel source, very static
		("https://docs.python.org/3/", False), # Documentation, static
		("https://craigslist.org/", False), # Ancient HTML structure
        ("https://www.w3.org/TR/html5/", False), # Massive technical spec (pure text)
        ("https://gutenberg.org/", False), # Project Gutenberg (pure HTML archives)
        ("https://lite.cnn.com/en", False), # CNN Lite (specifically designed for low data)
        ("https://motherfuckingwebsite.com/", False), # Famous satire site (purest HTML)

		# These have < 300 chars of text but contain <form> or <input>, so they are STATIC.
		("https://github.com/login", False),
		("https://stackoverflow.com/users/login", False),
		("https://duckduckgo.com/lite", False), # The non-JS version of DDG
        ("https://old.reddit.com/login", False), # The old reddit login form
        ("https://m.facebook.com/", False), # The mobile basic site (often form heavy, low script)

		# SSR Framework Sites. These have id="__next" or id="root" but contain FULL content. 
		# We do NOT want to waste resources rendering them.
		("https://vercel.com/", False), 
		("https://nextjs.org/", False),
		("https://www.airbnb.com/", False), # React-heavy but SSR'd for SEO
		("https://remix.run/", False), # Heavily promotes SSR/Hydration
        ("https://medium.com/", False), # React based, but content is server rendered for SEO
        ("https://dev.to/", False), # Preact/Rails, delivers HTML first
        ("https://www.notion.so/product", False), # Marketing page is SSR, unlike the app
        ("https://astro.build/", False), # Astro sites ship zero JS by default usually
		
		# Edge Cases
		("https://example.com/", False), # extremely simple HTML
		("http://info.cern.ch/hypertext/WWW/TheProject.html", False), # The first website ever (pure HTML)
		("https://httpbin.org/html", False), # Simple API response returning HTML
        ("https://raw.githubusercontent.com/TheOneWhoWill/NotGoogle/refs/heads/main/README.md", False), # Raw text/markdown (no HTML tags should not trigger SPA)
	]

	passed_tests = 0
	num_tests = len(test_cases)

	for url, expected in test_cases:
		test_passed = await test_detect_spa(url, expected)
		if test_passed:
			print(f"Test passed for URL: {url}")
			passed_tests += 1
		else:
			print(f"Test failed for URL: {url}")

	if passed_tests == num_tests:
		print(f"{passed_tests}/{num_tests} tests passed successfully.")
	else:
		print(f"{passed_tests}/{num_tests} tests passed. Some tests failed.")

if __name__ == "__main__":
	import asyncio
	asyncio.run(run_tests())