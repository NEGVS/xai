import json
import time
import requests

import pandas as pd
import pymysql

date_str = time.strftime('%Y%m%d')
base_dir = "/tmp/"


# 设计模型
class QueryModel:
    def __init__(self, query, filename):
        self.query = query
        self.filename = filename
        self.file_dir = base_dir
        self.file_path = self.file_dir + self.filename


# 使用模型的list
queries_models = [
    QueryModel("""
    SELECT orv.project_id, orv.return_visit_type,
CONCAT(orv.project_name) AS 项目名称,
(CASE WHEN MAX(orv.return_visit_type) = 1 THEN '入职首日回访'
                  WHEN MAX(orv.return_visit_type) = 2 THEN '入职三天回访'
                        WHEN MAX(orv.return_visit_type) = 3 THEN '入职十天回访'
ELSE '' END ) AS 回访类型,
COUNT(DISTINCT orv.resume_apply_id) AS 回访总数,
COUNT(DISTINCT IF(orv.`status`=0,orv.resume_apply_id,NULL)) AS 未完成回访数,
COUNT(DISTINCT IF(orv.`status`=1,orv.resume_apply_id,NULL)) AS 已完成回访数,
COUNT(DISTINCT IF(orv.`status`=2,orv.resume_apply_id,NULL)) AS 过期回访数
FROM operater_return_visit orv
LEFT JOIN project p ON p.id=orv.project_id
WHERE
orv.deleted_at IS NULL
AND orv.employed_time > '2023-08-09'
AND orv.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL (DAYOFWEEK(CURRENT_DATE)+1) DAY)
AND orv.created_at < DATE_SUB(CURRENT_DATE, INTERVAL (DAYOFWEEK(CURRENT_DATE) - 6) DAY)
AND orv.project_id NOT IN (153,99)
AND p.type=2 AND p.signed_type=1
GROUP BY orv.project_id, orv.return_visit_type
    """, "每周六回访数据统计%s.xls" % date_str),
    QueryModel("""
SELECT
orv.project_name 项目, orv.user_name 会员,
DATE_FORMAT(orv.employed_time,'%Y-%m-%d') 入职时间,
(CASE WHEN orv.return_visit_type = 1 THEN '入职首日回访'
          WHEN orv.return_visit_type = 2 THEN '入职三天回访'
            WHEN orv.return_visit_type = 3 THEN '入职十天回访'
ELSE '' END ) AS 回访类型,
(CASE WHEN orv.`status` = 0 THEN '未完成回访'
          WHEN orv.`status` = 1 THEN '已完成回访'
            WHEN orv.`status` = 2 THEN '回访过期'
ELSE '' END ) AS 回访状态,
orv.created_at 回访生成时间,
orv.operater_name 回访人,
orv.updated_at 回访任务更新时间,
(SELECT MIN(created_at) FROM follow_up_log WHERE resume_apply_id=orv.resume_apply_id AND operater_id=orv.operater_id AND created_at >= orv.created_at) 已回访时间,
(SELECT GROUP_CONCAT(return_visit_remark) FROM follow_up_log WHERE resume_apply_id=orv.resume_apply_id AND operater_id=orv.operater_id AND created_at >= orv.created_at AND created_at <= orv.updated_at
GROUP BY resume_apply_id
) 回访备注
FROM operater_return_visit orv
LEFT JOIN project p ON p.id=orv.project_id
WHERE orv.deleted_at IS NULL
AND orv.employed_time > '2023-08-09'
AND orv.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL (DAYOFWEEK(CURRENT_DATE)+1) DAY)
AND orv.created_at < DATE_SUB(CURRENT_DATE, INTERVAL (DAYOFWEEK(CURRENT_DATE) - 6) DAY)
AND orv.project_id NOT IN (153,99)
AND p.type=2 AND p.signed_type=1
ORDER BY orv.employed_time
    """, "每周六回访数据明细%s.xls" % date_str),
]

# 1. 连接MySQL数据库
db = pymysql.connect(host="polar-syh-prod-lan.rwlb.rds.aliyuncs.com", user="readonly", password="Us7da88eGYtdQBW3",
                     database="supply_db")
cursor = db.cursor()

# 2. 对于每个模型，执行查询并保存为CSV
for model in queries_models:
    df = pd.read_sql(model.query, db)
    # df.to_csv(model.file_path, index=False)
    df.to_excel(model.file_path, index=False)

# https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8e69a96f-8847-42bc-8d1b-7e2a5d2141c5
bot_key = '8e69a96f-8847-42bc-8d1b-7e2a5d2141c5'

# 2. 对于每个模型，执行查询并保存为xls
for model in queries_models:
    df = pd.read_sql(model.query, db)
    # df.to_csv(model.file_path, index=False)
    df.to_excel(model.file_path, index=False)


def send_file_to_wechat(filename):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + bot_key  # 替换成你的 webhook 地址
    headers = {
        "Content-Type": "application/json"
    }

    # 上传文件到企业微信服务器，并获取media_id
    upload_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=%s&type=file" % bot_key
    with open(filename, 'rb') as f:
        files = {'media': f}
        r = requests.post(upload_url, files=files)
        response_data = r.json()
        if r.status_code == 200 and response_data.get("errcode") == 0:
            media_id = response_data.get("media_id")
        else:
            print(f"上传文件错误: {response_data.get('errmsg')}")
            return

    # 使用获取的media_id发送文件
    data = {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200 and response.json().get("errcode") == 0:
        print("文件上传成功")
    else:
        print(f"Error: {response.json().get('errmsg')}")


for model in queries_models:
    send_file_to_wechat(model.file_path)

# 关闭数据库连接
db.close()

print("发送企微成功")
