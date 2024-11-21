#encoding=utf-8

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import os
import datetime
import shutil
import gc
import update_database
import generation_of_input_data
import pyecharts
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Page
from bs4 import BeautifulSoup
from pyecharts.globals import ThemeType

#设置字体为楷体
#matplotlib.rcParams['font.sans-serif'] = ['KaiTi']

#设定数据库与表名
database_name = update_database.database_name
table_name = update_database.table_name

#用全局变量保存查数据库的结果，避免多次查询
result_for_educational_background = []
label_for_educational_background = []
data_for_educational_background = []

result_for_cadre_teacher = []
label_for_cadre_teacher = []
data_for_cadre_teacher = []

result_for_highest_title = []
label_for_highest_title = []
data_for_highest_title = []


#教师资格情况统计
count_without_certification = 0
count_all_teacher = 0
count_with_certification = 0


school_list = ["广州市实验外语学校"]
school_name = "广州市实验外语学校"#广州市实验外语学校、广州市源雅学校

period = "高中"#这里只能填一个学段


#用来设置排序
educational_background_order = {'高中及以下':1,'高中':2,'中专':3,"大学专科":4,"大学本科":5,"硕士研究生":6,"博士研究生":7,None:8}

#用来设置文件名
current_time = datetime.datetime.now().strftime('%Y-%m-%d')
save_path = r".\output\school" + '\\'

#统计学历

def log_for_educational_background(label,data):
    print("学历统计数据：",file=file)

    for i in range(0,len(data)):
        print(str(label[i]) + ":" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data),1)) + "%",file=file)

    print("",file=file)

def figure_for_educational_background():

    global result_for_educational_background
    global label_for_educational_background
    global data_for_educational_background

    try:
        if period == "":
            c.execute("select count(*),educational_background_highest from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "' group by educational_background_highest order by count(*) desc")
            result_for_educational_background = c.fetchall()
        else:
            c.execute("select count(*),educational_background_highest from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "' and period == '" + period + "' group by educational_background_highest order by count(*) desc")
            result_for_educational_background = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    result_for_educational_background = sorted(result_for_educational_background,key=lambda x: educational_background_order[x[1]])

    print(result_for_educational_background)

    data_for_educational_background = []
    label_for_educational_background = []
    for single_data in result_for_educational_background:
        if(single_data[1] != None and single_data[1] != "无"):
            label_for_educational_background.append(single_data[1])
            data_for_educational_background.append(single_data[0])


    log_for_educational_background(label=label_for_educational_background,data=data_for_educational_background)


def without_certification():
    global count_without_certification

    try:
        if period == "":
            c.execute("select count(*) from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "' and level_of_teacher_certification == '无'")
            count_without_certification = c.fetchall()[0][0]

        else:
            c.execute(
                "select count(*) from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "' and level_of_teacher_certification == '无' and period == '" + period + "'")
            count_without_certification = c.fetchall()[0][0]

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    #print(count_without_certification)

def count_all():
    global count_all_teacher
    global count_with_certification

    try:
        if(period == ""):
            c.execute("select count(*) from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "'")
            count_all_teacher = c.fetchall()[0][0]
        else:
            c.execute(
                "select count(*) from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "' and period == '" + period + "'")
            count_all_teacher = c.fetchall()[0][0]

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    #print(count_all_teacher)

    count_with_certification = count_all_teacher - count_without_certification


def log_for_certification():
    print("教师资格持证情况：",file=file)

    print("持证人数：" + str(count_with_certification),file=file)
    print("未持证人数：" + str(count_without_certification),file=file)
    print("总人数：" + str(count_all_teacher),file=file)
    print("持证百分比：" + str('{:.2%}'.format(count_with_certification/count_all_teacher)),file=file)
    print("",file=file)


def log_for_cadre_teacher(label,data):
    print("骨干教师统计数据：", file=file)

    for i in range(0, len(data)):
        print(str(label[i]) + ":" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%", file=file)

    print("", file=file)


def figure_for_cadre_teacher():

    global result_for_cadre_teacher
    global label_for_cadre_teacher
    global data_for_cadre_teacher

    try:
        if(period == ""):
            c.execute(
                "select count(*),cadre_teacher from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "' group by cadre_teacher order by case cadre_teacher when '白云区骨干教师' then 1 when '广州市骨干教师' then 2 when '广东省骨干教师' then 3 when '外省市骨干教师' then 4 when '其他' then 5 when '无' then 6 else 7 end")
            result_for_cadre_teacher = c.fetchall()

        else:
            c.execute(
                "select count(*),cadre_teacher from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "' and period == '" + period + "' group by cadre_teacher order by case cadre_teacher when '白云区骨干教师' then 1 when '广州市骨干教师' then 2 when '广东省骨干教师' then 3 when '外省市骨干教师' then 4 when '其他' then 5 when '无' then 6 else 7 end")
            result_for_cadre_teacher = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    data_for_cadre_teacher = []
    label_for_cadre_teacher = []
    for single_data in result_for_cadre_teacher:
        if (single_data[1] != None):
            label_for_cadre_teacher.append(single_data[1])
            data_for_cadre_teacher.append(single_data[0])

    log_for_cadre_teacher(label=label_for_cadre_teacher,data=data_for_cadre_teacher)

    print(data_for_cadre_teacher)
    print(label_for_cadre_teacher)


def log_for_highest_title(label,data):
    print("职称统计情况：",file=file)

    for i in range(0,len(label)):
        print(label[i] + "：" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%",file=file)

    print("",file=file)


def figure_for_highest_title():

    global result_for_highest_title
    global label_for_highest_title
    global data_for_highest_title

    try:
        if(period == ""):
            c.execute(
                "select count(*),highest_title from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "' group by highest_title order by case highest_title when '三级教师' then 1 when '二级教师' then 2 when '一级教师' then 3 when '高级教师' then 4 when '正高级教师' then 5 when '未取得职称' then 6 else 7 end")
            result_for_highest_title = c.fetchall()

        else:
            c.execute(
                "select count(*),highest_title from " + table_name + " where is_teacher == '是' and school_name == '" + school_name + "' and period == '" + period + "' group by highest_title order by case highest_title when '三级教师' then 1 when '二级教师' then 2 when '一级教师' then 3 when '高级教师' then 4 when '正高级教师' then 5 when '未取得职称' then 6 else 7 end")
            result_for_highest_title = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    label_for_highest_title = []
    data_for_highest_title = []

    for i in range(0,len(result_for_highest_title)):
        data_for_highest_title.append(result_for_highest_title[i][0])
        label_for_highest_title.append(result_for_highest_title[i][1])

    print(data_for_highest_title)
    print(label_for_highest_title)

    log_for_highest_title(label=label_for_highest_title,data=data_for_highest_title)


def pre_do():
    figure_for_educational_background()

    without_certification()

    count_all()

    figure_for_cadre_teacher()

    log_for_certification()

    figure_for_highest_title()

def draw_pyechart_for_district():

    title = school_name + "非编教师数据大屏" if period == "" else school_name + period + "非编教师数据大屏"

    big_title = (
        Pie() # 不画图，只显示一个标题，用来构成大屏的标题
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title,title_textstyle_opts=opts.TextStyleOpts(font_size=32),pos_top=10),
            legend_opts=opts.LegendOpts(is_show=False)
            )
    )
    big_title.render_notebook()

    pyechart_for_educational_background = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
            .add("", [list(z) for z in zip(label_for_educational_background, data_for_educational_background)],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="最高学历"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                             tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_educational_background.render_notebook()

    pyechart_for_cadre_teacher = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add("", [list(z) for z in zip(label_for_cadre_teacher, data_for_cadre_teacher)],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="骨干教师"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                             tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_cadre_teacher.render_notebook()


    pyechart_for_certification_overall = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
            .add("", [list(z) for z in zip(["持有教资","未持教资"], [count_with_certification,count_without_certification])],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="总教资统计"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                             tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_certification_overall.render_notebook()

    pyechart_for_highest_title = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
            .add("", [list(z) for z in zip(label_for_highest_title,data_for_highest_title)],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="职称统计"),legend_opts=opts.LegendOpts(pos_left='15%'))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        #.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_highest_title.render_notebook()


    page = Page()
    page.add(
        big_title,
        pyechart_for_certification_overall,
        pyechart_for_educational_background,
        pyechart_for_cadre_teacher,
        pyechart_for_highest_title
    )

    html_path = save_path + school_name +'.html' if period == "" else save_path + school_name + "-" + period +'.html'
    page.render(html_path)

    with open(html_path, "r+", encoding='utf-8') as html:
        html_bf = BeautifulSoup(html, 'html.parser')
        divs = html_bf.select('.chart-container') # 根据css定位标签，选中图像的父节点标签

        #全区信息的样式
        divs[0]["style"] = "width:50%;height:30%;position:absolute;top:0%;left:36.5%;border-style:dashed;border-color:#89641;border-width:0px;"
        divs[1]["style"] = "width:47%;height:45%;position:absolute;top:10%;left:3%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[2]["style"] = "width:47%;height:45%;position:absolute;top:10%;left:50%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[3]["style"] = "width:47%;height:45%;position:absolute;top:55%;left:3%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[4]["style"] = "width:47%;height:45%;position:absolute;top:55%;left:50%;border-style:solid;border-color:#ffffff;border-width:2px;"

        body = html_bf.find("body") # 根据标签名称定位到body标签
        body["style"] = "background-color:#ffffff;" # 修改背景颜色
        html_new = str(html_bf) # 将BeautifulSoup对象转换为字符
        html.seek(0, 0) # 光标移动至
        html.truncate() # 删除光标后的所有字符内容
        html.write(html_new) # 将由BeautifulSoup对象转换得到的字符重新写入html文件
        html.close()

def reset_variable():

    global result_for_educational_background
    global label_for_educational_background
    global data_for_educational_background

    global result_for_cadre_teacher
    global label_for_cadre_teacher
    global data_for_cadre_teacher

    global result_for_period
    global label_for_period
    global data_for_period

    global result_for_area
    global label_for_area
    global data_for_area

    global count_without_certification
    global count_all_teacher
    global count_with_certification


    result_for_educational_background = []
    label_for_educational_background = []
    data_for_educational_background = []

    result_for_cadre_teacher = []
    label_for_cadre_teacher = []
    data_for_cadre_teacher = []

    result_for_highest_title = []
    label_for_highest_title = []
    data_for_highest_title = []

    # 教师资格情况统计
    count_without_certification = 0
    count_all_teacher = 0
    count_with_certification = 0

if __name__ == '__main__':

    os.system(r'python .\update_database.py')

    for school in school_list:
        school_name = school

        txt_path = save_path + school_name + ".txt" if period == "" else save_path + school_name + "-" + period +".txt"

        if(os.path.exists(txt_path)):
            os.remove(txt_path)

        # 用来连接数据库
        conn = sqlite3.connect(database_name)
        c = conn.cursor()

        with open(txt_path, mode = "w" , encoding="utf-8") as file:
            pre_do()

            draw_pyechart_for_district()

            reset_variable()

        conn.close()