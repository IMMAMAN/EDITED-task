from app.utils.crawler import web_crawl

def start_screenshot_process(start_url, num_links, unique_id):
    try:
        # Start the crawling and screenshot process
        web_crawl(start_url, num_links, unique_id)
        
        return True
    except Exception as e:
        print(f"Error during screenshot process: {e}")
        return False
