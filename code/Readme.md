# Data Querying
  Briefly speaking, find a interesting dataset, check the feasibility of research, and then download the dataset.
  
1.	Access: Get into a Kaggle Dataset: https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy 
2.	Check intention: Check what the dataset involves(columns), and what the dataset is used for. See if I am interested in analyzing them and if I do gain some inspiration from them.
3.	Choose data: This comprehensive dataset has 21 columns, check if I need them all, or only part of them. Click on those columns I want.
4.	Download: On the Data site, click on the “Download” button, and then I get the csv file.

#### Code
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

####  pseudo-code
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
