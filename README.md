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

## Full Text Search and Indexing
The full text will be used to create an inverted index for search queries. This will allow us to get the intersection of the query keywords and quickly retrieve relevant documents which we will then apply page rank and other ranking algorithms on.

## Imporovements to be made
- Using a traditional database that can scale beyond my PC's storage limits. Currently using SQLite for simplicity.
- Store full text in an s3 bucket or similar object storage to save space on the database.
- Implementing a more robust crawling mechanism that respects `robots.txt` and handles rate limiting.
- Enhancing the metadata extraction process to include more relevant information such as keywords, author, publication date, etc.

## Under Consideration
- The use of vector embeddings to allow for semantic search capabilities. Vector similarity would be performed on the final few results as a last step after traditional ranking algorithms have been applied. The reason why pure vector search is not being considered is because of the high computational cost and complexity involved in maintaining a vector database for a large corpus of documents. There is also the issue of a website being relevant but not credible (prevent AI slop results), which traditional ranking algorithms can help mitigate.

## Tables Used
URL Lookup Table:
- id (Primary Key)
- canonical_url (Unique, also a secondary index)
- content_hash (String)
- pagerank_score FLOAT
- pagerank_updated_at TIMESTAMP
- last_crawled (Timestamp)

Robots.txt Table:
- website (Primary Key)
- robots_txt_content (String)
- last_fetched (Timestamp)
- sitemap_url (String)

Crawled Data Table:
- id (Integer Primary Key that references URL Lookup Table)
- title (String)
- meta_description (String)
- full_text_path (String that points to object/local storage)
- h1_text (String)
- http_status (Integer)
- content_hash (String)
- timestamp (Integer)

Link Graph Table:
- id (Integer Primary Key)
- from_id (Integer)
- to_id (Integer)
- anchor_text (String)
- from_id and to_id are index and reference URL Lookup Table

Inverted Index Table:
- term_id (Integer Primary Key)
- term (Text Unique)
- document_frequency (Integer)

Postings Table:
- term_id (Integer)
- doc_id (Integer)
- term_frequency (Integer)
- positions (Array of Integers)
- Primary Key (term_id, doc_id)

Crawl Queue Table:
- id (Integer Primary Key that references URL Lookup Table)
- priority (Integer)
- added_at (Timestamp)
- attempts (Integer)
- locked_by (String)
- locked_at (Timestamp)
- status (Enum: pending, in_progress, completed, failed)