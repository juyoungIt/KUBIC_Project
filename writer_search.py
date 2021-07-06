import pymysql

def search(keyword):
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
    writer_search_word = keyword

    # for writer search
    sql_writer_search = "SELECT doc_id FROM doc WHERE writer LIKE '%" + writer_search_word + "%' ORDER BY title;"
    cursor.execute(sql_writer_search)
    writer_result = [item[0] for item in cursor.fetchall()]

    return writer_result
