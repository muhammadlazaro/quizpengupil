from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import os
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:8080"

def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def setup_module(module):
    global driver
    driver = create_driver()

def teardown_module(module):
    driver.quit()

# FT_001 – Login dengan kredensial valid
def test_FT_001_login_valid():
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    assert "login.php" in driver.current_url

# FT_002 – Login dengan field kosong
def test_FT_002_login_empty():
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    error = driver.find_element(By.CLASS_NAME, "alert-danger")
    assert "Data tidak boleh kosong" in error.text

# FT_007 – Login dengan username tidak terdaftar
def test_FT_007_login_unregistered():
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.NAME, "username").send_keys("user_salah")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    error = driver.find_element(By.CLASS_NAME, "alert-danger")
    assert error.is_displayed()

# FT_008 – Login dengan password salah
def test_FT_008_login_wrong_password():
    driver.get(f"{BASE_URL}/login.php")

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("salah123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    # ASSERT berbasis behavior sistem
    assert "login.php" in driver.current_url


# FT_012 – Navigasi dari Login ke Register
def test_FT_012_navigate_login_to_register():
    driver.get(f"{BASE_URL}/login.php")

    driver.find_element(By.LINK_TEXT, "Register").click()
    time.sleep(1)

    assert "register.php" in driver.current_url
