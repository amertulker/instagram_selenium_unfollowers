from selenium import webdriver
import time

# Replace with your Instagram username and password
USERNAME = "your_username"
PASSWORD = "your_password"

# Replace with the path to your chromedriver executable
chromedriver_path = "path/to/chromedriver"

# Initialize a new Chrome browser instance
browser = webdriver.Chrome(chromedriver_path)

# Navigate to the Instagram login page
browser.get("https://www.instagram.com/accounts/login/")
time.sleep(2)

# Enter your login credentials and submit the form
username_field = browser.find_element_by_name("username")
password_field = browser.find_element_by_name("password")
username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)
login_button = browser.find_element_by_xpath('//button[@type="submit"]')
login_button.click()
time.sleep(2)

# Navigate to your Instagram profile page
browser.get("https://www.instagram.com/" + USERNAME + "/")
time.sleep(2)

# Click on the "Following" button to see a list of users you're following
following_button = browser.find_element_by_partial_link_text("following")
following_button.click()
time.sleep(2)

# Get a list of all the users you're following
following_list = browser.find_element_by_xpath("//div[@class='isgrP']")
scroll_height = 0
while True:
    browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', following_list)
    time.sleep(1)
    new_height = browser.execute_script('return arguments[0].scrollHeight', following_list)
    if new_height == scroll_height:
        break
    scroll_height = new_height
following_links = following_list.find_elements_by_tag_name('a')
following_usernames = [link.text for link in following_links if link.text != '']

# Click on the "Followers" button to see a list of users who are following you
followers_button = browser.find_element_by_partial_link_text("followers")
followers_button.click()
time.sleep(2)

# Get a list of all the users who are following you
followers_list = browser.find_element_by_xpath("//div[@class='isgrP']")
scroll_height = 0
while True:
    browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_list)
    time.sleep(1)
    new_height = browser.execute_script('return arguments[0].scrollHeight', followers_list)
    if new_height == scroll_height:
        break
    scroll_height = new_height
followers_links = followers_list.find_elements_by_tag_name('a')
followers_usernames = [link.text for link in followers_links if link.text != '']

# Unfollow users who are not following you back
for username in following_usernames:
    if username not in followers_usernames:
        browser.get("https://www.instagram.com/" + username + "/")
        time.sleep(2)
        unfollow_button = browser.find_element_by_xpath("//button[text()='Following']")
        unfollow_button.click()
        time.sleep(2)
        confirm_unfollow_button = browser.find_element_by_xpath("//button[text()='Unfollow']")
        confirm_unfollow_button.click()
        time.sleep(2)

# Close the browser window
browser.quit()
