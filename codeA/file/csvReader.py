import csv

dates = []
role1 = []
role2 = []
path = '/Users/andy_mac/PycharmProjects/xai/docs/file/Result_21.csv'
path2 = '/Users/andy_mac/PycharmProjects/xai/docs/file/srzp_application_srzon_match_greet_record.csv'
with open(path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dates.append(row["user_id"])
        role1.append(int(row["business_user_id"]))
        role2.append(int(row["job_id"]))
dates.reverse()
role1.reverse()
role2.reverse()
print("dates:", dates)
print("role1:", role1)
print("role2:", role2)
