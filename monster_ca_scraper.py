import json
import requests


def send_request(query, offset, json_file):
    url = "https://services.monster.io/jobs-svx-service/v2/monster/search-jobs/samsearch/en-ca"
    headers = {
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
    'referer': 'https://www.monster.ca/jobs/search?q=QA+Engineer&where=&page=6',
    'accept-language': 'en-US,en;q=0.9',}

    data = '{"jobQuery":{"locations":[{"address":"","country":"ca","radius":{"unit":"km","value":"20"}}],"excludeJobs":[],"companyDisplayNames":[],"query":"QA Engineer"},"offset":20,"pageSize":100,"searchId":"","fingerprintId":"01b67215fbde83ba8bd88ec6fa768a03","jobAdsRequest":{"position":[1,2,3,4,5,6,7,8,9,10],"placement":{"component":"JSR_LIST_VIEW","appName":"monster"}}}'

    response = requests.post(url, headers=headers, data=data)

    job_results = response.json().get("jobResults")
    print(job_results)

    collected = get_data(job_results)

    json.dump(collected, json_file, indent=4, sort_keys=True, ensure_ascii=False)


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
        collected.append(job_data)
    return collected


def save_data():
    with open('saved_jobs.json', 'w') as file:
        send_request("QA Engineer", 0, file)
        # for offset in range(0, 1000, 20):

if __name__ == "__main__":
    save_data()