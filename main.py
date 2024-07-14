from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging

# Setup logging
logging.basicConfig(filename='gold_bar_finder.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the website
driver.get('http://sdetchallenge.fetch.com/')

# Function to clear the bowls by clicking the reset button
def clear_bowls():
    logging.info("Clicking the Reset button to clear the bowls")
    attempts = 0

    while attempts < 5:
        try:
            # Try finding the reset button using various selectors
            reset_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Reset"]'))
            )
        except Exception as e:
            logging.error(f"Could not find Reset button by XPATH: {e}")
            try:
                reset_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#reset.button'))
                )
            except Exception as e:
                logging.error(f"Could not find Reset button by CSS_SELECTOR: {e}")
                reset_button = None

        if reset_button:
            try:
                # Using ActionChains to click the button
                actions = ActionChains(driver)
                actions.move_to_element(reset_button).click().perform()
                logging.info("Reset button successfully clicked using ActionChains")
                time.sleep(3)

                # Checking if the bowls are cleared
                all_clean = True
                for i in range(3):
                    left_bowl = driver.find_element(By.XPATH, f'//*[@id="left_{i}"]')
                    right_bowl = driver.find_element(By.XPATH, f'//*[@id="right_{i}"]')
                    if left_bowl.get_attribute('value') or right_bowl.get_attribute('value'):
                        logging.warning(f"Bowl {i} not cleared")
                        all_clean = False
                    else:
                        logging.info(f"Bowl {i} successfully cleared")
                if all_clean:
                    return
                else:
                    logging.warning("Could not clear all bowls")
            except Exception as e:
                logging.error(f"Could not click Reset button using ActionChains: {e}")

        attempts += 1
        time.sleep(1)  # Wait before next attempt

# Function to fill the bowls for the first weighing
def fill_bowls_first_weighing():
    clear_bowls()
    logging.info("Filling bowls for the first weighing")
    left_bowls = [driver.find_element(By.XPATH, '//*[@id="left_0"]'),
                  driver.find_element(By.XPATH, '//*[@id="left_1"]'),
                  driver.find_element(By.XPATH, '//*[@id="left_2"]')]
    right_bowls = [driver.find_element(By.XPATH, '//*[@id="right_0"]'),
                   driver.find_element(By.XPATH, '//*[@id="right_1"]'),
                   driver.find_element(By.XPATH, '//*[@id="right_2"]')]

    for i, bowl in enumerate(left_bowls):
        logging.info(f"Placing coin {i} in the left bowl")
        bowl.send_keys(str(i))

    for i, bowl in enumerate(right_bowls):
        logging.info(f"Placing coin {i + 3} in the right bowl")
        bowl.send_keys(str(i + 3))

    time.sleep(2)

# Function to fill the bowls for the second weighing
def fill_bowls_second_weighing(left_coin, right_coin):
    clear_bowls()
    logging.info("Filling bowls for the second weighing")

    left_bowl = driver.find_element(By.XPATH, '//*[@id="left_0"]')
    right_bowl = driver.find_element(By.XPATH, '//*[@id="right_0"]')

    logging.info(f"Placing coin {left_coin} in the left bowl")
    left_bowl.send_keys(str(left_coin))

    logging.info(f"Placing coin {right_coin} in the right bowl")
    right_bowl.send_keys(str(right_coin))

    time.sleep(2)

# Function to get the result of the weighing
def get_weighing_result():
    driver.find_element(By.XPATH, '//*[@id="weigh"]').click()
    time.sleep(2)
    try:
        logging.info("Waiting for the weighing result...")
        result_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="game-info"]/ol/li[last()]'))
        )
        result = result_element.text
        logging.info(f"Weighing result: {result}")
        return result
    except Exception as e:
        logging.error(f"Could not get the weighing result: {e}")
        try:
            alert = driver.switch_to.alert
            logging.warning(f"Alert Text: {alert.text}")
            alert.accept()
        except:
            pass
        return None

# Function to handle second weighing and determine fake coin
def second_weighing(result):
    if "<" in result:
        logging.info("Left bowl is lighter")
        fill_bowls_second_weighing(0, 1)
        second_result = get_weighing_result()
        if "=" in second_result:
            logging.info("Coin 2 is fake")
            fake_coin = 2
        elif "<" in second_result:
            logging.info("Coin 0 is fake")
            fake_coin = 0
        else:
            logging.info("Coin 1 is fake")
            fake_coin = 1
    elif ">" in result:
        logging.info("Right bowl is lighter")
        fill_bowls_second_weighing(3, 4)
        second_result = get_weighing_result()
        if "=" in second_result:
            logging.info("Coin 5 is fake")
            fake_coin = 5
        elif "<" in second_result:
            logging.info("Coin 3 is fake")
            fake_coin = 3
        else:
            logging.info("Coin 4 is fake")
            fake_coin = 4
    elif "=" in result:
        logging.info("Bowls are equal")
        fill_bowls_second_weighing(6, 7)
        second_result = get_weighing_result()
        if "=" in second_result:
            logging.info("Coin 8 is fake")
            fake_coin = 8
        elif "<" in second_result:
            logging.info("Coin 6 is fake")
            fake_coin = 6
        else:
            logging.info("Coin 7 is fake")
            fake_coin = 7
    else:
        fake_coin = None

    if fake_coin is not None:
        logging.info(f"Clicking the fake coin button: {fake_coin}")
        driver.find_element(By.XPATH, f'//*[@id="coin_{fake_coin}"]').click()
        time.sleep(2)
        alert = driver.switch_to.alert
        logging.info(f"Fake bar: {fake_coin}, Alert message: {alert.text}")
        alert.accept()

# Main logic for the first and second weighings
def first_weighing():
    fill_bowls_first_weighing()
    result = get_weighing_result()
    logging.info(f"First weighing result: {result}")

    if result is None:
        logging.error("Error getting first weighing result")
    else:
        logging.info(f"Successfully got the first weighing result: {result}")
        second_weighing(result)

# Run the main logic for first and second weighings
first_weighing()

# Close the driver
driver.quit()
