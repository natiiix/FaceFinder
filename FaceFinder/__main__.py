"""This is the main module of the FaceFinder script."""

import time
import selenium.webdriver

KEY_ENTER = u'\ue007'
KEY_ARROW_RIGHT = u'\ue014'
PAGE_LOAD_SLEEP = 2.0

def main():
    """This is the main function of the FaceFinder script."""

    # Ask the user to enter their Facebook login information and the target's id
    print("Email: ", end="")
    email = input()
    print("Password: ", end="")
    password = input()
    print("Target: ", end="")
    target = input()

    # Open new Firefox window and maximize it
    driver = selenium.webdriver.Firefox()
    driver.get("about:blank")
    driver.maximize_window()

    # Load the Facebook homepage and log in
    driver.get("https://facebook.com")
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id("pass").send_keys(password)
    driver.find_element_by_id("pass").send_keys(KEY_ENTER)
    time.sleep(PAGE_LOAD_SLEEP)

    # Go to the specified person's photos page
    driver.get("https://www.facebook.com/" + target + "/photos")
    time.sleep(PAGE_LOAD_SLEEP)

    # Click the first picture
    driver.find_element_by_class_name("uiMediaThumb").click()
    # Variable used for storing the source URL of the first picture
    # Used to determine if all pictures have been visited (first picture was re-visited)
    first_picture = None

    # Infinite loop that goes through all the pictures
    while True:
        # Wait for the page to load
        time.sleep(PAGE_LOAD_SLEEP)

        # Find the spotlight element
        spotlight = driver.find_element_by_class_name("spotlight")

        # If the spotlight element is not present, try to find a video element
        if spotlight is None or not spotlight.is_displayed():
            spotlight = driver.find_element_by_tag_name("video")

        # Get the source URL of the currently displayed picture
        pic_src = spotlight.get_attribute("src")

        # Store the URL of the first picture
        if first_picture is None:
            first_picture = pic_src
        # Break the infinite loop if the first picture is being seen for the second time
        elif pic_src == first_picture:
            print("All pictures visited!")
            break

        try:
            # Find the tagged location
            location = driver.find_element_by_class_name("withTagItem")
            # If the location information is available
            if location is not None:
                # Print the time and the name of the location
                timestamp = driver.find_element_by_tag_name("abbr").get_attribute("title")
                print(timestamp + " - " + location.text)
        except selenium.common.exceptions.NoSuchElementException:
            pass

        # Move on to the next page
        spotlight.send_keys(KEY_ARROW_RIGHT)

    # The data collection is done
    # Close the browser window and dispose of the web driver
    print("Please wait! Destroying the web driver instance...")
    driver.quit()
    # Wait for user to exit the program
    print("Done! Pretty ENTER to exit...")
    input()

if __name__ == "__main__":
    main()
