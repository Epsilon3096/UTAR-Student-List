import requests
import time
import browser_cookie3  # Extract cookies after manual login
import undetected_chromedriver as uc  # Bypass bot detection
from bs4 import BeautifulSoup
import concurrent.futures
import pandas as pd
import re
import threading
import json

# Name, Profile, Course_Code
"""
# URL Configuration
LOGIN_URL = "https://ewble-sl.utar.edu.my/login/index.php" # Edited
TARGET_PAGE = "https://ewble-sl.utar.edu.my/user/index.php?id=15253" # Edited

Students = {}
default_course = "INFORMATION SKILLS PROGRAMME TO FYP STUDENTS"
id_number = 00000
data_lock = threading.Lock()

format = f"https://ewble-sl.utar.edu.my/user/view.php?id={id_number}&course=5640" # course=5640 as default

# URL generation
urls = [
    "https://ewble-sl.utar.edu.my/user/view.php?id=50715&course=5640",
    "https://ewble-sl.utar.edu.my/user/view.php?id=69715&course=5640",
    "https://ewble-sl.utar.edu.my/user/view.php?id=71070&course=5640"
]
"""

class ClassName:
    def __init__(self):
        """ Parameter Setup """
        # URL Configuration
        selfLOGIN_URL = "https://ewble-sl.utar.edu.my/login/index.php" # Edited
        self.TARGET_PAGE = "https://ewble-sl.utar.edu.my/user/index.php?id=15253" # Edited

        self.urls = []
        self.students = {}
        self.default_course = "INFORMATION SKILLS PROGRAMME TO FYP STUDENTS"
        self.errorurl = []
        self.data_lock = threading.Lock()

        # Cookies Input
        value1 = input("MOODLEID_ewbleSL: ")
        value2 = input("MoodleSessionTestewbleSL: ")
        value3 = input("MoodleSessionewbleSL: ")

        self.cookies_dict = {
            "MOODLEID_ewbleSL": f"{value1}", 
            "MoodleSessionTestewbleSL": f"{value2}", 
            "MoodleSessionewbleSL": f"{value3}"
        }

        self.ID_generation()

        return None

    # Generate ID for URL
    def ID_generation(self):
        
        for id_number in range(0, 99999):
            url = f"https://ewble-sl.utar.edu.my/user/view.php?id={id_number:05}&course=5640" # course=5640 as default
            self.urls.append(url)
                
        self.Threading()

        return None

    # Use requests to access the protected page
    def webpage_access(self, url):
        
        print("🔹 Accessing protected page...")
        self.session = requests.Session()
        self.session.cookies.update(self.cookies_dict)

        self.response = self.session.get(self.TARGET_PAGE)

        return self.webpage_fetching(url)

    # Fetching Webpage Status
    def webpage_fetching(self, url):
        try:
            self.response = self.session.get(url)
            self.response.raise_for_status()  # Raise error for bad response

        except Exception as e:
            self.errorurl.append(url)
            return None
        
        finally:
            return self.parse_and_extract(url)
        
    def parse_and_extract(self, url):
        extracted_data = []
        specific_links = []
        others = []

        soup = BeautifulSoup(self.response.text, "html.parser")

        ### Extract all <td> elements
        td_elements = soup.find_all("td", class_="info c1")
        if td_elements == []:
            return None
        
        # Extract data  
        for td in td_elements:
            # Check if the td contains <a> tags (links)
            links = td.find_all("a")
            
            if len(links) != 0:
                
                for link in links:
                    specific_links.append(link["href"])  # Extract link
                if link['href'].startswith("mailto:"):
                    extracted_data.append(link.get_text(strip=True)) # Extract mail_link
                else: 
                    extracted_data.extend([code for code in td.get_text(strip=True).split(",")]) # Extract course_name

            else:
                others.append(td.get_text(strip=True).replace("\xa0", " ")) # Extract others
                
            

        specific_links.insert(1, url) # Insert default link
        outputs = [[specific_link, course_code] for specific_link, course_code in zip(specific_links, extracted_data)]
        outputs += others

        ### Regular expression to extract 'id' value
        match = re.search(r"id=(\d+)", url)
        
        # Extracted id value
        id_value = match.group(1) if match else 0

        ### Extract all <h2> elements with class="main" / Name session
        h2_main = soup.find_all("h2", class_="main")
        
        if len(h2_main) != 1:
            with self.data_lock:
                self.errorurl.append(url)
        else: 
            name = h2_main[0].get_text(strip=True) # Get name
            outputs.append(name)

            with self.data_lock:
                self.students[id_value] = outputs

        return None
    
    def Threading(self):
        # Fetch and extract data from multiple URLs in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(executor.map(self.webpage_access, self.urls))
        
        self.record()
        return None

    def record(self):
        with open("data.txt", "w") as f:
            json.dump(self.students, f, indent=4)

        with open("Error_data.txt", "w") as f:
            json.dump(self.students, f, indent=4)

        return None
ClassName()
input("Completed")
'''
# Step 4: Save or display the data
if response.status_code == 200:
    print("✅ Accessed!")
    with open("data.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("💾 Data saved to 'data.html'")
else:
    print(f"❌ Failed to access data! Status code: {response.status_code}")
'''





"""

def fetch_and_extract(url):
    #Fetches a webpage and extracts the required <td> data.

    extracted_data = []
    specific_links = []
    others = []

    try:
        response = session.get(url)
        response.raise_for_status()  # Raise error for bad response

        soup = BeautifulSoup(response.text, "html.parser")

        ### Extract all <td> elements with class="info c1"
        td_elements = soup.find_all("td", class_="info c1")
        if td_elements == []:
            return None
        
        # Extract data
        for td in td_elements:
            # Check if the td contains <a> tags (links)
            links = td.find_all("a")
            if links:
                for link in links:
                    specific_links.append(link["href"])  # Extract link
                if len(links) == 1:
                    extracted_data.append(td.get_text(strip=True)) # Extract mail_link
                else: 
                    extracted_data.extend([code for code in td.get_text(strip=True).split(",")]) # Extract course_name

            else:
                others.append(td.get_text(strip=True).replace("\xa0", " ")) # Extract others

        specific_links.insert(1, url) # Insert default link
        outputs = [[specific_link, course_code] for specific_link, course_code in zip(specific_links, extracted_data)]
        outputs += others
        #print(outputs)

        ### Regular expression to extract 'id' value
        match = re.search(r"id=(\d+)", url)
        
        # Extracted id value
        id_value = match.group(1) if match else 0
        outputs.append(id_value)

        ### Extract all <h2> elements with class="main" / Name session
        h2_main = soup.find_all("h2", class_="main")

        if len(h2_main) != 1:
            print(h2_main)
            '''Record error value'''
        else: 
            name = h2_main[0].get_text(strip=True) # Get name
            with data_lock:
                Students[name] = outputs

        return None

    except Exception as e:
        return (url, f"Error: {str(e)}")

# Fetch and extract data from multiple URLs in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(fetch_and_extract, urls))
    #print(results)

with open("data.txt", "w") as f:
    json.dump(Students, f, indent=4)

'''
# Print extracted data
for result in results:
    print(result)
'''

"""