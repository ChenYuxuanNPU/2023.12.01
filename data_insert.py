#
#这个文件用来生成c.executemany中的sql语句，并将generation_of_input_data中的数据与语句一起插入数据库中
#不需要单独跑，被update_database调用
#

import sqlite3
import generation_of_input_data

def insert_data(database_name,table_name):

    # 用来连接数据库插入数据
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    # 用来生成批量插入的语句
    sentence_for_executemany = ""  # 用来放很多问号
    print("import来的数据长度为：" + str(len(generation_of_input_data.result[0])) + "（来自data_insert）")

    #print(len(generation_of_input_data.result[0]) - 1)
    for _ in range(0, len(generation_of_input_data.result[0]) - 1):
        sentence_for_executemany = sentence_for_executemany + "? , "
    sentence_for_executemany = sentence_for_executemany + "?"

    sql_sentence = "insert into " + table_name + " values ( " + sentence_for_executemany + " )"

    # 插入数据
    try:
        # 插入数据
        c.executemany(sql_sentence, generation_of_input_data.result)

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()
        conn.close()
        print("数据插入成功" + "（来自data_insert）")
