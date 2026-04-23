import os
import glob
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

ROOT = os.path.abspath(os.path.dirname(__file__))
HTML_PATH = os.path.join(ROOT, "screenr.html")

def find_latest(paths):
    if not paths:
        return None
    return max(paths, key=lambda p: os.path.getmtime(p))

def find_drivers():
    edge_paths = glob.glob(os.path.expanduser(r"~\.cache\selenium\msedgedriver\win64\*\msedgedriver.exe"))
    chrome_paths = glob.glob(os.path.expanduser(r"~\.cache\selenium\chromedriver\win64\*\chromedriver.exe"))
    return {
        "edge": find_latest(edge_paths) if edge_paths else None,
        "chrome": find_latest(chrome_paths) if chrome_paths else None,
    }

def build_driver():
    drivers = find_drivers()
    browser = "edge" if drivers.get("edge") else "chrome"
    driver_path = drivers.get(browser)
    
    if not driver_path:
        print("No driver found. Using default.")
        try:
            options = EdgeOptions()
            options.add_argument("--headless=new")
            return webdriver.Edge(options=options)
        except:
            options = ChromeOptions()
            options.add_argument("--headless=new")
            return webdriver.Chrome(options=options)

    if browser == "edge":
        options = EdgeOptions()
        options.add_argument("--headless=new")
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        service = EdgeService(executable_path=driver_path)
        return webdriver.Edge(service=service, options=options)
    else:
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        service = ChromeService(executable_path=driver_path)
        return webdriver.Chrome(service=service, options=options)

def main():
    driver = build_driver()
    try:
        url = f"file:///{HTML_PATH.replace(os.sep, '/')}"
        print(f"Loading {url}...")
        driver.get(url)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        print("Running validation suite...")
        # runAllTests now includes the integrated additional tests
        results = driver.execute_script("return ExtendedValidationSuite.runAllTests();")
        
        passed_count = 0
        failed_count = 0
        
        print("\n--- Validation Results ---")
        for res in results:
            status = "PASS" if res.get('passed') else "FAIL"
            if res.get('passed'):
                passed_count += 1
            else:
                failed_count += 1
                
            print(f"[{status}] {res.get('name')}")
            if not res.get('passed'):
                print(f"  Expected: {res.get('expected')}")
                print(f"  Actual:   {res.get('actual')}")
        
        print(f"\nTotal: {len(results)}")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")
        
        if failed_count > 0:
            logs = driver.get_log('browser')
            for entry in logs:
                print(entry)
            exit(1)
            
    except Exception as e:
        print(f"CRASH: {e}")
        logs = driver.get_log('browser')
        for entry in logs:
            print(entry)
        raise e
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
