import os
import logging
from urllib.parse import urljoin, urlparse

from flask import current_app
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import zipfile
from app.models.models import ScreenshotSession
from app.models.enums import CrawlSessionStatus
from app.app import db


#TODO: function except web_crawl can go to a better place e.g service_utls
#TODO: files should be saved to some external storage e.g s3 
# in docker files are lost once the container is stopped; same for db changes
def take_screenshot(page, url, screenshot_folder, unique_id, count):
    try:
        page.goto(url, timeout=10000)
        screenshot_path = os.path.join(screenshot_folder, f"{unique_id}_{count}.png")
        page.screenshot(path=screenshot_path)
        logging.info(f"Screenshot taken for: {url}")
    except Exception as e:
        logging.error(f"Error taking screenshot for {url}: {e}")
        raise


def collect_links(page, url, num_links):
    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)
    links = set(links)
    links_set = {url}
    #TODO: set is not fixing the issue of duplicates might need to do string match 
    # or check whats after netloc and /
    for link in links:
        if len(links_set) > num_links:
            break

        href = link.get('href')
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)
        if parsed_url.netloc:
            links_set.add(full_url)
    return links_set

def zip_screenshots(screenshot_folder, unique_id):    
    files = [f for f in os.listdir(screenshot_folder) if f.endswith('.png')]
    zip_filename = f"{unique_id}.zip"
    zip_path = os.path.join(current_app.root_path, 'screenshots', unique_id, zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files:
                file_path = os.path.join(screenshot_folder, file)
                zipf.write(file_path, file)

def create_instance(unique_id, start_url, num_links):
    screenshot_session = ScreenshotSession(
        id=unique_id,
        start_url=start_url,
        num_links=num_links,
    )
    db.session.add(screenshot_session)
    db.session.commit()


def update_instance(unique_id, status):
    screenshot_session = ScreenshotSession.query.get(unique_id)
    try:
        screenshot_session.status = status
        db.session.commit()
    except Exception as e:
        logging.error(f"Error updating screenshot session status: {e}")
        db.session.rollback()
        raise

#TODO: async or celery
def web_crawl(start_url, num_links, unique_id):
    screenshot_folder = os.path.join(current_app.root_path, 'screenshots', unique_id)
    create_instance(unique_id, start_url, num_links)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(start_url)
            links_to_go = collect_links(page, start_url, num_links)

            for count, url in enumerate(links_to_go, start=1):
                take_screenshot(page, url, screenshot_folder, unique_id, count)
            browser.close()
            logging.info("Crawling and screenshot process completed successfully.")
        
        zip_screenshots(screenshot_folder, unique_id)
        logging.info(f"Zipped screenshots for ID: {unique_id}")
        update_instance(unique_id, CrawlSessionStatus.COMPLETED)
    except FileNotFoundError:
        update_instance(unique_id, CrawlSessionStatus.FAILED)
        logging.error(f"Screenshot folder not found: {screenshot_folder}")
        raise
    except Exception as e:
        update_instance(unique_id, CrawlSessionStatus.FAILED)
        logging.error(f"Error launching Playwright: {e}")
        raise
    
