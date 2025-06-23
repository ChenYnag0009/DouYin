from playwright.sync_api import sync_playwright

def download_from_douyin_wtf(link: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://douyin.wtf/", timeout=60000)

        # Paste link and submit
        page.fill("input[name='url']", link)
        page.click("button[type='submit']")

        # Wait for video to appear
        try:
            page.wait_for_selector("video", timeout=15000)
            video_src = page.locator("video").get_attribute("src")
            return video_src
        except:
            return None
        finally:
            browser.close()
