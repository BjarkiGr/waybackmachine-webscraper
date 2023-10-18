import requests
import csv
WAYBACK_API_URL = "http://web.archive.org/cdx/search/cdx"

website = (
    "https://www.eimskip.is/thjonusta/gjaldskrar/"  
)
from_date = "201010"  # start date in YYYYMM format
to_date = "202310"  # end date in YYYYMM format

params = {
    "url": website,
    "from": from_date,
    "to": to_date,
    "output": "json",
    "fl": "timestamp,original",
    "filter": ["statuscode:200"],
    "collapse": "timestamp:8",
}

try:
    response = requests.get(WAYBACK_API_URL, params=params)
    response.raise_for_status()

    data = response.json()

    with open("wayback_data.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["timestamp", "original"])

        for row in data:
            csv_writer.writerow(row)

    print("Data saved to wayback_data.csv")

    for row in data[1:]:
        timestamp, original_url = row
        response = requests.get(
            f"http://web.archive.org/web/{timestamp}/{original_url}"
        )

        if response.status_code == 200:
            yyyymmdd = timestamp[:8]
            with open(f"{yyyymmdd}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
                print(f"Saved {original_url} from {timestamp} to {yyyymmdd}.html")
        else:
            print(f"Failed to retrieve {original_url} from {timestamp}")

except requests.exceptions.RequestException as e:
    print("Error in making the request to Wayback Machine API:", str(e))
except Exception as e:
    print("An unexpected error occurred:", str(e))
