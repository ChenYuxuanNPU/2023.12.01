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

result_for_period = []
label_for_period = []
data_for_period = []

result_for_area = []
label_for_area = []
data_for_area = []

#教师资格情况统计
count_without_certification = 0
count_all_teacher = 0
count_with_certification = 0

count_all_mid_and_pri = 0
count_without_mid_and_pri = 0
count_all_kindergarten = 0
count_without_kindergarten = 0


#用来设置排序
educational_background_order = {'高中及以下':1,'高中':2,'中专':3,"大学专科":4,"大学本科":5,"硕士研究生":6,"博士研究生":7,None:8}

#用来设置文件名
current_time = datetime.datetime.now().strftime('%Y-%m-%d')
save_path = r".\output\district" + '\\'

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
        c.execute("select count(*),educational_background_highest from " + table_name + " where is_teacher == '是' group by educational_background_highest order by count(*) desc")
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
        c.execute("select count(*) from " + table_name + " where is_teacher == '是' and level_of_teacher_certification == '无'")
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
        c.execute("select count(*) from " + table_name + " where is_teacher == '是'")
        count_all_teacher = c.fetchall()[0][0]

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    #print(count_all_teacher)

    count_with_certification = count_all_teacher - count_without_certification

def certification_and_period():

    global count_all_mid_and_pri
    global count_without_mid_and_pri
    global count_all_kindergarten
    global count_without_kindergarten

    try:
        c.execute("select count(*) from " + table_name + " where is_teacher == '是' and period == '幼儿园'")
        count_all_kindergarten = c.fetchall()[0][0]

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    try:
        c.execute("select count(*) from " + table_name + " where is_teacher == '是' and period == '幼儿园' and level_of_teacher_certification == '无'")
        count_without_kindergarten = c.fetchall()[0][0]

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    try:
        c.execute("select count(*) from " + table_name + " where is_teacher == '是' and period != '幼儿园' and period != '其他'")
        count_all_mid_and_pri = c.fetchall()[0][0]

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    try:
        c.execute("select count(*) from " + table_name + " where is_teacher == '是' and period != '幼儿园' and period != '其他' and level_of_teacher_certification == '无'")
        count_without_mid_and_pri = c.fetchall()[0][0]

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    print("中小学持证人数：" + str(count_all_mid_and_pri - count_without_mid_and_pri),file=file)
    print("中小学未持证人数：" + str(count_without_mid_and_pri),file=file)
    print("中小学总人数：" + str(count_all_mid_and_pri),file=file)
    print("中小学持证百分比：" + str('{:.2%}'.format((count_all_mid_and_pri - count_without_mid_and_pri)/count_all_mid_and_pri)),file=file)

    print("", file=file)

    print("幼儿园持证人数：" + str(count_all_kindergarten - count_without_kindergarten),file=file)
    print("幼儿园未持证人数：" + str(count_without_kindergarten),file=file)
    print("幼儿园总人数：" + str(count_all_kindergarten),file=file)
    print("幼儿园持证百分比：" + str('{:.2%}'.format((count_all_kindergarten - count_without_kindergarten)/count_all_kindergarten)),file=file)

def log_for_certification():
    print("教师资格持证情况：",file=file)

    print("持证人数：" + str(count_with_certification),file=file)
    print("未持证人数：" + str(count_without_certification),file=file)
    print("总人数：" + str(count_all_teacher),file=file)
    print("持证百分比：" + str('{:.2%}'.format(count_with_certification/count_all_teacher)),file=file)

    certification_and_period()


def log_for_period(label,data):
    print("学段统计数据：", file=file)

    print(label)

    print(data)

    for i in range(0, len(data)):
        print(str(label[i]) + ":" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%", file=file)

    print("", file=file)

def figure_for_period():
    global result_for_period
    global label_for_period
    global data_for_period

    try:
        c.execute("select count(*),period from " + table_name + " where is_teacher == '是' and period != '其他' group by period order by case period when '幼儿园' then 1 when '小学' then 2 when '初中' then 3 when '高中' then 4 else 5 end")
        result_for_period = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()

    print(result_for_period)

    for i in range(0,len(result_for_period)):
        data_for_period.append(result_for_period[i][0])
        label_for_period.append(result_for_period[i][1])

    log_for_period(label=label_for_period, data=data_for_period)


def log_for_area(label,data):
    print("片区统计数据：", file=file)

    for i in range(0, len(data)):
        print(str(label[i]) + ":" + str(data[i]) + "人，占比" + str(round(100 * data[i] / sum(data), 1)) + "%", file=file)

    print("", file=file)

def figure_for_area():
    global result_for_area
    global label_for_area
    global data_for_area

    try:
        c.execute("select count(*),area from " + table_name + " where is_teacher == '是' group by area order by count(*)")
        result_for_area = c.fetchall()

    except Exception as e:
        print("执行mysql语句时报错：%s" % e)

    finally:
        conn.commit()


    for i in range(0,len(result_for_area)):
        data_for_area.append(result_for_area[i][0])
        label_for_area.append(result_for_area[i][1])

    log_for_area(label=label_for_area, data=data_for_area)

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
        c.execute(
            "select count(*),cadre_teacher from " + table_name + " where is_teacher == '是' group by cadre_teacher order by case cadre_teacher when '白云区骨干教师' then 1 when '广州市骨干教师' then 2 when '广东省骨干教师' then 3 when '外省市骨干教师' then 4 when '其他' then 5 when '无' then 6 else 7 end")
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



def pre_do():
    figure_for_educational_background()
    without_certification()
    count_all()
    print(count_with_certification)
    print(count_without_certification)

    figure_for_period()

    figure_for_area()

    figure_for_cadre_teacher()

    log_for_certification()

def draw_pyechart_for_district():

    big_title = (
        Pie() # 不画图，只显示一个标题，用来构成大屏的标题
            .set_global_opts(
            title_opts=opts.TitleOpts(title="白云区非编教师信息可视化大屏",title_textstyle_opts=opts.TextStyleOpts(font_size=32),pos_top=10),
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

    pyechart_for_area = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add("", [list(z) for z in zip(label_for_area, data_for_area)],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="片区统计"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                             tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_area.render_notebook()

    pyechart_for_period = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
            .add("", [list(z) for z in zip(label_for_period, data_for_period)],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="学段统计"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                             tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_period.render_notebook()

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

    pyechart_for_certification_mid_and_pri = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add("", [list(z) for z in zip(["持有教资","未持教资"], [count_all_mid_and_pri - count_without_mid_and_pri,count_without_mid_and_pri])],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="中小学教资统计"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                             tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_certification_mid_and_pri.render_notebook()

    pyechart_for_certification_kindergarten = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add("", [list(z) for z in zip(["持有教资","未持教资"], [count_all_kindergarten - count_without_kindergarten,count_without_kindergarten])],
                 center=["50%", "60%"], radius="65%")
            .set_global_opts(title_opts=opts.TitleOpts(title="幼儿园教资统计"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%"))
        #.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c},占比{d}%"),tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c} ({d}%)"))
    )
    pyechart_for_certification_kindergarten.render_notebook()

    page = Page()
    page.add(
        big_title,
        pyechart_for_area,
        pyechart_for_period,
        pyechart_for_educational_background,
        pyechart_for_cadre_teacher,
        pyechart_for_certification_overall,
        pyechart_for_certification_mid_and_pri,
        pyechart_for_certification_kindergarten
    )

    page.render(save_path + '\\page.html')

    with open(save_path + "\\page.html", "r+", encoding='utf-8') as html:
        html_bf = BeautifulSoup(html, 'html.parser')
        divs = html_bf.select('.chart-container') # 根据css定位标签，选中图像的父节点标签

        #全区信息的样式
        divs[0]["style"] = "width:50%;height:30%;position:absolute;top:0%;left:36.5%;border-style:dashed;border-color:#89641;border-width:0px;"
        divs[1]["style"] = "width:47%;height:45%;position:absolute;top:10%;left:3%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[2]["style"] = "width:47%;height:45%;position:absolute;top:10%;left:50%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[3]["style"] = "width:47%;height:45%;position:absolute;top:55%;left:3%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[4]["style"] = "width:47%;height:45%;position:absolute;top:55%;left:50%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[5]["style"] = "width:33%;height:45%;position:absolute;top:105%;left:0%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[6]["style"] = "width:33%;height:45%;position:absolute;top:105%;left:33%;border-style:solid;border-color:#ffffff;border-width:2px;"
        divs[7]["style"] = "width:33%;height:45%;position:absolute;top:105%;left:66%;border-style:solid;border-color:#ffffff;border-width:2px;"

        body = html_bf.find("body") # 根据标签名称定位到body标签
        body["style"] = "background-color:#ffffff;" # 修改背景颜色
        html_new = str(html_bf) # 将BeautifulSoup对象转换为字符
        html.seek(0, 0) # 光标移动至
        html.truncate() # 删除光标后的所有字符内容
        html.write(html_new) # 将由BeautifulSoup对象转换得到的字符重新写入html文件
        html.close()

if __name__ == '__main__':

    os.system(r'python .\update_database.py')

    if(os.path.exists(save_path + "doc.txt")):
        os.remove(save_path + "doc.txt")

    # 用来连接数据库
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    with open(save_path + "doc.txt" , mode = "w" , encoding="utf-8") as file:
        pre_do()

        draw_pyechart_for_district()

