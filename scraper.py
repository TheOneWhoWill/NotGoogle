from datetime import datetime
from urllib.parse import urljoin
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import httpx
import spa_detector

class CrawlResponse:
	url: str
	title: str = ""
	h1_text: str = ""
	h2_tags: list[str] = []
	# 1 for success, 0 for failure
	status_code: int = 1
	full_text: str = ""
	timestamp: int = 0
	meta_description: str = ""
	# A list of # tags found on the page
	anchor_tags: list[str] = []
	links: list[str] = []

	def __init__(self, url, title, timestamp, meta_description, full_text, links):
		self.url = url
		self.title = title
		self.timestamp = timestamp
		self.meta_description = meta_description
		self.full_text = full_text
		self.links = links

	def set_failure(self):
		self.status_code = 0

def generate_crawl_response(soup: BeautifulSoup, url: str) -> CrawlResponse:
	title = soup.title.string if soup.title else ''
	full_text = soup.get_text(separator='\n', strip=True)
	meta_description_tag = soup.find('meta', attrs={'name': 'description'})
	# Fallback rank: descrption -> og:description -> content snippet -> empty
	if meta_description_tag:
		meta_description = meta_description_tag['content']
	elif soup.find('meta', attrs={'property': 'og:description'}):
		meta_description = soup.find('meta', attrs={'property': 'og:description'})['content']
	elif full_text:
		## TODO: improve content snippet extraction to skip junk titles and other non-content text
		meta_description = full_text[:160]
	else:
		meta_description = ""
	timestamp = int(datetime.now().timestamp())
	links = set()
	for a_tag in soup.find_all('a', href=True):
		link = a_tag['href']
		if link.startswith('/'):
			# Convert relative URL to absolute
			link = urljoin(url, link)
		if link.startswith('http'):
			# Remove ? tracking parameters
			link = link.split('?')[0]
			link = link.split('#')[0]
			link = link.lower()
			if link.endswith('/'):
				link = link[:-1]
			# Avoid duplicates
			links.add(link)
	return CrawlResponse(
		url=url,
		title=title,
		timestamp=timestamp,
		meta_description=meta_description,
		full_text=full_text,
		links=list(links)
	)

async def crawl_with_httpx(url) -> CrawlResponse:
	async with httpx.AsyncClient(timeout=1.0) as client:
		client.headers.update({
			"User-Agent": "NotGoogle Crawler (Contact: muhammad.rafikov@oplex.us)"
		})
		try:
			response = await client.get(url)
			if response.status_code == 403:
				return await crawl_with_playwright(url)
			if response.status_code != 200:
				raise Exception(f"Non-200 status code: {response.status_code}")

			soup = BeautifulSoup(response.text, 'html.parser')

			is_spa_app = spa_detector.detect_spa(soup)
			if is_spa_app:
				# Skip SPA apps in this crawler
				return await crawl_with_playwright(url)
			return generate_crawl_response(soup, url)
		except Exception as e:
			print(f"Error crawling {url}: {e}")
			return_response = CrawlResponse(
				url=url,
				title="",
				timestamp=0,
				meta_description="",
				full_text="",
				links=[]
			)
			return_response.set_failure()
			return return_response

async def crawl_with_playwright(url) -> CrawlResponse:
	async with async_playwright() as p:
		browser = await p.chromium.launch(headless=True)
		# Set user agent to mimic a real browser
		user_agent = "NotGoogle Chromium Headless (Contact: muhammad.rafikov@oplex.us)"
		context = await browser.new_context(user_agent=user_agent)
		page = await context.new_page()

		try:
			await page.goto(url)
			await page.wait_for_timeout(200)
			rendered_html = await page.content()
			# Pass any Are you a robot?
			page.dblclick('body')
			await browser.close()

			soup = BeautifulSoup(rendered_html, 'html.parser')
			return generate_crawl_response(soup, url)
		except Exception as e:
			await browser.close()
			return_response = CrawlResponse(
				url=url,
				title="",
				timestamp=0,
				meta_description="",
				full_text="",
				links=[]
			)
			return_response.set_failure()
			return return_response

async def main():
	urls = [
		# "https://techcrunch.com/",
		"https://www.bloomberg.com/",
		# "https://www.theverge.com/",
		# "https://www.wired.com/",
		# "https://www.cnet.com/"
	]
	# Crawl in sequence
	for url in urls:
		result = await crawl_with_httpx(url)
		print(f"URL: {result.url}")
		print(f"Title: {result.title}")
		print(f"Timestamp: {result.timestamp}")
		print(f"Meta Description: {result.meta_description}")
		print(f"Links Found: {len(result.links)}")
		print("-" * 80)

if __name__ == "__main__":
	start_time = datetime.now()
	asyncio.run(main())
	end_time = datetime.now()
	print(f"\nCrawling completed in {(end_time - start_time).total_seconds()} seconds.")