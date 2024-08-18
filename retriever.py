import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.statsf1.com/en/grands-prix.aspx'

load_dotenv()

headers = {
    'Accept': os.getenv('ACCEPT'),
    'Accept-Language': os.getenv('ACCEPT_LANGUAGE'),
    'Cache-Control': os.getenv('CACHE_CONTROL'),
    'Connection': os.getenv('CONNECTION'),
    'Cookie': os.getenv('COOKIE'),
    'Sec-Fetch-Dest': os.getenv('SEC_FETCH_DEST'),
    'Sec-Fetch-Mode': os.getenv('SEC_FETCH_MODE'),
    'Sec-Fetch-Site': os.getenv('SEC_FETCH_SITE'),
    'Sec-Fetch-User': os.getenv('SEC_FETCH_USER'),
    'Upgrade-Insecure-Requests': os.getenv('UPGRADE_INSECURE_REQUESTS'),
    'User-Agent': os.getenv('USER_AGENT'),
    'sec-ch-ua': os.getenv('SEC_CH_UA'),
    'sec-ch-ua-mobile': os.getenv('SEC_CH_UA_MOBILE'),
    'sec-ch-ua-platform': os.getenv('SEC_CH_UA_PLATFORM')
}

# Send a GET request to the website with headers
response = requests.get(url, headers=headers, allow_redirects=True)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Table containing the Grand Prix data
    table = soup.find('table', {'class': 'sortable'}) 

    # Prepare to store the data
    data = []
    
    # Extract table rows
    rows = table.find_all('tr')
    
    # Loop through the rows (skip the header row)
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=['Grand Prix', 'Number', 'First', 'Last'])

    print(df)

    # Save the DataFrame to a CSV file
    # df.to_csv('grand_prix_data.csv', index=False)

    print("Data saved to grand_prix_data.csv")
else:
    print(f"Failed to retrieve data: {response.status_code}")