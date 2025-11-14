# Print the number of websites in the stack and the scraped database
import sqlite3

def get_stats():
	stack_conn = sqlite3.connect('stack.db')
	scraped_conn = sqlite3.connect('scraped.db')

	stack_cursor = stack_conn.cursor()
	scraped_cursor = scraped_conn.cursor()

	# Get count of websites in the stack
	stack_cursor.execute('SELECT COUNT(*) FROM stack;')
	stack_count = stack_cursor.fetchone()[0]

	# Get count of websites in the scraped database
	scraped_cursor.execute('SELECT COUNT(*) FROM scraped;')
	scraped_count = scraped_cursor.fetchone()[0]

	print(f'Websites in stack: {stack_count}')
	print(f'Websites in scraped database: {scraped_count}')

	stack_conn.close()
	scraped_conn.close()

if __name__ == "__main__":
	get_stats()