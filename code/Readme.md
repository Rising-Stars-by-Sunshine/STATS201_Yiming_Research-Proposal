# Data Querying
  The main part of the data was directly downloaded from
1.	 https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy, which is an open data source sorted by Ansh Tanwar. 
2.	 New data for 2021-2022 from the World Bank https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators

  Additionally, there is also a data query code, which is used for scraping data on the EIA website, including gas consumption and prices in California, USA. As for the process, I first asked ChatGPT to write a general query code for me. And then, I made up the specific headers and API URL; dealt with the OSError, which refers to the proxy problem. The code and pseudo-code are as shown below.
 
  The last sample code might be potentially applied, feel free to check if you are interested!!


### Code
Linke for code in CoLab: https://colab.research.google.com/drive/1GVRQS_lPPvG4PGDtL9XREuSXiEv3eQit?usp=sharing 
```
import csv
import re, time
from requests_html import HTMLSession

session = HTMLSession()

class Demo(object):

    # Input keywords and time range
    q = input('Enter keyword: ')
    start_t = input('Enter start date, e.g., 2023-01-01: ')
    end_t = input('Enter end date, e.g., 2023-01-03: ')

    # Constructing the URL for Weibo search
    url = f'https://s.weibo.com/weibo?q={q}&typeall=1&suball=1&timescope=custom:{start_t}:{end_t}&Refer=g&page='

    # Setting cookie and headers to simulate browser requests
    cookie = 'your cookie information'
    headers = {
        # These headers mimic common browser request headers
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': cookie,
        'referer': 'https://s.weibo.com/weibo?q=%E7%8B%82%E9%A3%99&typeall=1&suball=1&timescope=custom:2022-11-01:2023-02-01&Refer=g&page=2',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    # URL for fetching detailed Weibo data
    data_url = 'https://weibo.com/ajax/statuses/show?id={}'

    # Store already crawled Weibo IDs
    code_all = []

    # Create and open a CSV file for storing data
    w = open(f'{q}.csv', 'a', encoding='utf-8', newline='')
    w = csv.writer(w)
    # Writing the header of the CSV file
    w.writerow(['mid', 'Content', 'Post Location', 'Post Time', 'Likes', 'Reposts', 'Comments'])

    def start(self):
        for i in range(1, 51):  # Loop through the first 50 pages
            new_url = self.url + str(i)
            res = session.get(new_url, headers=self.headers).text  # Send request and get response

            # Use regex to find all Weibo links
            more_urls = re.findall(r'//weibo.com/[0-9]{1,}/.*?[?]refer_flag', res)
            for code in more_urls:
                code = code.split('/')[-1][:-len('?refer_flag')]
                if code not in self.code_all:  # If this ID has not been crawled yet
                    self.code_all.append(code)
                    print(code)
                    time.sleep(2)  # Pause to avoid being blocked

                    # Fetch detailed information of the Weibo
                    data_all = session.get(self.data_url.format(code), headers=self.headers).json()
                    mid = data_all['id']
                    text = data_all['text_raw'].replace('\n', '').replace('\u200b', '')
                    try:
                        place = data_all['region_name']
                    except:
                        place = 'none'
                    t = data_all['created_at']
                    attitudes_count = data_all['attitudes_count']
                    reposts_count = data_all['reposts_count']
                    comments_count = data_all['comments_count']

                    # Write data into CSV file
                    self.w.writerow([mid, text, place, t, attitudes_count, reposts_count, comments_count])
                    print([mid, text, place, t, attitudes_count, reposts_count, comments_count])

if __name__ == '__main__':
    Demo().start()  # Instantiate Demo and start crawling data
```

###  pseudo-code
```
Create a class named Demo

In the Demo class:
1. Prompt user to input keyword, start date, and end date.
2. Construct a search URL using the input keyword and date range.
3. Define headers and cookie for the HTTP requests.

4. Initialize an empty list to store crawled Weibo IDs.
5. Open (or create) a CSV file named after the input keyword.
6. Write header row in the CSV file: ['mid', 'Content', 'Post Location', 'Post Time', 'Likes', 'Reposts', 'Comments'].

Define a method start in the Demo class:
    For each page from 1 to 50:
        a. Construct a new URL by appending the page number to the base search URL.
        b. Make an HTTP GET request to the new URL with the defined headers.
        c. Extract Weibo post IDs using regular expressions from the response.
        d. For each extracted Weibo ID:
            i. If the ID is not already in the list of crawled IDs:
                - Add the ID to the list.
                - Pause for 2 seconds (to prevent blocking).
                - Make an HTTP GET request to fetch detailed data of the Weibo post.
                - Extract data: ID, content, location, time, likes, reposts, comments.
                - Write the extracted data to the CSV file.

When the script is run:
    - Create an instance of the Demo class.
    - Call the start method on the instance.
```

### flowchart
![image](DataQuery.png)


