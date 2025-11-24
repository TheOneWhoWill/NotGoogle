import httpx
import spa_detector

async def test_detect_spa(url: str, expected: bool):
	async with httpx.AsyncClient() as client:
		# Fetch the html content
		response = await client.get(url, follow_redirects=True)
		result = spa_detector.detect_spa(response.text)
		return result == expected

async def run_tests():
	# Test cases for SPA detection
	test_cases = [
		("https://crunchyroll.com/", True),
		# Complex Static/SSR Sites (Should be False)
		("https://reactjs.org/", False),
		("https://www.nytimes.com/", False),
		("https://github.com/login", False), # Login page is not SPA
		("https://www.bbc.com/", False),
	]

	for url, expected in test_cases:
		test_passed = await test_detect_spa(url, expected)
		if test_passed:
			print(f"Test passed for URL: {url}")
		else:
			print(f"Test failed for URL: {url}")

if __name__ == "__main__":
	import asyncio
	asyncio.run(run_tests())