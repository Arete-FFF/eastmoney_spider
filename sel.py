from selenium import webdriver
from time import sleep
import mysql.connector as mysql

"""爬取上证指数的所有股票信息，保存到本地文件/数据库"""


def extractor(xpath_text):
    """根据xpath获取内容"""
    TCases = driver.find_element_by_xpath(xpath_text)
    return TCases.text


def export_to_file(stock_dict):
    """导出股票数据"""
    with open("沪指股票数据.csv", "a", encoding="gbk") as file:
        file.write(",".join(stock_dict.values()))
        file.write("\n")


db = mysql.connect(host="localhost", user="root", passwd="", database="testdb2")
cursor = db.cursor()
query = "insert into stocks (symbol, name, new, chg_rate, change_value, vol, amount, amplitude, high, low, open, prev_close, qrr, turnover_rate, pe, pb) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

url = "http://quote.eastmoney.com/center/gridlist.html#sh_a_board"
driver = webdriver.Chrome("D:\python\爬虫\chromedriver.exe")
driver.get(url)
sleep(5)

for page_num in range(1, 81):
    for i in range(1, 11):
        for ele_type in ["odd", "even"]:
            stock_dict = {}
            number_list = [
                "2",
                "3",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
            ]
            ele_list = [
                "代码",
                "名称",
                "最新价",
                "涨跌幅",
                "涨跌额",
                "成交量",
                "成交额",
                "振幅",
                "最高价",
                "最低价",
                "今开",
                "昨收",
                "量比",
                "换手率",
                "市盈率",
                "市净率",
            ]
            for j, name in zip(number_list, ele_list):
                temp_xpath = "/html/body/div[@class='page-wrapper']/div[@id='page-body']/div[@id='body-main']/div[@id='table_wrapper']/div[@class='listview full']/table[@id='table_wrapper-table']/tbody/tr[@class='{}'][{}]/td[{}]".format(
                    ele_type, i, j
                )
                stock_dict[name] = extractor(temp_xpath)
            print(list(stock_dict.values()))
            cursor.execute(query, list(stock_dict.values()))
            db.commit()
            # export_to_file(stock_dict)
    # 到下一页继续爬
    driver.find_element_by_xpath(
        "/html/body/div[@class='page-wrapper']/div[@id='page-body']/div[@id='body-main']/div[@id='table_wrapper']/div[@class='listview full']/div[@class='dataTables_wrapper']/div[@id='main-table_paginate']/a[@class='next paginate_button']"
    ).click()
    sleep(1)

driver.close()
