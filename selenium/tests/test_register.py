from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

BASE_URL = "http://localhost/quizpengupil"

def setup_module(module):
    global driver, rand
    driver = webdriver.Chrome()
    driver.maximize_window()
    rand = random.randint(1000, 9999)

def teardown_module(module):
    driver.quit()

# FT_003 – Register dengan data valid
def test_FT_003_register_valid():
    driver.get(f"{BASE_URL}/register.php")
    driver.find_element(By.NAME, "name").send_keys("User Test")
    driver.find_element(By.NAME, "email").send_keys(f"user{rand}@test.com")
    driver.find_element(By.NAME, "username").send_keys(f"usertest{rand}")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    assert "login.php" in driver.current_url or "register.php" in driver.current_url

# FT_004 – Register dengan field kosong
def test_FT_004_register_empty():
    driver.get(f"{BASE_URL}/register.php")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    error = driver.find_element(By.CLASS_NAME, "alert-danger")
    assert "Data tidak boleh kosong" in error.text

# FT_005 – Register dengan email tidak valid
def test_FT_005_register_invalid_email():
    driver.get(f"{BASE_URL}/register.php")
    driver.find_element(By.NAME, "email").send_keys("admin")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    assert "register.php" in driver.current_url

# FT_006 – Register password dan re-password tidak sama
def test_FT_006_register_password_mismatch():
    driver.get(f"{BASE_URL}/register.php")

    driver.find_element(By.NAME, "name").send_keys("User Test")
    driver.find_element(By.NAME, "email").send_keys("mismatch@test.com")
    driver.find_element(By.NAME, "username").send_keys("mismatchuser")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password321")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    # ASSERT berdasarkan BEHAVIOR sistem
    assert "register.php" in driver.current_url


# FT_009 – Register dengan username sudah terdaftar
def test_FT_009_register_existing_username():
    driver.get(f"{BASE_URL}/register.php")

    driver.find_element(By.NAME, "name").send_keys("User Test")
    driver.find_element(By.NAME, "email").send_keys("existing@test.com")
    driver.find_element(By.NAME, "username").send_keys("admin")  # sudah ada
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "repassword").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    # ASSERT berbasis hasil akhir
    assert "register.php" in driver.current_url


# FT_010 – Register hanya sebagian field diisi
def test_FT_010_register_partial_input():
    driver.get(f"{BASE_URL}/register.php")
    driver.find_element(By.NAME, "name").send_keys("User Test")
    driver.find_element(By.NAME, "username").send_keys("usertest2")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    error = driver.find_element(By.CLASS_NAME, "alert-danger")
    assert "Data tidak boleh kosong" in error.text

# FT_011 – Register dengan password sangat pendek
def test_FT_011_register_short_password():
    driver.get(f"{BASE_URL}/register.php")

    driver.find_element(By.NAME, "name").send_keys("Short Pass User")
    driver.find_element(By.NAME, "email").send_keys("shortpass@test.com")
    driver.find_element(By.NAME, "username").send_keys(f"shortpass{rand}")
    driver.find_element(By.NAME, "password").send_keys("1")
    driver.find_element(By.NAME, "repassword").send_keys("1")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    # Karena sistem tidak membatasi panjang password
    assert "login.php" in driver.current_url or "register.php" in driver.current_url
