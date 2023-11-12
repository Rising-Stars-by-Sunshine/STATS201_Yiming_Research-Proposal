# Data Querying
  The main part of the data was directly downloaded from
1.	 https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy, which is an open data source sorted by Ansh Tanwar. 
2.	 New data for 2021-2022 from the World Bank https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators

  Additionally, there is also a data query code, which is used for scraping data on the EIA website, including gas consumption and prices in California, USA. As for the process, I first asked ChatGPT to write a general query code for me. And then, I made up the specific headers and API URL; dealt with the OSError, which refers to the proxy problem. The code and pseudo-code are as shown below.


### Code
```
pip install requests
import requests
import json

url = "https://api.eia.gov/v2/natural-gas/sum/lsum/data/"

headers = {
    'X-Params': json.dumps({
        "frequency": "annual",
        "data": ["value"],
        "facets": {"series": ["N3010CA2", "N3010CA3"]},
        "start": "2013",
        "end": "2023",
        "sort": [{"column": "period", "direction": "desc"}],
        "offset": 0,
        "length": 5000
    })
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parsing the response JSON
    data = response.json()
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")

```

###  pseudo-code
```
DEFINE url AS "https://api.eia.gov/v2/natural-gas/sum/lsum/data/"

DEFINE headers AS MAP OF:
    'X-Params': STRINGIFIED JSON OF:
        "frequency": "annual"
        "data": LIST CONTAINING "value"
        "facets": MAP OF "series": LIST CONTAINING "N3010CA2", "N3010CA3"
        "start": "2013"
        "end": "2023"
        "sort": LIST CONTAINING MAP OF "column": "period", "direction": "desc"
        "offset": 0
        "length": 5000

SEND GET REQUEST to url WITH headers
STORE RESPONSE IN response

IF response status code IS 200 THEN
    PARSE response content AS JSON
    PRINT parsed data
ELSE
    PRINT "Failed to retrieve data: " AND response status code
```


