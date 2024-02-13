#1使用高德API获取985大学地理信息
import requests
import csv

universities = []
with open('university.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        universities.append(row)
# 定义请求URL和参数
url = 'https://restapi.amap.com/v3/geocode/geo'
params = {'key': '78aff143c80be095bb0b05b0aa7b606b', 'address': '', 'city': ''}

for university in universities:
    address = university['name']
    params['address'] = address
    response = requests.get(url, params=params)
    result = response.json()
    if result['status'] == '1':
        geocode = result['geocodes'][0]
        university['location'] = geocode['location']
        university['formatted_country'] = geocode['formatted_address'].replace(' ', '')
        university['country'] = geocode['country']
        university['province'] = geocode['province']
        university['city'] = geocode['city']
        university['district'] = geocode['district']
        university['street'] = geocode['street']
        university['number'] = geocode['number']
    else:
        print(f"获取{address}的地理编码信息失败：{result['info']}")
#将结果保存到'university_geocode.csv'文件
header = universities[0].keys()
with open('university_geocode.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(universities)

#2拆分google专利文件
import json
import datetime
import sys

with open("./google100.txt", "r") as f:
    with open('./patent_dates.txt', 'a') as fs:
        fs.write("Filing Date|Publication Date|Grant Date|Priority Date\n")
        for pt in f.readlines():
            patent = json.loads(pt)
            filing_date = patent.get("filing_date", "")
            publication_date = patent.get("publication_date", "")
            grant_date = patent.get("grant_date", "")
            priority_date = patent.get("priority_date", "")

            fs.write(f"{filing_date}|{publication_date}|{grant_date}|{priority_date}\n")

#从google专利文件中拆分出专利的filling date|publication date|grant date|priority date，并将拆分过程写成针对文件的函数，从命令行直接运行，参数为文件名(google100.txt)

import sys
import json
def patent_dates(input_file, output_file):
    with open(input_file, "r") as f:
        with open(output_file, 'a') as fs:
            fs.write("Filing Date|Publication Date|Grant Date|Priority Date\n")
            for pt in f.readlines():
                patent = json.loads(pt)
                filing_date = patent.get("filing_date", "")
                publication_date = patent.get("publication_date", "")
                grant_date = patent.get("grant_date", "")
                priority_date = patent.get("priority_date", "")

                fs.write(f"{filing_date}|{publication_date}|{grant_date}|{priority_date}\n")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = "./google100_patent_dates.txt"
    patent_dates(input_file, output_file)