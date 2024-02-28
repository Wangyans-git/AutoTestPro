from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class ExecuteOta(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(300)

        self.driver.get(url="https://app.slack.com/workspace-signin?redir=%2Fgantry%2Fauth%3Fapp%3Dclient%26lc%3D163896"
                            "8525%26return_to%3D%252Fclient%252FT4MJC3XG8%252FC4MJC421W%26teams%3D")

        self.driver.find_element(By.ID, "domain").send_keys("skybellhq.slack.com")
        self.driver.find_element(By.XPATH, "//*[text()='继续']").click()

        self.driver.find_element(By.ID, "email").send_keys("charles.chan@d-3.com.hk")
        self.driver.find_element(By.ID, "password").send_keys("d3d3d3d3")
        self.driver.find_element(By.ID, "signin_btn").click()
        time.sleep(10)

        # 记录第一台设备FW A->B的次数
        self.device_one_a = 0
        self.device_one_b = 0
        # 记录第二台设备FW A->B的次数
        self.device_two_a = 0
        self.device_two_b = 0
        # 记录第三台设备FW A->B的次数
        self.device_three_a = 0
        self.device_three_b = 0
        # 记录第四台设备FW A->B的次数
        self.device_four_a = 0
        self.device_four_b = 0
        # 记录第四台设备FW A->B的次数
        self.device_five_a = 0
        self.device_five_b = 0

        print("###############录入需要升级的设备信息###############")
        # 设备1
        self.device_sn_one = input("输入要升级的设备SN①:")
        self.device_id_one = input("输入要升级的设备id①:")
        # 设备2
        self.device_sn_two = input("输入要升级的设备SN②:")
        self.device_id_two = input("输入要升级的设备id②:")
        # 设备3
        self.device_sn_three = input("输入要升级的设备SN③:")
        self.device_id_three = input("输入要升级的设备id③:")
        # 设备4
        self.device_sn_four = input("输入要升级的设备SN④:")
        self.device_id_four = input("输入要升级的设备id④:")
        # 设备5
        self.device_sn_five = input("输入要升级的设备SN⑤:")
        self.device_id_five = input("输入要升级的设备id⑤:")

        # 需要升级的版本id   A->B
        print("###############录入需要升级的版本信息###############")
        self.update_version_a = input("输入要升级的版本号 A：")
        self.update_version_id_a = input("输入要升级的版本id A：")
        self.update_version_b = input("输入要升级的版本号 B：")
        self.update_version_id_b = input("输入要升级的版本id B：")

    def run_trim2(self):

        """
        v8087 60c8af03e1b99f3f33bdff86
        v8088 612645909d200bf8e4ab2d73

        """

        # 执行A版本
        while True:
            # 升级2台
            # update_device_list = [self.device_id_one, self.device_id_two]
            # 升级3台
            # update_device_list = [self.device_id_one, self.device_id_two, self.device_id_three]
            # 升级5台
            update_device_list = [self.device_id_one, self.device_id_two, self.device_id_three, self.device_id_four,
                                  self.device_id_five]

            # 第一台机器one，执行A版本
            self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
                "device " + update_device_list[0] + " firmware " + self.update_version_id_a)
            self.driver.find_element(By.XPATH,
                                     '//span[contains(@class,"c-wysiwyg_container__send_button--w'
                                     'ith_options")]').click()
            time.sleep(10)
            # 检查是否已经是A版本
            for update_check in self.driver.find_elements(By.XPATH,
                                                          '//div[@class="c-virtual_list__item"][last()]//span'
                                                          '[@class="c-message_kit__text"]'):
                # 如果是A版本,执行B版本

                if "No upgrade needed" in update_check.text:
                    self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
                        "device " + update_device_list[0] + " firmware " + self.update_version_id_b)
                    self.driver.find_element(By.XPATH,
                                             '//span[contains(@class,"c-wysiwyg_container__send_button'
                                             '--with_options")]').click()
                    # 等待升级
                    print("------------" + self.device_sn_one + "正在升级" + self.update_version_b + "...------------")
                    time.sleep(420)
                    # 检查是否已经是B
                    self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
                        "device " + update_device_list[0] + " firmware " + self.update_version_id_b)
                    self.driver.find_element(By.XPATH,
                                             '//span[contains(@class,"c-wysiwyg_container__send_'
                                             'button--with_options")]').click()
                    time.sleep(30)
                    # 如果是已经是B版本,则B+1
                    for count in self.driver.find_elements(By.XPATH,
                                                           '//div[@class="c-virtual_list__item"][last()]//span'
                                                           '[@class="c-message_kit__text"]'):
                        """
                        Requesting firmware upgrade for device SN A3BB304556. Going from 8088 to 8087...
                        """

                        print(count.text)
                        if "No upgrade needed. Version: " + self.update_version_b in count.text:
                            self.device_one_b += 1
                            print("device_one_b += 1")

                    print(self.device_sn_one + "已经升级" + self.update_version_b + ": " + str(self.device_one_b) + "次")
                    time.sleep(30)
                # 报503
                elif "Got 5.03 status code" in update_check.text:
                    print(self.device_sn_one + " Got 5.03 status code...")
                    time.sleep(60)
                # 否则升级A
                else:
                    # 等待升级
                    print("------------" + self.device_sn_one + "正在升级" + self.update_version_a + "...------------")
                    time.sleep(420)
                    # 检查是否已经是A
                    self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
                        "device " + update_device_list[0] + " firmware " + self.update_version_id_a)
                    self.driver.find_element(By.XPATH,
                                             '//span[contains(@class,"c-wysiwyg_container__send_button--with_opti'
                                             'ons")]').click()
                    time.sleep(30)
                    # 如果是已经是A版本,则A+1

                    for count in self.driver.find_elements(By.XPATH,
                                                           '//div[@class="c-virtual_list__item"][last()]//span'
                                                           '[@class="c-message_kit__text"]'):

                        print(count.text)
                        if "No upgrade needed. Version: " + self.update_version_a in count.text:
                            self.device_one_a += 1
                            print("device_one_a += 1")

                    print(self.device_sn_one + "已经升级" + self.update_version_a + ": " + str(self.device_one_a) + "次")
                    time.sleep(30)

            # 第二台机器one，执行A版本
            self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
                "device " + update_device_list[1] + " firmware " + self.update_version_id_a)
            self.driver.find_element(By.XPATH,
                                     '//span[contains(@class,"c-wysiwyg_container__send_butto'
                                     'n--with_options")]').click()
            time.sleep(10)
            # 检查是否已经是A
            for update_check in self.driver.find_elements(By.XPATH,
                                                          '//div[@class="c-virtual_list__item"][last()]//span[@c'
                                                          'lass="c-message_kit__text"]'):
                # 如果是A,执行B
                if "No upgrade needed. Version" in update_check.text:
                    self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
                        "device " + update_device_list[1] + " firmware " + self.update_version_id_b)
                    self.driver.find_element(By.XPATH,
                                             '//span[contains(@class,"c-wysiwyg_container__send_button--with_opti'
                                             'ons")]').click()
                    # 等待升级
                    print("------------" + self.device_sn_two + "正在升级" + self.update_version_b + "...------------")
                    time.sleep(420)
                    self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
                        "device " + update_device_list[1] + " firmware " + self.update_version_id_b)
                    self.driver.find_element(By.XPATH,
                                             '//span[contains(@class,"c-wysiwyg_container__send_button--with_optio'
                                             'ns")]').click()
                    time.sleep(30)

                    for count in self.driver.find_elements(By.XPATH,
                                                           '//div[@class="c-virtual_list__item"][last()]//span'
                                                           '[@class="c-message_kit__text"]'):
                        print(count.text)
                        if "No upgrade needed. Version: " + self.update_version_b in count.text:
                            self.device_two_b += 1
                            print("device_two_b += 1")

                    print(self.device_sn_two + "已经升级" + self.update_version_b + ": " + str(self.device_two_b) + "次")
                    time.sleep(30)
                # 报503
                elif "Got 5.03 status code" in update_check.text:
                    print(self.device_sn_two + " Got 5.03 status code...")
                    time.sleep(60)
                # 否则升级4089
                else:
                    # 等待升级
                    print("------------" + self.device_sn_two + "正在升级" + self.update_version_a + "...------------")
                    time.sleep(420)

                    self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
                        "device " + update_device_list[1] + " firmware " + self.update_version_id_a)
                    self.driver.find_element(By.XPATH,
                                             '//span[contains(@class,"c-wysiwyg_container__send_button--with_opti'
                                             'ons")]').click()
                    time.sleep(30)
                    for count in self.driver.find_elements(By.XPATH,
                                                           '//div[@class="c-virtual_list__item"][last()]//sp'
                                                           'an[@class="c-message_kit__text"]'):
                        print(count.text)
                        if "No upgrade needed. Version: " + self.update_version_a in count.text:
                            self.device_two_a += 1
                            print("device_two_a += 1")

                    print(self.device_sn_two + "已经升级" + self.update_version_a + ": " + str(self.device_two_a) + "次")
                    time.sleep(30)

            # 第三台机器one，执行A版本
            # self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #     "device " + update_device_list[2] + " firmware " + self.update_version_id_a)
            # self.driver.find_element(By.XPATH,
            #                          '//span[contains(@class,"c-wysiwyg_container__send_butto'
            #                          'n--with_options")]').click()
            # time.sleep(10)
            # # 检查是否已经是A
            # for update_check in self.driver.find_elements(By.XPATH,
            #                                               '//div[@class="c-virtual_list__item"][last()]//span[@c'
            #                                               'lass="c-message_kit__text"]'):
            #     # 如果是A,执行B
            #     if "No upgrade needed. Version" in update_check.text:
            #         self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #             "device " + update_device_list[2] + " firmware " + self.update_version_id_b)
            #         self.driver.find_element(By.XPATH,
            #                                  '//span[contains(@class,"c-wysiwyg_container__send_button--with_opti'
            #                                  'ons")]').click()
            #         # 等待升级
            #         print(
            #             "------------" + self.device_sn_three + "正在升级" + self.update_version_b + "...------------")
            #         time.sleep(360)
            #         self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #             "device " + update_device_list[2] + " firmware " + self.update_version_id_b)
            #         self.driver.find_element(By.XPATH,
            #                                  '//span[contains(@class,"c-wysiwyg_container__send_button--with_optio'
            #                                  'ns")]').click()
            #         time.sleep(30)
            #
            #         for count in self.driver.find_elements(By.XPATH,
            #                                                '//div[@class="c-virtual_list__item"][last()]//span'
            #                                                '[@class="c-message_kit__text"]'):
            #             # print(count.text)
            #             if "No upgrade needed. Version: " + self.update_version_b in count.text:
            #                 self.device_three_b += 1
            #                 # print("device_two_b += 1")
            #
            #         print(self.device_sn_three + "已经升级" + self.update_version_b + ": " + str(
            #             self.device_three_b) + "次")
            #         time.sleep(30)
            #     # 报503
            #     elif "Got 5.03 status code" in update_check.text:
            #         print(self.device_sn_three + " Got 5.03 status code...")
            #         time.sleep(120)
            #     # 否则升级4089
            #     else:
            #         # 等待升级
            #         print(
            #             "------------" + self.device_sn_three + "正在升级" + self.update_version_a + "...------------")
            #         time.sleep(360)
            #
            #         self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #             "device " + update_device_list[2] + " firmware " + self.update_version_id_a)
            #         self.driver.find_element(By.XPATH,
            #                                  '//span[contains(@class,"c-wysiwyg_container__send_button--with_opti'
            #                                  'ons")]').click()
            #         time.sleep(30)
            #         for count in self.driver.find_elements(By.XPATH,
            #                                                '//div[@class="c-virtual_list__item"][last()]//sp'
            #                                                'an[@class="c-message_kit__text"]'):
            #             # print(count.text)
            #             if "No upgrade needed. Version: " + self.update_version_a in count.text:
            #                 self.device_three_a += 1
            #                 # print("device_two_a += 1")
            #
            #         print(self.device_sn_three + "已经升级" + self.update_version_a + ": " + str(
            #             self.device_three_a) + "次")
            #         time.sleep(30)

            """
                升级五台可取消注释下面代码
            """
            # # 第四台机器one，执行A版本
            # self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #     "device " + update_device_list[3] + " firmware " + self.update_version_id_a)
            # self.driver.find_element(By.XPATH,
            #                          '//span[contains(@class,"c-wysiwyg_container__send_butto'
            #                          'n--with_options")]').click()
            # time.sleep(10)
            # # 检查是否已经是A
            # for update_check in self.driver.find_elements(By.XPATH,
            #                                               '//div[@class="c-virtual_list__item"][last()]//span[@c'
            #                                               'lass="c-message_kit__text"]'):
            #     # 如果是A,执行B
            #     if "No upgrade needed. Version" in update_check.text:
            #         self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #             "device " + update_device_list[3] + " firmware " + self.update_version_id_b)
            #         self.driver.find_element(By.XPATH,
            #                                  '//span[contains(@class,"c-wysiwyg_container__send_button--with_opti'
            #                                  'ons")]').click()
            #         # 等待升级
            #         print(
            #             "------------" + self.device_sn_four + "正在升级" + self.update_version_b + "...------------")
            #         time.sleep(360)
            #         self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #             "device " + update_device_list[3] + " firmware " + self.update_version_id_b)
            #         self.driver.find_element(By.XPATH,
            #                                  '//span[contains(@class,"c-wysiwyg_container__send_button--with_optio'
            #                                  'ns")]').click()
            #         time.sleep(30)
            #
            #         for count in self.driver.find_elements(By.XPATH,
            #                                                '//div[@class="c-virtual_list__item"][last()]//span'
            #                                                '[@class="c-message_kit__text"]'):
            #             # print(count.text)
            #             if "No upgrade needed. Version: " + self.update_version_b in count.text:
            #                 self.device_four_b += 1
            #                 # print("device_two_b += 1")
            #
            #         print(self.device_sn_four + "已经升级" + self.update_version_b + ": " + str(
            #             self.device_four_b) + "次")
            #         time.sleep(30)
            #     # 报503
            #     elif "Got 5.03 status code" in update_check.text:
            #         print(self.device_sn_four + " Got 5.03 status code...")
            #         time.sleep(120)
            #     # 否则升级4089
            #     else:
            #         # 等待升级
            #         print(
            #             "------------" + self.device_sn_four + "正在升级" + self.update_version_a + "...------------")
            #         time.sleep(360)
            #
            #         self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #             "device " + update_device_list[3] + " firmware " + self.update_version_id_a)
            #         self.driver.find_element(By.XPATH,
            #                                  '//span[contains(@class,"c-wysiwyg_container__send_button--with_opti'
            #                                  'ons")]').click()
            #         time.sleep(30)
            #         for count in self.driver.find_elements(By.XPATH,
            #                                                '//div[@class="c-virtual_list__item"][last()]//sp'
            #                                                'an[@class="c-message_kit__text"]'):
            #             # print(count.text)
            #             if "No upgrade needed. Version: " + self.update_version_a in count.text:
            #                 self.device_four_a += 1
            #                 # print("device_two_a += 1")
            #
            #         print(self.device_sn_four + "已经升级" + self.update_version_a + ": " + str(
            #             self.device_four_a) + "次")
            #         time.sleep(30)
            #
            # # 第五台机器one，执行A版本
            # self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #     "device " + update_device_list[4] + " firmware " + self.update_version_id_a)
            # self.driver.find_element(By.XPATH,
            #                          '//span[contains(@class,"c-wysiwyg_container__send_butto'
            #                          'n--with_options")]').click()
            # time.sleep(10)
            # # 检查是否已经是A
            # for update_check in self.driver.find_elements(By.XPATH,
            #                                               '//div[@class="c-virtual_list__item"][last()]//span[@c'
            #                                               'lass="c-message_kit__text"]'):
            #     # 如果是A,执行B
            #     if "No upgrade needed. Version" in update_check.text:
            #         self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #             "device " + update_device_list[4] + " firmware " + self.update_version_id_b)
            #         self.driver.find_element(By.XPATH,
            #                                  '//span[contains(@class,"c-wysiwyg_container__send_button--with_opti'
            #                                  'ons")]').click()
            #         # 等待升级
            #         print(
            #             "------------" + self.device_sn_five + "正在升级" + self.update_version_b + "...------------")
            #         time.sleep(360)
            #         self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #             "device " + update_device_list[4] + " firmware " + self.update_version_id_b)
            #         self.driver.find_element(By.XPATH,
            #                                  '//span[contains(@class,"c-wysiwyg_container__send_button--with_optio'
            #                                  'ns")]').click()
            #         time.sleep(30)
            #
            #         for count in self.driver.find_elements(By.XPATH,
            #                                                '//div[@class="c-virtual_list__item"][last()]//span'
            #                                                '[@class="c-message_kit__text"]'):
            #             # print(count.text)
            #             if "No upgrade needed. Version: " + self.update_version_b in count.text:
            #                 self.device_five_b += 1
            #                 # print("device_two_b += 1")
            #
            #         print(self.device_sn_five + "已经升级" + self.update_version_b + ": " + str(
            #             self.device_five_b) + "次")
            #         time.sleep(30)
            #     # 报503
            #     elif "Got 5.03 status code" in update_check.text:
            #         print(self.device_sn_five + " Got 5.03 status code...")
            #         time.sleep(120)
            #     # 否则升级4089
            #     else:
            #         # 等待升级
            #         print(
            #             "------------" + self.device_sn_five + "正在升级" + self.update_version_a + "...------------")
            #         time.sleep(360)
            #
            #         self.driver.find_element(By.XPATH, '//div[contains(@class,"ql-editor")]').send_keys(
            #             "device " + update_device_list[4] + " firmware " + self.update_version_id_a)
            #         self.driver.find_element(By.XPATH,
            #                                  '//span[contains(@class,"c-wysiwyg_container__send_button--with_opti'
            #                                  'ons")]').click()
            #         time.sleep(30)
            #         for count in self.driver.find_elements(By.XPATH,
            #                                                '//div[@class="c-virtual_list__item"][last()]//sp'
            #                                                'an[@class="c-message_kit__text"]'):
            #             # print(count.text)
            #             if "No upgrade needed. Version: " + self.update_version_a in count.text:
            #                 self.device_five_a += 1
            #                 # print("device_two_a += 1")
            #
            #         print(self.device_sn_five + "已经升级" + self.update_version_a + ": " + str(
            #             self.device_five_a) + "次")
            #         time.sleep(30)


run = ExecuteOta()
while True:
    run.run_trim2()
