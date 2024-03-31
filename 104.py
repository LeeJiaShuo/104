import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

url = "https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword=%E5%BE%8C%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%AB&mode=s&page=1"

data = pd.DataFrame(columns=["工作", "公司", "工作內容", "技能"])


def geturl(url):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def crawl(url):
    skillall = []
    job = []
    com = []
    workcontent = []
    soup = geturl(url)
    all = soup.find_all(
        "article", class_="b-block--top-bord job-list-item b-clearfix js-job-item"
    )
    workurl = soup.find_all("a", class_="js-job-link")
    for w, j, c in zip(workurl, all, all):
        jobname = j.get("data-job-name")
        company = c.get("data-cust-name")
        work = w.get("href")
        if "hotjob" in work:
            pass
        else:
            skill = []
            job.append(jobname)
            com.append(company)

            jobid = work.split("/")[-1].split("?")[0]

            HEADERS = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36",
                "Referer": f"{url}",
            }

            res = requests.get(
                f"https://www.104.com.tw/job/ajax/content/{jobid}", headers=HEADERS
            )
            a = res.json()

            workcontent.append(a["data"]["jobDetail"]["jobDescription"])

            for i in a["data"]["condition"]["skill"]:
                skill.append(i["description"])
            skillall.append(skill)

    for i in range(len(job)):
        if len(skillall[i]) == 0:
            skillall[i] = "無"
        skillall[i] = ",".join(skillall[i])
        data.loc[i] = (job[i], com[i], workcontent[i], skillall[i])

    return data


crawl(url)
data = data
data.to_csv(f"hw.csv", index=False, encoding="utf-8-sig")
