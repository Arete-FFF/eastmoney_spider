from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_country_data(driver):
    urlList = [
        "https://data.eastmoney.com/cjsj/ppi.html",
        "https://data.eastmoney.com/cjsj/cpi.html",
        "https://data.eastmoney.com/cjsj/gyzjz.html",
    ]
    tableHeaders = [
        ["月份", "当月", "当月同比增长", "累计"],
        [
            "月份",
            "当月",
            "同比增长",
            "环比增长",
            "累计",
            "当月",
            "同比增长",
            "环比增长",
            "累计",
            "当月",
            "同比增长",
            "环比增长",
            "累计",
        ],
        ["月份", "同比增长", "累计增长"],
    ]
    for url, headers in zip(urlList, tableHeaders):
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="cjsj_table"]/table/tbody')
            )
        )
        pageSize = driver.find_element(
            By.XPATH, '//*[@id="cjsj_table_pager"]/div[1]/a[7]'
        ).text
        all_data = []
        for _ in range(int(pageSize) - 1):
            table = driver.find_element(By.XPATH, '//*[@id="cjsj_table"]/table/tbody')
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cols = [ele.text for ele in row.find_elements(By.TAG_NAME, "td")]
                all_data.append(cols)
            next_page = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="cjsj_table_pager"]/div[1]/a[contains(text(),"下一页")]',
                    )
                )
            )
            if next_page.is_displayed():
                next_page.click()
            sleep(2)
        df = pd.DataFrame(all_data, columns=headers)
        df.to_csv("out/cn_{}.csv".format(url.split("/")[-1]), index=False)


if __name__ == "__main__":
    edge_driver_path = "/Users/arete/DevTools/mesdgedriver/mesdgedriver"
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service)
    get_country_data(driver)
    driver.quit()


# db = mysql.connect(host="localhost", user="root", passwd="", database="testdb2")
# cursor = db.cursor()
# query = "insert into stocks (symbol, name, new, chg_rate, change_value, vol, amount, amplitude, high, low, open, prev_close, qrr, turnover_rate, pe, pb) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

# url = "http://quote.eastmoney.com/center/gridlist.html#sh_a_board"
# driver = webdriver.Chrome("D:\python\爬虫\chromedriver.exe")
# driver.get(url)
# sleep(5)

# for page_num in range(1, 81):
#     for i in range(1, 11):
#         for ele_type in ["odd", "even"]:
#             stock_dict = {}
#             number_list = [
#                 "2",
#                 "3",
#                 "5",
#                 "6",
#                 "7",
#                 "8",
#                 "9",
#                 "10",
#                 "11",
#                 "12",
#                 "13",
#                 "14",
#                 "15",
#                 "16",
#                 "17",
#                 "18",
#             ]
#             ele_list = [
#                 "代码",
#                 "名称",
#                 "最新价",
#                 "涨跌幅",
#                 "涨跌额",
#                 "成交量",
#                 "成交额",
#                 "振幅",
#                 "最高价",
#                 "最低价",
#                 "今开",
#                 "昨收",
#                 "量比",
#                 "换手率",
#                 "市盈率",
#                 "市净率",
#             ]
#             for j, name in zip(number_list, ele_list):
#                 temp_xpath = "/html/body/div[@class='page-wrapper']/div[@id='page-body']/div[@id='body-main']/div[@id='table_wrapper']/div[@class='listview full']/table[@id='table_wrapper-table']/tbody/tr[@class='{}'][{}]/td[{}]".format(
#                     ele_type, i, j
#                 )
#                 stock_dict[name] = extractor(temp_xpath)
#             print(list(stock_dict.values()))
#             cursor.execute(query, list(stock_dict.values()))
#             db.commit()
#             # export_to_file(stock_dict)
#     # 到下一页继续爬
#     driver.find_element_by_xpath(
#         "/html/body/div[@class='page-wrapper']/div[@id='page-body']/div[@id='body-main']/div[@id='table_wrapper']/div[@class='listview full']/div[@class='dataTables_wrapper']/div[@id='main-table_paginate']/a[@class='next paginate_button']"
#     ).click()
#     sleep(1)

# driver.close()
