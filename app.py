from flask import Flask, render_template, request
import pymysql
import bm25_module
import inst_search
import writer_search
from operator import itemgetter

app = Flask(__name__)

results_per_page = 5  # number of results per result page

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#BM25 applied
@app.route('/results', methods=['GET'])
def results():

    # keyword set
    keyword = request.args.get('q')
    page = request.args.get('p', 1, type=int)
    sort = request.args.get('sort')
    category = request.args.get('c')

    # 정렬
    if sort is None:
        sort = 'rank'

    # 검색 카테고리
    if category is None:
        category = 'default'

    if category == 'author':
        rank_result = writer_search.search(keyword)
        related_result = []

    elif category == 'inst':
        rank_result = inst_search.search(keyword)
        related_result = []

    else:
        # BM25
        rank_result, related_result = bm25_module.bm25(keyword)

    related = related_result

    # database connection info
    db = pymysql.connect(
        user='user name here...',
        passwd='password here...',
        host='ip address here...',
        db='database name here...',
        charset='utf8mb4'
    )

    # find data via rank_result

    cursor = db.cursor()
    dataList = []

    if sort == 'date':
        # 랭킹순
        for doc_id in rank_result:
            query = ("SELECT doc.doc_id, doc.title, doc.date, doc.category, doc.writer, file.file_url, institution.inst_name, "
                     "institution.inst_url FROM doc LEFT JOIN file on doc.doc_id= file.doc_id "
                     "LEFT JOIN institution on doc.inst_id = institution.inst_id WHERE doc.doc_id = (%s);")
            cursor.execute(query, doc_id)
            row = cursor.fetchone()
            dataList.append(row)

            # sort result
            sortList = []
            for i in range(len(dataList)):
                if dataList[i][2] is not None:
                    sortList.append(dataList[i])
            sortList.sort(key=itemgetter(2), reverse=True)

            for i in range(len(dataList)):
                if dataList[i][2] is None:
                    sortList.append(dataList[i])

            dataList = sortList

    else:
        # 최신순
        for doc_id in rank_result:
            query = ("SELECT doc.doc_id, doc.title, doc.date, doc.category, doc.writer, file.file_url, institution.inst_name, "
                     "institution.inst_url FROM doc LEFT JOIN file on doc.doc_id= file.doc_id "
                     "LEFT JOIN institution on doc.inst_id = institution.inst_id WHERE doc.doc_id = (%s);")
            cursor.execute(query, doc_id)
            row = cursor.fetchone()
            dataList.append(row)

    if len(dataList) > 0:
        arr = dataList
    else:
        arr = ''
    '''
    keyword1_txt = keyword + ".txt" # dataList
    keyword2_txt = keyword + "2.txt" # related
    file = open(keyword1_txt, 'w')
    file.write(dataList)
    file = open(keyword2_txt, 'w')
    file.write(related)
    '''
    return render_template('results.html', arr=dataList, p=page, related=related, sort=sort)

@app.route('/detail', methods=['GET'])
def detail():
    doc_id = request.args.get('id')

    db = pymysql.connect(
        user='user name here...',
        passwd='password here...',
        host='ip address here...',
        db='database name here...',
        charset='utf8mb4'
    )

    # find data via rank_result

    cursor = db.cursor()

    query = "SELECT doc.doc_id, doc.title, doc.date, doc.category, doc.writer, file.file_url, institution.inst_name, institution.inst_url, body.body FROM doc LEFT JOIN file on doc.doc_id= file.doc_id LEFT JOIN institution on doc.inst_id = institution.inst_id LEFT JOIN body ON doc.doc_id = body.doc_id WHERE doc.doc_id = (%s)"
    cursor.execute(query, doc_id)
    row = cursor.fetchall()
    data = row[0]

    return render_template('detail.html', data=data)