""" Scraping some data from site 'flashscore' by going through strarting line-ups and collecting the profile link of each player, and then visiting each players profile
    to get their playing time. 'Button-clicking' is used to reveal more matches, which is very important to surf through the site when webscraping.    
    """
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
firefox_options = Options() 
firefox_options.headless = True


# Open the browser
driver=Firefox(options=firefox_options)

# Go to the match line ups
driver.get('https://www.flashscore.gr/match/rwXP4l3L/#/match-summary/lineups')

# Wait till line ups table is fully loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.section:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(3) > strong:nth-child(1)"))
)

# The link of each player's statistics is gonna saved in playerLinks
playerLinks=[]


for j in range(1,3,1):      # j=1 is for home team and j=2 is for away team 

    for i in range(1,12,1): # i runs through each player
       
        link=driver.find_element(By.CSS_SELECTOR,f'.lf__lineUp > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child({j}) > div:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > a:nth-child(3)')

        playerLinks.append(link.get_attribute('href'))

driver.quit()

driver=Firefox(options=firefox_options)

playingTime=[] # This is gonna be the list with all players and their playing time for each of their last 15 matches.

i=0
# Running through each player's link to find their playing time
for link in playerLinks: 
    i+=1
    name=''
    
    driver.get(link) 
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".lmTable"))
    )
    name=driver.find_element(By.CSS_SELECTOR, '.wcl-webTypeHeading02_levdb').text   # Get the player's name
    
    # Only the first time we visit the site we need to reject the cookies.
    if i==1:
        # Some actions to make "More Results" clickable, so that we can get playing time for more than 10 matches, which is the default.
        
        cookie_reject_button_selector = (By.CSS_SELECTOR, '#onetrust-reject-all-handler')
        cookie_reject_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(cookie_reject_button_selector)
        )
        
        # Reject Cookies
        cookie_reject_button.click()
        
    # Wait for the overlay to be clickable and then click it
    overlay_close_button_xpath = "//div[@id='onetrust-group-container']//button[@aria-label='Close']"
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, overlay_close_button_xpath))
        )
        close_button.click()
    except:
        print(f"{i}")

    # Now, attempt to click your original element
    target_element_xpath = "/html/body/div[4]/div[1]/div/div/main/div[6]/div[2]/div[1]/div/div[3]/a"
    target_element = driver.find_element(By.XPATH, target_element_xpath)
    target_element.click()
    

    
    minutesPlayed=[] # A temporary list for each player, which will represent the player row and will be inserted to playingTime list.
    
    minutesPlayed.append(name) 
    
    for i in range(2,16,1):

        # If a player didn't play, insert the string "0'". If the element is not found, it means that the player didn't play in that match.  
        try: 
            driver.find_element(By.CSS_SELECTOR,f'div.lmTable__row:nth-child({i}) > div:nth-child(8) > div:nth-child(2)')
                                                        
            minutesPlayed.append(driver.find_element(By.CSS_SELECTOR,f'div.lmTable__row:nth-child({i}) > div:nth-child(8) > div:nth-child(2)').text)
        except NoSuchElementException:
            
            minutesPlayed.append("0'")
              
    playingTime.append(minutesPlayed)    



driver.quit()

print(playingTime)
df=pd.DataFrame(playingTime)
df.to_csv('PlayingTime.csv')
df.style
