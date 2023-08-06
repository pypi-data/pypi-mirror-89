from adnar_scraper.utility.data_loader import DataLoader
from adnar_scraper.utility.selenium_controller import SeleniumController
from adnar_scraper.utility.save_file_controller import SaveFileController
from adnar_scraper.utility.database_controller import DatabaseController

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process, Manager
import time


class MagazineScraper:
    def __init__(self):
        # infinity, page
        self.web_list = {
            "cosmopolitan": {"url": "https://www.cosmopolitan.co.kr/fashion",
                             "pattern": "infinity_with_load_btn",
                             "wrapped_item_xpath": '//app-magazine-depth-item[{}]/ng-component/div/div[1]/div',
                             "article_name_xpath": 'descendant::div[2]/em/a',
                             "load_btn_xpath": '//div[contains(@class, "btn_box_more")]/button',
                             "is_wrapped": True,
                             "initial_num": 1,
                             "page_term": 0},

            "elle": {"url": "https://www.elle.co.kr/fashion",
                     "pattern": "infinity_with_load_btn",
                     "wrapped_item_xpath": '//app-magazine-depth-item[{}]/ng-component/div/div[1]/div',
                     "article_name_xpath": 'descendant::div[2]/em/a',
                     "load_btn_xpath": '//div[contains(@class, "btn_box_more")]/button',
                     "is_wrapped": True,
                     "initial_num": 1,
                     "page_term": 0},

            "marieclaire": {"url": "http://www.marieclairekorea.com/category/fashion/",
                            "pattern": "infinity_with_load_btn",
                            "wrapped_item_xpath": None,
                            "article_name_xpath": '/html/body/div[1]/div[2]/main/div/section/div/div[1]/article[{}]/div[2]/h2/a',
                            "load_btn_xpath": '//div[contains(@class, "fusion-load-more-button")]',
                            "is_wrapped": False,
                            "initial_num": 2,
                            "page_term": 0},

            "thesingle": {"url": "https://m.thesingle.co.kr/SinglesMobile/mobileweb/news_content/news_content.do?fmc_no=599674&fsmc_no=599718&fmc_nm=Fashion&fsmc_nm=shopping",
                          "pattern": "infinity_with_load_btn",
                          "wrapped_item_xpath": "/html/body/div[1]/div[5]/section/div/ul[{}]/li",
                          "article_name_xpath": "descendant::a/span[2]/strong",
                          "load_btn_xpath": "/html/body/div[1]/div[5]/section/a",
                          "is_wrapped": True,
                          "initial_num": 1,
                          "page_term": 1},


            "smlounge": {"url": "https://www.smlounge.co.kr/arena/list/3000000",
                         "pattern": "infinity_with_load_btn",
                         "wrapped_item_xpath": None,
                         "article_name_xpath": "/html/body/section/div[5]/div/div/ul/li[{}]/div[2]/p[2]",
                         "load_btn_xpath": '//*[@id="listMoreArena"]',
                         "is_wrapped": False,
                         "initial_num": 1,
                         "page_term": 0
                         },

            "instyle": {
                "url": "http://www.instylekorea.com/issue/article.asp?sec=004002",
                "pattern": "infinity_with_load_btn",
                "wrapped_item_xpath": None,
                "article_name_xpath": "/html/body/div[3]/div[2]/div[2]/div/ul/li[{}]/div/div/div/h2",
                "load_btn_xpath": '//*[@id="more"]',
                "is_wrapped": False,
                "initial_num": 1,
                "page_term": 0
            },

            "dazed": {"url": "http://kr.dazeddigital.com/article/fashion",
                      "pattern": "infinity_with_load_btn",
                      "wrapped_item_xpath": None,
                      "article_name_xpath": "/html/body/div[3]/div[1]/div/div/div[1]/div[{}]/div/div/a",
                      "load_btn_xpath": '/html/body/div[3]/div[1]/div/div/div[2]/a',
                      "is_wrapped": False,
                      "initial_num": 1,
                      "page_term": 0
                      },


            ##########
            "fahsionn": {"url": "https://www.fashionn.com/board/list_new.php?page=5&table=1023",
                         "pattern": "pagenation"},

            "leonkorea": {"url": "http://www.leonkorea.com/magazine/style",
                          "pattern": "pagenation"},

            "hiphoper": {"url": "http://www.hiphoper.com/magazine",
                         "pattern": "pagenation"},
            "allure": {"url": "http://www.allurekorea.com/category/fashion/",
                       "pattern": "pagenation"},
            "snap": {"url": "http://zine.istyle24.com/Fashion/FashionList.aspx",
                     "pattern": "pagenation"},

            "wkorea": {"url": "http://www.wkorea.com/category/fashion/shopping-fashion/",
                       "pattern": "pagenation"},

            "gq": {"url": "http://www.gqkorea.co.kr/category/style/page/2/",
                   "pattern": "pagenation"},

            "stlyem": {
                "url": "https://stylem.mt.co.kr/",
                "pattern": "pagenation"},

            "vogue": {"url": "http://www.vogue.co.kr/category/fashion/%ec%87%bc%ed%95%91-fashion/",
                      "pattern": "infinity"},
        }

        self.scraper_name = "magazine_scraper"
        self.kind = "local_title"

        self.selenium_controller = SeleniumController()
        self.starting_time = DataLoader.create_file_name()
        self.save_file_controller = SaveFileController(name=self.scraper_name, date_time=self.starting_time,
                                                       kind=self.kind)
        self.database_controller = DatabaseController(selected_database=self.kind)

    def multi_get_data(self, num_of_process, data_list):
        with Manager() as manager:
            data_len_list = manager.list()

            if num_of_process == 2:
                basis = len(data_list) // 2

                process_1 = Process(target=self.get_scrape_method, args=(data_list, 0, basis * 1))
                process_2 = Process(target=self.get_scrape_method, args=(data_list, basis * 1, len(data_list)))

                process_1.start()
                process_2.start()

                process_1.join()
                process_2.join()

    def get_scrape_method(self, magazine_key_list, start_idx, end_idx):
        for magazine_key in magazine_key_list[start_idx:end_idx]:
            if self.web_list[magazine_key]["pattern"] == "infinity_with_load_btn":
                dict_v = self.web_list[magazine_key]

                self.scrape_infinity_with_load_btn(magazine_name=magazine_key, wrapped_item_xpath=dict_v["wrapped_item_xpath"],
                                                   article_name_xpath=dict_v["article_name_xpath"], load_btn_xpath=dict_v["load_btn_xpath"],
                                                   is_wrapped=dict_v["is_wrapped"], initial_num=dict_v["initial_num"],
                                                   page_term=dict_v["page_term"])

    def scrape_infinity_with_load_btn(self, magazine_name, wrapped_item_xpath, article_name_xpath, load_btn_xpath,
                                      is_wrapped, initial_num, page_term):

        driver = self.selenium_controller.get_image_blocked_driver(show_browser=False)
        driver.get(self.web_list[magazine_name]["url"])

        # var for when to stop
        item_loaded = True

        # var for save list
        saved_title_list = []
        save_num = 0

        # var for order managing
        prev_num = initial_num
        prev_list = None
        same_loaded_count = 0

        # count num of item
        num_of_item = 0

        while item_loaded is True:
            # expend error by scaling num of unbreak
            error_occurred_num = 0

            self.selenium_controller.get_to_bottom(driver=driver, scroll_pause_time=0.5)

            if is_wrapped is True:
                try:
                    wrapped_items = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, wrapped_item_xpath.format(prev_num))))

                except Exception as e:
                    wrapped_items = []

                if len(wrapped_items) == 0:
                    error_occurred_num += 1

                    if error_occurred_num > 20:
                        item_loaded = False

                temp_save_list = []

                for item in wrapped_items:
                    article_name = item.find_element_by_xpath(xpath=article_name_xpath).text
                    article_data = {'title': article_name, 'magazine_name': magazine_name}
                    temp_save_list.append(article_data)

                    print(article_name)

                if prev_list != temp_save_list:
                    saved_title_list += temp_save_list
                    prev_list = temp_save_list

                    num_of_item += len(temp_save_list)

                else:
                    same_loaded_count += 1

            else:
                temp_save_list = []
                need_loading = False

                while need_loading is False:
                    try:
                        article_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, article_name_xpath.format(prev_num)))).text
                        print(article_name)

                        article_data = {'title': article_name, 'magazine_name': magazine_name}
                        temp_save_list.append(article_data)

                    except Exception as e:
                        print(e)
                        need_loading = True

                if len(temp_save_list) != 0 and temp_save_list != prev_list:
                    saved_title_list += temp_save_list
                    prev_list = temp_save_list

                    num_of_item += len(temp_save_list)

                else:
                    error_occurred_num += 1

                    if error_occurred_num > 20:
                        item_loaded = False

            try:
                load_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, load_btn_xpath)))
                driver.execute_script("arguments[0].click();", load_btn)
                prev_num += (1 + page_term)

            except:
                try:
                    self.selenium_controller.get_to_bottom(driver=driver, scroll_pause_time=0.5)
                    load_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, load_btn_xpath)))
                    driver.execute_script("arguments[0].click();", load_btn)
                    prev_num += (1 + page_term)
                except:
                    try:
                        self.selenium_controller.get_to_bottom(driver=driver, scroll_pause_time=0.5)
                        load_btn = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, load_btn_xpath)))
                        driver.execute_script("arguments[0].click();", load_btn)
                        prev_num += (1 + page_term)
                    except:
                        pass

            if len(saved_title_list) > 100 or same_loaded_count >= 3:
                self.save_file_controller.save_with_namespace(namespace=magazine_name, data_set=saved_title_list)
                saved_title_list = []

                if same_loaded_count >= 3:
                    break

            print("-" * 50)
            print("Next page Loaded - {} - Num_of_Item : {}".format(magazine_name, num_of_item))

    def scrape_vouge(self):
        magazine_name = "vogue"

        #driver = self.selenium_controller.get_image_blocked_driver()
        driver = self.selenium_controller.get_visual_driver()
        driver.get(self.web_list[magazine_name]["url"])

        #/html/body/div[2]/div[6]/main/div/section/div/div[1]/article[2]/div/div[3]/div[1]/h2/a
        #/html/body/div[2]/div[6]/main/div/section/div/div[1]/article[17]/div/div[3]/div[1]/h2/a
        #/html/body/div[2]/div[6]/main/div/section/div/div[1]/article[63]/div/div[3]/div[1]/h2/a
        #/html/body/div[2]/div[6]/main/div/section/div/div[1]/article[2]/div/div[3]/div[1]/h2/a
        #/html/body/div[2]/div[6]/main/div/section/div/div[1]/article[15]/div/div[3]/div[1]/h2/a
        #/html/body/div[2]/div[6]/main/div/section/div/div[1]/article[13]/div/div[3]/h2/a

        # 1, 14, 28
        # 2, 15, 28

        # 1, 14, 27
        # x / 14 == 1 : pass

        # var for when to stop
        error_occurred = False

        # var for save list
        saved_title_list = []
        save_num = 0

        # var for order managing
        prev_num = 2

        while error_occurred is False:
            self.selenium_controller.get_to_bottom(driver=driver, scroll_pause_time=0.5)

            time.sleep(10)

            self.selenium_controller.get_to_bottom(driver=driver, scroll_pause_time=0.5)

            item_loaded = True

            current_gathered_item = []

            while item_loaded is True:
                try:
                    if prev_num // 14 != 1:
                        article_name = driver.find_element_by_xpath(
                            xpath='/html/body/div[2]/div[6]/main/div/section/div/div[1]/article[{}]/div/div[3]/div[1]/h2/a'.format(prev_num)).text

                        print("{}: {}".format(prev_num, article_name))
                        current_gathered_item.append(article_name)

                    prev_num += 1

                except Exception as e:
                    item_loaded = False
                    print(e)

            if len(current_gathered_item) == 0:
                error_occurred = True

            saved_title_list += current_gathered_item

            print("-" * 50)
            print("Next page Loaded")



if __name__ == "__main__":
    #/html/body/app-root/app-layout/app-category/ng-component/div/div[2]/div/div[2]/app-magazine-depth-item[2]/ng-component/div/div[1]/div[5]/div[2]/em/a
    scraper = MagazineScraper()

    d_list = []

    num_idx = 0

    for k, v in scraper.web_list.items():
        if v['pattern'] == "infinity_with_load_btn":
            d_list.append(k)
            print("{} : {}".format(num_idx, k))

            num_idx += 1

    # 7 일단 오류 : (2,3,4,6) ㄱㅊ (0, 1, 5) >> 1.조기종료의 범위를 엄청나게 늘려야함, try문을 이용해서 EC가 오류를 일으키지 않도록 해야함
    chosen = 6

    #scraper.get_scrape_method(magazine_key_list=d_list, start_idx=chosen, end_idx=chosen+1)
    scraper.multi_get_data(num_of_process=2, data_list=d_list)
    '''
    load_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, load_btn_xpath)))
  File "/home/discoverious/Documents/PycharmProjects/adnar-scraper/venv/lib/python3.6/site-packages/selenium/webdriver/support/wait.py", line 80, in until
    raise TimeoutException(message, screen, stacktrace)
selenium.common.exceptions.TimeoutException: Message: 

or break

    '''




