import sqlite3

stack_conn = sqlite3.connect('stack.db')

# The stack will contain non-visited websites
# The scraped will be a db of visited websites
stack_conn.execute('''
CREATE TABLE IF NOT EXISTS stack
			 (url TEXT PRIMARY KEY NOT NULL);''')

cursor = stack_conn.cursor()

# If there are no websites in the stack, add a seed website
cursor.execute('SELECT COUNT(*) FROM stack;')
count = cursor.fetchone()[0]
if count == 0:
	seeds = [
		"https://techcrunch.com/",
		"https://www.bloomberg.com/",
		"https://www.theverge.com/",
		"https://www.wired.com/",
		"https://www.cnet.com/",
		"https://www.crunchyroll.com/news",
		"https://www.reddit.com/r/science/",
		"https://www.reddit.com/r/programming/",
		"https://apnews.com/",
		"https://www.reddit.com/r/technology/",
		"https://blog.google/",
		"https://www.reddit.com/r/news/"

	]
	# Add the first seed to the stack
	stack_conn.execute("INSERT INTO stack (url) VALUES (?);", (seeds[0],))
	stack_conn.commit()

visited_conn = sqlite3.connect('scraped.db')