import csv

dates = []
role1 = []
role2 = []
path2 = '/Users/andy_mac/PycharmProjects/xai/docs/file/srzp_application_ai_chat_task.csv'
with open(path2, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dates.append(row["userId"])
print("dates:", dates)
print("dates:", len(dates))
