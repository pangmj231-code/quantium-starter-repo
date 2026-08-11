"""
Test suite for the Soul Foods Dash application.
Uses unittest and Selenium to verify core UI components.
"""

import unittest
import threading
import time
from app import app

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestDashApp(unittest.TestCase):
    """Test cases for the Dash application."""
    
    @classmethod
    def setUpClass(cls):
        """Start the Dash server and WebDriver once before all tests."""
        # Run Dash app in a separate thread
        cls.server_thread = threading.Thread(target=lambda: app.run(debug=False, use_reloader=False, port=8050))
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Give the server time to start
        time.sleep(3)
        
        # Set up WebDriver with automatic ChromeDriver management
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (no browser window)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Use ChromeDriverManager to automatically download and use the correct driver
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.get("http://127.0.0.1:8050/")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        cls.driver.quit()
    
    def test_1_header_present(self):
        """Test Case 1: Verify page header exists."""
        wait = WebDriverWait(self.driver, 10)
        header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        self.assertIsNotNone(header)
        self.assertGreater(len(header.text), 0)
        print(f"Header found: {header.text}")
    
    def test_2_visualization_present(self):
        """Test Case 2: Verify chart visualization is rendered."""
        wait = WebDriverWait(self.driver, 10)
        # Wait for Plotly chart to load (it creates a .js-plotly-plot element)
        chart = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".js-plotly-plot")))
        self.assertIsNotNone(chart)
        print("Chart found successfully")
    
    def test_3_region_picker_present(self):
        """Test Case 3: Verify region selector exists."""
        wait = WebDriverWait(self.driver, 10)
        # Look for radio input elements
        radio = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio']")))
        self.assertIsNotNone(radio)
        print("Region picker found successfully")

if __name__ == "__main__":
    unittest.main(verbosity=2)