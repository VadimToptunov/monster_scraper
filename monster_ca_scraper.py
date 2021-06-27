from datetime import datetime
import json
import requests

URL = "https://services.monster.io/jobs-svx-service/v2/monster/search-jobs/samsearch/en-ca"
HEADERS = {
    'authority': 'services.monster.io',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://www.monster.ca',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.monster.ca/',
    'accept-language': 'en-US,en;q=0.9',
    }

MIN_OFFSET = 0
MAX_OFFSET = 1000
STEP = 30


def send_request(query, offset, json_file):

    data = inject_query(query, offset)

    session = requests.Session()
    response = session.post(URL, headers=HEADERS, data=data)
    job_results = response.json().get("jobResults")
    collected = get_data(job_results)
    json.dump(collected, json_file, indent=4, sort_keys=True, ensure_ascii=False)


def inject_query(query, offset):
    body = {"jobQuery":{"locations":[{"address":"","country":"ca","radius":{"unit":"km","value":"20"}}],"excludeJobs":[],"companyDisplayNames":[],"query":"QA Engineer"},"offset":20,"pageSize":100,"searchId":"","fingerprintId":"01b67215fbde83ba8bd88ec6fa768a03","jobAdsRequest":{"position":[1,2,3,4,5,6,7,8,9,10],"placement":{"component":"JSR_LIST_VIEW","appName":"monster"}}}
    body["jobQuery"]["query"] = query 
    body["offset"] = offset
    return json.dumps(body)

def get_data(job_results):
    collected = []
    for result in job_results:
        posting = result.get("jobPosting")
        application = result.get("apply")
        titles = result.get("enrichments").get("normalizedTitles")[0]
        url = posting.get("url")
        recency = result.get("dateRecency")
        date_posted = result.get("formattedDate")
        company = posting.get("hiringOrganization").get("name")
        job_data = {
        'url' : url,
        'date' : date_posted,
        'recency' : recency,
        'company' : company,
        'applyUrl' : application.get("applyUrl"),
        'title' : titles.get("title")
        }

        if recency == 'Today' or recency == '1 day ago' or recency == '2 days ago':
            collected.append(job_data)
    return collected


def save_data(query):
    filename = str(datetime.date(datetime.now())) + '.json'
    with open(filename, 'w+') as file:
        for offset in range(MIN_OFFSET, MAX_OFFSET, STEP):
            send_request(query, offset, file)
            print("Processing vacancies")

if __name__ == "__main__":
    query = input("Insert profession to find: ")
    save_data(query)