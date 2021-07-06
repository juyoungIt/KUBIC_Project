# search function by using inverted index
import pymysql
from rank_bm25 import BM25Okapi

def bm25(keyword):
    db = pymysql.connect(
        user='user name here...',
        passwd='password here...',
        host='ip address here...',
        db='database name here...',
        charset='utf8mb4'
    )

    # make cursor for interaction with database
    cursor = db.cursor()

    # make sql statement
    # sql_loadTerms = 'SELECT term FROM inv_index JOIN terms USING (terms_id) WHERE doc_id = (%s);'
    sql_loadTerms = 'SELECT term FROM search_table FORCE INDEX(s_table) WHERE doc_id = %s;'
    sql_candidate = 'SELECT doc_id FROM inv_index JOIN terms USING (terms_id) WHERE term = (%s);'


    # enter the search keyword from the users
    search_word = keyword
    tokenized_search_word = search_word.lower().split(" ")
    # print(tokenized_search_word) - for test

    # load candidate document by using search word
    doc_list = []
    for term in tokenized_search_word:
        val_candidate = term
        cursor.execute(sql_candidate, val_candidate)
        result = [item[0] for item in cursor.fetchall()]  # for formatting
        doc_list.append(list(result))

    # merge document list - for BM25 algorithm
    # if search keyword consist multiple words
    merge_doc_list = []
    for each_doc in doc_list:
        merge_doc_list.extend(each_doc)  # merge the all doc_list
    merge_doc_list = sorted(set(merge_doc_list))  # sort doc_list by using doc_id value

    # use the MB25 algorithm
    tokenized_corpus = []
    for doc_id in merge_doc_list:
        cursor.execute(sql_loadTerms, doc_id)
        tmp = [item[0] for item in cursor.fetchall()]  # for formatting
        tokenized_corpus.append(tmp)

    # give the dataset for BM25 Algorithm
    try:
        bm25 = BM25Okapi(tokenized_corpus)
        search_result = bm25.get_scores(tokenized_search_word)  # load the matching score
        table = {}  # table for doc_id & score
        for idx in range(len(search_result)):
            table[merge_doc_list[idx]] = search_result[idx]

        table = sorted(table.items(), key=lambda x: x[1], reverse=True)  # sort by using value(score)
        table = dict(table)  # convert list to dictionary

        # make the final rank list
        rank_result = []
        for key, value in table.items():
            rank_result.append(key)
    except:
        rank_result = []

    sql_related_term = 'SELECT term, SUM(freq) FROM search_table WHERE term LIKE \'%' + \
                       tokenized_search_word[0] + '%\''
    for i in range(1, len(tokenized_search_word)):
        sql_related_term += ' OR term LIKE \'%' + tokenized_search_word[i] + '%\''
    sql_related_term += 'GROUP BY term ORDER BY SUM(freq) DESC LIMIT 5;'
    cursor.execute(sql_related_term)
    result = [item[0] for item in cursor.fetchall()]

    final_result = []
    for i in result:
        if i not in tokenized_search_word:
            final_result.append(i)

    return rank_result, final_result  # print the rank result
