#用来获取文档中的内容并更新数据库
#不需要单独跑，在生成图片的figure_output_district中被调用

import sqlite3
import os
import data_insert
import generation_of_database

#设定数据库与表名
database_name = "202312.db"
table_name = "teacher_info"

if __name__ == '__main__':
    #main函数里的内容不会被调用就直接运行
    print("正在更新数据库（来自update_database）")

    #删除旧数据库
    if(os.path.exists(r".\\" + database_name)):
        os.remove(r".\\" + database_name)

    # 用来连接数据库
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    #创建新的数据表并规定字段
    generation_of_database.create_table(database_name = database_name,table_name = table_name)
    print("数据表创建成功！（来自update_database）")

    #将表格中数据插入数据库中
    data_insert.insert_data(database_name = database_name,table_name = table_name)

    print("")