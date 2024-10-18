from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up the Firefox driver
driver = Firefox()

# Open the page
driver.get('https://fbref.com/en/comps/20/passing/Bundesliga-Stats')

# Wait for the table to load fully
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#div_stats_passing"))
)

# Extracting header titles (1st row)
headTitles=[]
for i in range(1, 10):
    header = driver.find_element(By.CSS_SELECTOR, f'#stats_passing > thead:nth-child(3) > tr:nth-child(1) > th:nth-child({i})')
    headTitles.append(header.text)                   
    if header.text=='':
         headTitles[i-1]='BLANK_SPACE'
    
driver.quit()

#Here we print the titles with duplicates
print("HeadTitles: ", headTitles) 

#Here we remove duplicates and print the headTitles
headTitles = list(dict.fromkeys(headTitles))
print(headTitles)


#Setting up the Firefox driver again
driver = Firefox()

# Open the page
driver.get('https://fbref.com/en/comps/20/passing/Bundesliga-Stats')

# Wait for the table to load fully
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#div_stats_passing"))
)

#Extracting subhead titles (2nd row)
subHeadTitles=[]
for i in range(1,33,1):
    subhead=driver.find_element(By.CSS_SELECTOR,f' #stats_passing > thead:nth-child(3) > tr:nth-child(2) > th:nth-child({i})')
                                       
    subHeadTitles.append(subhead.text)

driver.quit()

#Printing the subhead titles
print(subHeadTitles)


#Setting up Firefox driver again
driver = Firefox()

# Open the page
driver.get('https://fbref.com/en/comps/20/passing/Bundesliga-Stats')

# Wait for the table to load fully
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#div_stats_passing"))
)

#Extracting all data from the table
datarow=[]

#Running through all the rows
for j in range(1,395):
  
  #With this condition, we avoid extracting some rows of the table, which are useless.
  #Specifically, these rows contain the same subhead titles we extracted before.
  if not j%26:
      continue 
  
  rowdata=[]
  #Running through columns to extract from each row the data.
  for i in range(2,33):
    data=driver.find_element(By.CSS_SELECTOR,f'#stats_passing > tbody:nth-child(4) > tr:nth-child({j}) > td:nth-child({i})')
    
    #We append each data we extract to the row that it belongs
    rowdata.append(data.text)

   #Appending the whole data-row to final list of data-rows
  datarow.append(rowdata)                     

driver.quit()

#Here we create a list of tuples of the form (headTitle,subHeadTitle), so that we can create a dataframe in which every subhead title is below its corresponding 
# head title. Variable Titloi is going to be the list of tuples.

Titloi=[]
i=0
for title in subHeadTitles:
    
    
        if i==0:
            Titloi.append(('',title))
            
        elif i==1:
           Titloi.append((headTitles[i],title))
        elif i==2:
           Titloi.append((headTitles[i],title))
        elif i==3:
           Titloi.append((headTitles[i],title))
        elif i==4:
           Titloi.append((headTitles[i],title))
        elif i==5 or i==6 or i==7:
           Titloi.append((headTitles[5],title))     
        if title=='90s':
            i+=1
            continue
        elif title=='PrgDist' and i<=1:
            i+=1
            continue
        elif title=='Cmp%' and i>=2:
            i+=1
            continue

print(Titloi)   



#Here we fix some data that ara passed as empty attributes inside the dataframe. Instead, they take the string value: '0'.

for data in datarow:
    i=0
    for data1 in data:
        if data1=='':
            data[i]='0'
        i+=1

#We drop some data that we don't want to appear in the dataframe
extracted_data = [datar[:30] for datar in datarow]

#We create the dataframe with the data we extracted, except some data that we dropped, and we use the MultiIndex.from_tuples method to create the columns as we wanted.
df=pd.DataFrame(extracted_data,columns=pd.MultiIndex.from_tuples(Titloi[1:31]))



#From the column 'Nation', we delete some useless lowercase characters from each cell.

for word in df[('','Nation')]:
   result= ''.join([char for char in word if not char.islower()] )
   
   df[('','Nation')][df[('','Nation')]==word]=result



#Creating a csv file with this table of data.
df.to_csv('BundesligaPassingStats1.csv')

#Printing the table.
df.style
