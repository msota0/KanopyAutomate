import os
import xlrd
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from pathlib import Path

# Function to extract date from filename
def extract_date(filename):
    return filename.split('_')[1].split('.')[0]

def process_date(driver, date_ip, path, final_path):
    download_path = path
    destination = final_path
    
    # Populate start date
    driver.execute_script(f'document.getElementById("date_start").value = "{date_ip}";')
    driver.execute_script(f'document.getElementById("date_end").value = "{date_ip}";')
    
    # Click the Apply button
    apply_button = driver.find_element(By.ID, 'edit-submit')
    apply_button.click()
    
    try:
        link_xpath = '//*[@id="DataTables_Table_0_wrapper"]/div[1]/label/a'
        
        # Wait for the export-to-excel button to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, link_xpath)))
        
        # Click the export-to-excel button
        link_element = driver.find_element(By.XPATH, link_xpath)
        link_element.click()
        print("Clicked on the link successfully")
        
        time.sleep(5)
        
        # Get the latest downloaded file
        default_download_dir = download_path
        old_filename = max([os.path.join(default_download_dir, f) for f in os.listdir(default_download_dir)], key=os.path.getctime)
        
        # Rename the file with report_{date_ip}.xls
        new_filename = f'report_{date_ip}.xls'
        new_filepath = os.path.join(destination, new_filename)
        os.rename(old_filename, new_filepath)
        print(f"File downloaded and renamed to: {new_filename}")
        
        date_from_filename = extract_date(new_filename)
        
        # Open the Excel file and add the date column
        workbook = xlrd.open_workbook(new_filepath, on_demand=True, ignore_workbook_corruption=True)
        sheet = workbook.sheet_by_index(0)  # Assuming data is on the first sheet
        headers = sheet.row_values(0)  # Assuming headers are in the first row
        file_data = []
        
        for row_idx in range(1, sheet.nrows):
            row_data = sheet.row_values(row_idx)
            if len(row_data) == len(headers):
                row_data.append(date_from_filename)  # Append date to each row
                file_data.append(row_data)
            else:
                print(f"Skipping row {row_idx+1} in file {new_filename}: Row length does not match headers")
        
        # Convert to DataFrame
        df = pd.DataFrame(file_data, columns=headers + ['Date'])
        return df
    
    except TimeoutException:
        print(f"No data available for date {date_ip}, export-to-excel button not found")
        return None
    
    except Exception as e:
        print(f"Error processing date {date_ip}: {str(e)}")
        return None



# Selenium setup and login
driver = webdriver.Chrome()
login_url = 'https://www.kanopy.com/en/login'
username = input('Enter the username')
password = input('Enter the password')

# Directory setup
dates = [
  "2021-07-01", "2021-07-02", "2021-07-03", "2021-07-04", "2021-07-05", "2021-07-06", "2021-07-07", "2021-07-08", "2021-07-09", "2021-07-10",
  "2021-07-11", "2021-07-12", "2021-07-13", "2021-07-14", "2021-07-15", "2021-07-16", "2021-07-17", "2021-07-18", "2021-07-19", "2021-07-20",
  "2021-07-21", "2021-07-22", "2021-07-23", "2021-07-24", "2021-07-25", "2021-07-26", "2021-07-27", "2021-07-28", "2021-07-29", "2021-07-30", "2021-07-31",
  "2021-08-01", "2021-08-02", "2021-08-03", "2021-08-04", "2021-08-05", "2021-08-06", "2021-08-07", "2021-08-08", "2021-08-09", "2021-08-10",
  "2021-08-11", "2021-08-12", "2021-08-13", "2021-08-14", "2021-08-15", "2021-08-16", "2021-08-17", "2021-08-18", "2021-08-19", "2021-08-20",
  "2021-08-21", "2021-08-22", "2021-08-23", "2021-08-24", "2021-08-25", "2021-08-26", "2021-08-27", "2021-08-28", "2021-08-29", "2021-08-30", "2021-08-31",
  "2021-09-01", "2021-09-02", "2021-09-03", "2021-09-04", "2021-09-05", "2021-09-06", "2021-09-07", "2021-09-08", "2021-09-09", "2021-09-10",
  "2021-09-11", "2021-09-12", "2021-09-13", "2021-09-14", "2021-09-15", "2021-09-16", "2021-09-17", "2021-09-18", "2021-09-19", "2021-09-20",
  "2021-09-21", "2021-09-22", "2021-09-23", "2021-09-24", "2021-09-25", "2021-09-26", "2021-09-27", "2021-09-28", "2021-09-29", "2021-09-30",
  "2021-10-01", "2021-10-02", "2021-10-03", "2021-10-04", "2021-10-05", "2021-10-06", "2021-10-07", "2021-10-08", "2021-10-09", "2021-10-10",
  "2021-10-11", "2021-10-12", "2021-10-13", "2021-10-14", "2021-10-15", "2021-10-16", "2021-10-17", "2021-10-18", "2021-10-19", "2021-10-20",
  "2021-10-21", "2021-10-22", "2021-10-23", "2021-10-24", "2021-10-25", "2021-10-26", "2021-10-27", "2021-10-28", "2021-10-29", "2021-10-30", "2021-10-31",
  "2021-11-01", "2021-11-02", "2021-11-03", "2021-11-04", "2021-11-05", "2021-11-06", "2021-11-07", "2021-11-08", "2021-11-09", "2021-11-10",
  "2021-11-11", "2021-11-12", "2021-11-13", "2021-11-14", "2021-11-15", "2021-11-16", "2021-11-17", "2021-11-18", "2021-11-19", "2021-11-20",
  "2021-11-21", "2021-11-22", "2021-11-23", "2021-11-24", "2021-11-25", "2021-11-26", "2021-11-27", "2021-11-28", "2021-11-29", "2021-11-30",
  "2021-12-01", "2021-12-02", "2021-12-03", "2021-12-04", "2021-12-05", "2021-12-06", "2021-12-07", "2021-12-08", "2021-12-09", "2021-12-10",
  "2021-12-11", "2021-12-12", "2021-12-13", "2021-12-14", "2021-12-15", "2021-12-16", "2021-12-17", "2021-12-18", "2021-12-19", "2021-12-20",
  "2021-12-21", "2021-12-22", "2021-12-23", "2021-12-24", "2021-12-25", "2021-12-26", "2021-12-27", "2021-12-28", "2021-12-29", "2021-12-30", "2021-12-31",
  "2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06", "2022-01-07", "2022-01-08", "2022-01-09", "2022-01-10",
  "2022-01-11", "2022-01-12", "2022-01-13", "2022-01-14", "2022-01-15", "2022-01-16", "2022-01-17", "2022-01-18", "2022-01-19", "2022-01-20",
  "2022-01-21", "2022-01-22", "2022-01-23", "2022-01-24", "2022-01-25", "2022-01-26", "2022-01-27", "2022-01-28", "2022-01-29", "2022-01-30", "2022-01-31",
  "2022-02-01", "2022-02-02", "2022-02-03", "2022-02-04", "2022-02-05", "2022-02-06", "2022-02-07", "2022-02-08", "2022-02-09", "2022-02-10",
  "2022-02-11", "2022-02-12", "2022-02-13", "2022-02-14", "2022-02-15", "2022-02-16", "2022-02-17", "2022-02-18", "2022-02-19", "2022-02-20",
  "2022-02-21", "2022-02-22", "2022-02-23", "2022-02-24", "2022-02-25", "2022-02-26", "2022-02-27", "2022-02-28",
  "2022-03-01", "2022-03-02", "2022-03-03", "2022-03-04", "2022-03-05", "2022-03-06", "2022-03-07",  "2022-03-08", "2022-03-09", "2022-03-10", "2022-03-11", "2022-03-12", "2022-03-13", "2022-03-14", "2022-03-15", "2022-03-16",
  "2022-03-17", "2022-03-18", "2022-03-19", "2022-03-20", "2022-03-21", "2022-03-22", "2022-03-23", "2022-03-24", "2022-03-25", "2022-03-26",
  "2022-03-27", "2022-03-28", "2022-03-29", "2022-03-30", "2022-03-31",
  "2022-04-01", "2022-04-02", "2022-04-03", "2022-04-04", "2022-04-05", "2022-04-06", "2022-04-07", "2022-04-08", "2022-04-09", "2022-04-10",
  "2022-04-11", "2022-04-12", "2022-04-13", "2022-04-14", "2022-04-15", "2022-04-16", "2022-04-17", "2022-04-18", "2022-04-19", "2022-04-20",
  "2022-04-21", "2022-04-22", "2022-04-23", "2022-04-24", "2022-04-25", "2022-04-26", "2022-04-27", "2022-04-28", "2022-04-29", "2022-04-30",
  "2022-05-01", "2022-05-02", "2022-05-03", "2022-05-04", "2022-05-05", "2022-05-06", "2022-05-07", "2022-05-08", "2022-05-09", "2022-05-10",
  "2022-05-11", "2022-05-12", "2022-05-13", "2022-05-14", "2022-05-15", "2022-05-16", "2022-05-17", "2022-05-18", "2022-05-19", "2022-05-20",
  "2022-05-21", "2022-05-22", "2022-05-23", "2022-05-24", "2022-05-25", "2022-05-26", "2022-05-27", "2022-05-28", "2022-05-29", "2022-05-30", "2022-05-31",
  "2022-06-01", "2022-06-02", "2022-06-03", "2022-06-04", "2022-06-05", "2022-06-06", "2022-06-07", "2022-06-08", "2022-06-09", "2022-06-10",
  "2022-06-11", "2022-06-12", "2022-06-13", "2022-06-14", "2022-06-15", "2022-06-16", "2022-06-17", "2022-06-18", "2022-06-19", "2022-06-20",
  "2022-06-21", "2022-06-22", "2022-06-23", "2022-06-24", "2022-06-25", "2022-06-26", "2022-06-27", "2022-06-28", "2022-06-29", "2022-06-30",
  "2022-07-01", "2022-07-02", "2022-07-03", "2022-07-04", "2022-07-05", "2022-07-06", "2022-07-07", "2022-07-08", "2022-07-09", "2022-07-10",
  "2022-07-11", "2022-07-12", "2022-07-13", "2022-07-14", "2022-07-15", "2022-07-16", "2022-07-17", "2022-07-18", "2022-07-19", "2022-07-20",
  "2022-07-21", "2022-07-22", "2022-07-23", "2022-07-24", "2022-07-25", "2022-07-26", "2022-07-27", "2022-07-28", "2022-07-29", "2022-07-30", "2022-07-31",
  "2022-08-01", "2022-08-02", "2022-08-03", "2022-08-04", "2022-08-05", "2022-08-06", "2022-08-07", "2022-08-08", "2022-08-09", "2022-08-10",
  "2022-08-11", "2022-08-12", "2022-08-13", "2022-08-14", "2022-08-15", "2022-08-16", "2022-08-17", "2022-08-18", "2022-08-19", "2022-08-20",
  "2022-08-21", "2022-08-22", "2022-08-23", "2022-08-24", "2022-08-25", "2022-08-26", "2022-08-27", "2022-08-28", "2022-08-29", "2022-08-30", "2022-08-31",
  "2022-09-01", "2022-09-02", "2022-09-03", "2022-09-04", "2022-09-05", "2022-09-06", "2022-09-07", "2022-09-08", "2022-09-09", "2022-09-10",
  "2022-09-11", "2022-09-12", "2022-09-13", "2022-09-14", "2022-09-15", "2022-09-16", "2022-09-17", "2022-09-18", "2022-09-19", "2022-09-20",
  "2022-09-21", "2022-09-22", "2022-09-23", "2022-09-24", "2022-09-25", "2022-09-26", "2022-09-27", "2022-09-28", "2022-09-29", "2022-09-30",
  "2022-10-01", "2022-10-02", "2022-10-03", "2022-10-04", "2022-10-05", "2022-10-06", "2022-10-07", "2022-10-08", "2022-10-09", "2022-10-10",
  "2022-10-11", "2022-10-12", "2022-10-13", "2022-10-14", "2022-10-15", "2022-10-16", "2022-10-17", "2022-10-18", "2022-10-19", "2022-10-20",
  "2022-10-21", "2022-10-22", "2022-10-23", "2022-10-24", "2022-10-25", "2022-10-26", "2022-10-27", "2022-10-28", "2022-10-29", "2022-10-30", "2022-10-31",
  "2022-11-01", "2022-11-02", "2022-11-03", "2022-11-04", "2022-11-05", "2022-11-06", "2022-11-07", "2022-11-08", "2022-11-09", "2022-11-10",
  "2022-11-11", "2022-11-12", "2022-11-13", "2022-11-14", "2022-11-15", "2022-11-16", "2022-11-17", "2022-11-18", "2022-11-19", "2022-11-20",
  "2022-11-21", "2022-11-22", "2022-11-23", "2022-11-24", "2022-11-25", "2022-11-26", "2022-11-27", "2022-11-28", "2022-11-29", "2022-11-30",
  "2022-12-01", "2022-12-02", "2022-12-03", "2022-12-04", "2022-12-05", "2022-12-06", "2022-12-07", "2022-12-08", "2022-12-09", "2022-12-10",
  "2022-12-11", "2022-12-12", "2022-12-13", "2022-12-14", "2022-12-15", "2022-12-16", "2022-12-17", "2022-12-18", "2022-12-19", "2022-12-20",
  "2022-12-21", "2022-12-22", "2022-12-23", "2022-12-24", "2022-12-25", "2022-12-26", "2022-12-27", "2022-12-28", "2022-12-29", "2022-12-30", "2022-12-31",
  "2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06", "2023-01-07", "2023-01-08", "2023-01-09", "2023-01-10",
  "2023-01-11", "2023-01-12", "2023-01-13", "2023-01-14", "2023-01-15", "2023-01-16", "2023-01-17", "2023-01-18", "2023-01-19", "2023-01-20",
  "2023-01-21", "2023-01-22", "2023-01-23", "2023-01-24", "2023-01-25", "2023-01-26", "2023-01-27", "2023-01-28", "2023-01-29", "2023-01-30", "2023-01-31",
  "2023-02-01", "2023-02-02", "2023-02-03", "2023-02-04", "2023-02-05", "2023-02-06", "2023-02-07", "2023-02-08", "2023-02-09", "2023-02-10",
  "2023-02-11", "2023-02-12", "2023-02-13", "2023-02-14", "2023-02-15", "2023-02-16", "2023-02-17", "2023-02-18", "2023-02-19", "2023-02-20",
  "2023-02-21", "2023-02-22", "2023-02-23", "2023-02-24", "2023-02-25", "2023-02-26", "2023-02-27", "2023-02-28",
  "2023-03-01", "2023-03-02", "2023-03-03", "2023-03-04", "2023-03-05", "2023-03-06", "2023-03-07", "2023-03-08", "2023-03-09", "2023-03-10",
  "2023-03-11", "2023-03-12", "2023-03-13", "2023-03-14", "2023-03-15", "2023-03-16", "2023-03-17", "2023-03-18", "2023-03-19", "2023-03-20",
  "2023-03-21", "2023-03-22", "2023-03-23", "2023-03-24", "2023-03-25", "2023-03-26", "2023-03-27", "2023-03-28", "2023-03-29", "2023-03-30", "2023-03-31",
  "2023-04-01", "2023-04-02", "2023-04-03", "2023-04-04", "2023-04-05", "2023-04-06", "2023-04-07", "2023-04-08", "2023-04-09", "2023-04-10",
  "2023-04-11", "2023-04-12", "2023-04-13", "2023-04-14", "2023-04-15", "2023-04-16", "2023-04-17", "2023-04-18", "2023-04-19", "2023-04-20",
  "2023-04-21", "2023-04-22", "2023-04-23", "2023-04-24", "2023-04-25", "2023-04-26", "2023-04-27", "2023-04-28", "2023-04-29", "2023-04-30",
  "2023-05-01", "2023-05-02", "2023-05-03", "2023-05-04", "2023-05-05", "2023-05-06", "2023-05-07", "2023-05-08", "2023-05-09", "2023-05-10",
  "2023-05-11", "2023-05-12", "2023-05-13", "2023-05-14", "2023-05-15", "2023-05-16", "2023-05-17", "2023-05-18", "2023-05-19", "2023-05-20",
  "2023-05-21", "2023-05-22", "2023-05-23", "2023-05-24", "2023-05-25", "2023-05-26", "2023-05-27", "2023-05-28", "2023-05-29", "2023-05-30", "2023-05-31",
  "2023-06-01", "2023-06-02", "2023-06-03", "2023-06-04", "2023-06-05", "2023-06-06", "2023-06-07", "2023-06-08", "2023-06-09", "2023-06-10",
  "2023-06-11", "2023-06-12", "2023-06-13", "2023-06-14", "2023-06-15", "2023-06-16", "2023-06-17", "2023-06-18", "2023-06-19", "2023-06-20",
  "2023-06-21", "2023-06-22", "2023-06-23", "2023-06-24", "2023-06-25", "2023-06-26", "2023-06-27", "2023-06-28", "2023-06-29", "2023-06-30",
  "2023-07-01", "2023-07-02", "2023-07-03", "2023-07-04", "2023-07-05", "2023-07-06", "2023-07-07", "2023-07-08", "2023-07-09", "2023-07-10",
  "2023-07-11", "2023-07-12", "2023-07-13", "2023-07-14", "2023-07-15", "2023-07-16", "2023-07-17", "2023-07-18", "2023-07-19", "2023-07-20", "2023-07-21", "2023-07-22", "2023-07-23", "2023-07-24", "2023-07-25", "2023-07-26", "2023-07-27", "2023-07-28", "2023-07-29", "2023-07-30", "2023-07-31",
  "2023-08-01", "2023-08-02", "2023-08-03", "2023-08-04", "2023-08-05", "2023-08-06", "2023-08-07", "2023-08-08", "2023-08-09", "2023-08-10",
  "2023-08-11", "2023-08-12", "2023-08-13", "2023-08-14", "2023-08-15", "2023-08-16", "2023-08-17", "2023-08-18", "2023-08-19", "2023-08-20",
  "2023-08-21", "2023-08-22", "2023-08-23", "2023-08-24", "2023-08-25", "2023-08-26", "2023-08-27", "2023-08-28", "2023-08-29", "2023-08-30", "2023-08-31",
  "2023-09-01", "2023-09-02", "2023-09-03", "2023-09-04", "2023-09-05", "2023-09-06", "2023-09-07", "2023-09-08", "2023-09-09", "2023-09-10",
  "2023-09-11", "2023-09-12", "2023-09-13", "2023-09-14", "2023-09-15", "2023-09-16", "2023-09-17", "2023-09-18", "2023-09-19", "2023-09-20",
  "2023-09-21", "2023-09-22", "2023-09-23", "2023-09-24", "2023-09-25", "2023-09-26", "2023-09-27", "2023-09-28", "2023-09-29", "2023-09-30",
  "2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05", "2023-10-06", "2023-10-07", "2023-10-08", "2023-10-09", "2023-10-10",
  "2023-10-11", "2023-10-12", "2023-10-13", "2023-10-14", "2023-10-15", "2023-10-16", "2023-10-17", "2023-10-18", "2023-10-19", "2023-10-20",
  "2023-10-21", "2023-10-22", "2023-10-23", "2023-10-24", "2023-10-25", "2023-10-26", "2023-10-27", "2023-10-28", "2023-10-29", "2023-10-30", "2023-10-31",
  "2023-11-01", "2023-11-02", "2023-11-03", "2023-11-04", "2023-11-05", "2023-11-06", "2023-11-07", "2023-11-08", "2023-11-09", "2023-11-10",
  "2023-11-11", "2023-11-12", "2023-11-13", "2023-11-14", "2023-11-15", "2023-11-16", "2023-11-17", "2023-11-18", "2023-11-19", "2023-11-20",
  "2023-11-21", "2023-11-22", "2023-11-23", "2023-11-24", "2023-11-25", "2023-11-26", "2023-11-27", "2023-11-28", "2023-11-29", "2023-11-30",
  "2023-12-01", "2023-12-02", "2023-12-03", "2023-12-04", "2023-12-05", "2023-12-06", "2023-12-07", "2023-12-08", "2023-12-09", "2023-12-10",
  "2023-12-11", "2023-12-12", "2023-12-13", "2023-12-14", "2023-12-15", "2023-12-16", "2023-12-17", "2023-12-18", "2023-12-19", "2023-12-20",
  "2023-12-21", "2023-12-22", "2023-12-23", "2023-12-24", "2023-12-25", "2023-12-26", "2023-12-27", "2023-12-28", "2023-12-29", "2023-12-30", "2023-12-31",
  "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08", "2024-01-09", "2024-01-10",
  "2024-01-11", "2024-01-12", "2024-01-13", "2024-01-14", "2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19", "2024-01-20",
  "2024-01-21", "2024-01-22", "2024-01-23", "2024-01-24", "2024-01-25", "2024-01-26", "2024-01-27", "2024-01-28", "2024-01-29", "2024-01-30", "2024-01-31",
  "2024-02-01", "2024-02-02", "2024-02-03", "2024-02-04", "2024-02-05", "2024-02-06", "2024-02-07", "2024-02-08", "2024-02-09", "2024-02-10",
  "2024-02-11", "2024-02-12", "2024-02-13", "2024-02-14", "2024-02-15", "2024-02-16", "2024-02-17", "2024-02-18", "2024-02-19", "2024-02-20",
  "2024-02-21", "2024-02-22", "2024-02-23", "2024-02-24", "2024-02-25", "2024-02-26", "2024-02-27", "2024-02-28", 
  "2024-02-29", "2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-08", "2024-03-09", "2024-03-10",
  "2024-03-11", "2024-03-12", "2024-03-13", "2024-03-14", "2024-03-15", "2024-03-16", "2024-03-17", "2024-03-18", "2024-03-19", "2024-03-20",
  "2024-03-21", "2024-03-22", "2024-03-23", "2024-03-24", "2024-03-25", "2024-03-26", "2024-03-27", "2024-03-28", "2024-03-29", "2024-03-30", "2024-03-31",
  "2024-04-01", "2024-04-02", "2024-04-03", "2024-04-04", "2024-04-05", "2024-04-06", "2024-04-07", "2024-04-08", "2024-04-09", "2024-04-10",
  "2024-04-11", "2024-04-12", "2024-04-13", "2024-04-14", "2024-04-15", "2024-04-16", "2024-04-17", "2024-04-18", "2024-04-19", "2024-04-20",
  "2024-04-21", "2024-04-22", "2024-04-23", "2024-04-24", "2024-04-25", "2024-04-26", "2024-04-27", "2024-04-28", "2024-04-29", "2024-04-30",
  "2024-05-01", "2024-05-02", "2024-05-03", "2024-05-04", "2024-05-05", "2024-05-06", "2024-05-07", "2024-05-08", "2024-05-09", "2024-05-10",
  "2024-05-11", "2024-05-12", "2024-05-13", "2024-05-14", "2024-05-15", "2024-05-16", "2024-05-17", "2024-05-18", "2024-05-19", "2024-05-20",
  "2024-05-21", "2024-05-22", "2024-05-23", "2024-05-24", "2024-05-25", "2024-05-26", "2024-05-27", "2024-05-28", "2024-05-29", "2024-05-30", "2024-05-31",
  "2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04", "2024-06-05", "2024-06-06", "2024-06-07", "2024-06-08", "2024-06-09", "2024-06-10",
  "2024-06-11", "2024-06-12", "2024-06-13", "2024-06-14", "2024-06-15", "2024-06-16", "2024-06-17", "2024-06-18", "2024-06-19", "2024-06-20",
  "2024-06-21", "2024-06-22", "2024-06-23", "2024-06-24", "2024-06-25", "2024-06-26", "2024-06-27", "2024-06-28", "2024-06-29", "2024-06-30"
]

path = r'C:\Users\MDsota\Downloads'

# month_names = {
#     '01': 'January', '02': 'February', '03': 'March', '04': 'April',
#     '05': 'May', '06': 'June', '07': 'July', '08': 'August',
#     '09': 'September', '10': 'October', '11': 'November', '12': 'December'
# }

# current_month_number = dates[0].split('-')[1]
# folder_name = month_names[current_month_number]
folder_name = 'Reports-Folder'
destination_path = os.path.join(path, folder_name)
Path(destination_path).mkdir(parents=True, exist_ok=True)

try:
    # Open the login page
    driver.get(login_url)
    print("Opened login page")
    time.sleep(1)

    # Enter username and password
    username_field = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[3]/form/div[1]/input')
    username_field.send_keys(username)
    time.sleep(1)

    password_field = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[3]/form/div[2]/input')
    password_field.send_keys(password)
    time.sleep(1)

    # Click login button
    login_btn = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[3]/form/button')
    login_btn.click()

    # Check if login was successful
    print(driver.current_url)
    WebDriverWait(driver, 10).until(EC.url_contains('/user/'))
    if '/user/' in driver.current_url:
        print("Login successful!")

        # Navigate to analytics page
        user_id = driver.current_url.split('/')[-1]
        analytics_url = f'https://www.kanopy.com/user/{user_id}/analytics-ng/'
        driver.get(analytics_url)
        time.sleep(3)

        # Click links and process each date
        link1 = driver.find_element(By.XPATH, '/html/body/div[3]/main/div[1]/ul/li[2]/a')
        link1.click()
        time.sleep(3)

        link2 = driver.find_element(By.XPATH, '//*[@id="content-area"]/div/div/div[1]/div/div[1]/div/div/a[3]')
        link2.click()
        time.sleep(3)

        dfs = []
        for date_ip in dates:
            df = process_date(driver, date_ip, path, destination_path)
            if df is not None:
                dfs.append(df)

    else:
        print("Login failed. Please check your credentials.")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the browser
    driver.quit()

# Combine all DataFrames into a single DataFrame and save to Excel
if dfs:
    combined_data = pd.concat(dfs, ignore_index=True)
    combined_data_filename = f'Combined_Data_of_{folder_name}.xlsx'
    output_file = os.path.join(destination_path, combined_data_filename)
    combined_data.to_excel(output_file, index=False)
    print(f"Combined data saved to {output_file}")
else:
    print("No data to combine or save. Check previous error messages for details.")
