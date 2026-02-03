import sys
import base64
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def save_url_as_pdf(url, output_filename="output.pdf"):
    """
    Opens a URL in Chrome (headless) and saves it as a PDF in A4 Landscape format.
    """
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    
    # Initialize the driver
    print("Initializing Chrome Driver...")
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error initializing Chrome Driver: {e}")
        return

    try:
        print(f"Navigating to: {url}")
        driver.get(url)

        # Wait for the page to load completely. 
        # ChatGPT pages might take a moment to render the full conversation.
        print("Waiting for page load...")
        time.sleep(5) 

        # Additional logic could be added here to scroll to the bottom if content is lazy-loaded,
        # but shared links usually load the full context.

        # Configure print options for A4 Landscape
        # A4 size in inches: 8.27 x 11.69
        # Landscape: Width > Height
        print_options = {
            'landscape': True,
            'displayHeaderFooter': False,
            'printBackground': True,
            'paperWidth': 11.69,  # A4 width in inches (landscape)
            'paperHeight': 8.27,  # A4 height in inches (landscape)
            'marginTop': 0.4,
            'marginBottom': 0.4,
            'marginLeft': 0.4,
            'marginRight': 0.4,
        }

        print("Generating PDF...")
        # Execute Chrome DevTools Protocol command
        result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
        
        # Decode and write to file
        with open(output_filename, 'wb') as f:
            f.write(base64.b64decode(result['data']))
            
        print(f"Success! PDF saved to: {os.path.abspath(output_filename)}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Default URL if none provided
    default_url = "https://chatgpt.com/share/6968de77-861c-800f-9776-1d744b2ab113"
    
    target_url = default_url
    
    # Allow passing URL as command line argument
    if len(sys.argv) > 1:
        target_url = sys.argv[1]

    save_url_as_pdf(target_url, "chatgpt_conversation.pdf")
