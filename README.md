# NotGoogle
A simple search engine project written in Python. This project is ongoing and aims to create a basic search engine from scratch that implements page rank.

## The Crawler
The crawler is responsible for fetching web pages and extracting relevant information such as title, meta description, and content snippets. It uses libraries like `requests` and `BeautifulSoup` to handle HTTP requests and parse HTML content. It will also create a stack of websites that are yet to be crawled or have not be re-crawled in a long time.

## The Useful Metadata
The crawler extracts the following metadata from each web page:
- **Title**: The title of the web page, extracted from the `<title>` tag
- **Meta Description**: A brief description of the web page, extracted from the `<meta name="description">` tag or other relevant tags.
- **Content Snippet**: A short snippet of text from the web page content, used for previewing search results. Used as a fallback for meta description.
- **Full Text**: The complete text content of the web page
- **H1 Text**: The text contained within the first `<h1>` tag on the page
- **H2 Tags**: A list of texts contained within all `<h2>` tags on the page which can be used for easy sectional linking on a results page.

## Full Text Search and Indexing
The full text will be used to create an inverted index for search queries. This will allow us to get the intersection of the query keywords and quickly retrieve relevant documents which we will then apply page rank and other ranking algorithms on.