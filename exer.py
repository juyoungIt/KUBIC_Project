import pymysql
import bm25_module

# keyword set
keyword = '귀순북한'

# BM25
rank_result, final_result = bm25_module.bm25(keyword)

# database connection info
db = pymysql.connect(
        user='user name here...',
        passwd='password here...',
        host='ip address here...',
        db='database name here...',
        charset='utf8mb4'
    )

# find data via rank_result

dataList = []
cursor = db.cursor()
query = "SELECT * FROM doc WHERE title LIKE '%귀순북한동포%';"
cursor.execute(query)
row = cursor.fetchone()
dataList.append(row)


print(dataList)

