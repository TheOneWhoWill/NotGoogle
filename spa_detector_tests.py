import httpx
import spa_detector

async def test_detect_spa(url: str, expected: bool):
	async with httpx.AsyncClient() as client:
		# Fetch the html content
		response = await client.get(url, follow_redirects=True)
		result = spa_detector.detect_spa(response.text)
		assert result == expected, f"Expected {expected} for URL {url}, but got {result}"

async def run_tests():
	# Test cases for SPA detection
	test_cases = [
		("https://reactjs.org/", False),
		("https://www.nytimes.com/", False),
		("https://www.bbc.com/", False),
		("https://crunchyroll.com/", True),
	]

	all_passed = True
	for url, expected in test_cases:
		test_passed = await test_detect_spa(url, expected)
		if not test_passed:
			all_passed = False
			print(f"Test failed for URL: {url}")
	if not all_passed:
		print("Some SPA detection tests failed.")
	else:
		print("All SPA detection tests passed.")

if __name__ == "__main__":
	import asyncio
	asyncio.run(run_tests())