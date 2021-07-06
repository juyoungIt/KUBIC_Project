import pymysql


def search(keyword):
    # database connection information
    db = pymysql.connect(
        user='user name here...',
        passwd='password here...',
        host='ip address here...',
        db='database name here...',
        charset='utf8mb4'
    )

    # make cursor for interaction with database
    cursor = db.cursor()

    # enter the search keyword from the users
    inst_search_word = keyword

    # for institution search
    sql_inst_search = "SELECT doc_id FROM doc JOIN institution USING (inst_id) WHERE inst_name = '" + inst_search_word + "'ORDER BY title"
    cursor.execute(sql_inst_search)
    inst_result = [item[0] for item in cursor.fetchall()]

    return inst_result
