# Events

## Scraping a Page
1. A Website is in the crawl queue either by being added manually or discovered via links from other pages.
2. The script looks for in_progress entries that are not locked or have been locked for more than a threshold time (e.g., 10 minutes)\ to avoid stale locks.
3. [ROBOTS_EVENT] The crawler fetches the robots.txt
4. If the page is allowed to be crawled according to robots.txt, the crawler proceeds; otherwise, it marks the URL as failed in the crawl queue.
5. The crawler fetches the page content and records the HTTP status code.
7. The html of the page is stored locally or in an object storage service (e.g., S3).
6. The scraper stores the scraped data and the path to the stored html into the crawled data table and the content hash is computed.
7. If the page is new add to the url lookup table.
8. The last crawled timestamp is updated in the URL Lookup Table.
9. All the links from the page are added to the link graph table.
10. Any fetched links are added to the crawl queue if new and allowable by robots.txt.
11. Mark the URL as completed in the crawl queue.
12. Add the URL to the indexing queue for full text indexing.

## Fetching Robots.txt
1. The crawler checks if the robots.txt for the website is already stored and if it was fetched recently (e.g., within the last week).
2. If not, it fetches the robots.txt file from the root of the website.
3. The content of robots.txt is stored in the Robots.txt Table along with the fetch timestamp.
4. The crawler parses the robots.txt to determine allowed and disallowed paths for crawling.
5. If a sitemap URL is found in robots.txt, it is added to the crawl queue for future processing.
6. The crawler respects the rules defined in robots.txt when deciding whether to crawl a page or not.

## Indexing a Page
1. The indexing service picks URLs from the indexing queue.
2. It fetches the full text content from the stored path in the crawled data table.
3. The full text is tokenized into terms, and an inverted index is built.
4. Each term is stored in the Inverted Index Table with its document frequency.
5. The postings for each term are stored in the Postings Table, including term frequency and positions within the document.
6. The indexing service updates the URL Lookup Table with the content hash and the last indexed timestamp.
7. The indexing service updates the crawl queue status to completed for the URL.