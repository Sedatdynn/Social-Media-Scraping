from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from webdriver.dbconnection import connect
import os


class Facebook:
    def __init__(self,mail,password):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("disable-notifications")
        options.add_argument('--no-sandbox')
        browser_locale = 'tr'
        options.add_argument("--lang={}".format(browser_locale))
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('prefs', {'intl.accept_languages': 'tr'})

        pc_username = os.getenv("USERNAME")
        self.mail = mail
        self.password = password
        self.browser = webdriver.Chrome(executable_path=f"C:\\Users\\{pc_username}\\Desktop\\SedatTasks\\webdriver\\chromedriver.exe",options=options)
        self.browser.maximize_window()
        self.db = connect()

        self.doc = []


    def sıgnIn(self):
        self.browser.get("https://www.facebook.com/login")
        try:

            mailInput = WebDriverWait(self.browser,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="email"]')))

            passwordInput = self.browser.find_element_by_xpath('//*[@id="pass"]')

            mailInput.send_keys(self.mail)
            passwordInput.send_keys(self.password)
        except:
            print("şifre veya email hatalı olabilir. Tekrar deneyiniz.")


        try:
            login = WebDriverWait(self.browser,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="loginbutton"]')))
            login.click()
            time.sleep(10)
        except:
            print("Giriş yapılırken bir hata ile karşılaşıldı!")


    def group(self):
        self.browser.get("https://www.facebook.com/groups/sabrireyizresmi")
        time.sleep(5)
        i = 0
        while i <= 3000:
            self.browser.execute_script(f"window.scrollTo(0, {i})")

            time.sleep(2)
            i += 500

        time.sleep(5)

        page_source = self.browser.page_source
        #print(page_source)
        data = BeautifulSoup(page_source, "html.parser")

        title = data.find("h1",{"class": "gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl d2edcug0 hpfvmrgz"}).find("span").text
        #print(title) ---------->  #-Galatasaray Ailesi

        about = data.find_all("div",{"class":"rq0escxv l9j0dhe7 du4w35lb qmfd67dx hpfvmrgz gile2uim buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5"})
        grup_info = about[1].find("div",class_ = "kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql").find("div").text
        #print(grup_info) --------> Galatasaray taraftar topluluğu olarak Galatasarayımız ile ilgili en güncel bilgiler.
        time.sleep(5)

        members = data.find_all("div", class_ = "qzhwtbm6 knvmm38d")



        members_private = ""
        try:
            members_private = members[4].find("span",class_="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh e9vueds3 j5wam9gi knj5qynh oo9gr5id").text

        except:
            if members_private:
                pass

            else:
                members_private = "Grup gizlilik bilgisi çekilemedi."


        #print(members_private) #----------------->  Sadece üyeler grupta kimlerin olduğunu ve neler paylaştıklarını görebilir.
        visible = ""

        try:
            visible = members[6].find("span", class_="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh e9vueds3 j5wam9gi knj5qynh oo9gr5id").text
            #print(visible) #------->  Bu grubu herkes bulabilir.
        except:
            if visible:
                pass
            else:
                visible = "Grup gizliliği görüntülenemedi."

        listToStr = ""
        try:
            created_date = members[10].find("span",
                                            class_="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh e9vueds3 j5wam9gi knj5qynh oo9gr5id").text.split(
                " ")[:4]
            listToStr = ' '.join(map(str, created_date))
        except Exception as err:
            print(err)
            created_date = data.find_all('span',
                                         class_='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh e9vueds3 j5wam9gi knj5qynh oo9gr5id')
            listToStr = created_date[2].text.split("Daha Fazlasını Gör")[0]



        total_member = ""
        try:

            # total_member = members[11].find("h2", class_ = "gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl d2edcug0 hpfvmrgz").text.split(" ")[3]
            total_member = data.find_all('h2', class_='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl d2edcug0 hpfvmrgz')[1].text

        except Exception as err:
            print(err)
            total_member = data.find('span',
                                     class_='2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a5q79mjw g1cxx5fr lrazzd5p m9osqain').text


        today = members[12].find("span").text

        last_month = members[13].find("span").text

        post = str(today) + " - " + str(last_month)

        total_members = members[14].find("span").text

        last_week = members[15].find("span").text

        members_info = str(total_members) + " - " + str(last_week)



        rule_heads = []
        rule_infos = []
        group_rules = {}

        to_rule = data.find_all('div',
                                class_='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t g5gj957u d2edcug0 hpfvmrgz rj1gh0hx buofh1pr p8fzw8mz pcp91wgn iuny7tx3 ipjc6fyt')[
                  3:]
        for j in to_rule:
            rule_heads.append(j.find('span').text)

        to_rule_info = data.find_all('div',
                                     class_='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t g5gj957u d2edcug0 hpfvmrgz rj1gh0hx buofh1pr ife1yexw d6emx29t sj5x9vvc ipjc6fyt')
        for i in to_rule_info:
            rule_infos.append(i.find('span').text)

        for key in rule_heads:
            for value in rule_infos:
                group_rules[key] = value
                rule_infos.remove(value)
                break

        my_data = {
            'id': 0,
            'Group Name': title,
            'Group Description': grup_info,
            'Members Private': members_private,
            'Visible': visible,
            'Created Date': listToStr,
            'Total Member': total_member,
            'Post Info': post,
            'Members Info': members_info,
            'Group Rules': str(group_rules)

        }
        self.doc.append(my_data)

    def save_db(self):
        cursor = self.db.cursor()

        try:
            cursor.execute("CREATE TABLE facebookdatas ( id int NOT NULL AUTO_INCREMENT, group_name  TEXT, group_descript TEXT, members_private TEXT, visible TEXT, created_date VARCHAR(125), total_member VARCHAR(255),post_info VARCHAR(125),members_info VARCHAR(255), group_rules TEXT,"
                           "PRIMARY KEY (id) ) ")
        except Exception as err:
            print(err)

        insert_data = (
            "INSERT INTO facebookdatas (  group_name, group_descript, members_private, visible, created_date, total_member, post_info, members_info, group_rules )"
            "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s )"
        )
        for data in self.doc:

            js_datas = ( data["Group Name"], data['Group Description'], data['Members Private'], data['Visible'], data['Created Date'], data['Total Member'], data['Post Info'], data['Members Info'], data['Group Rules'])

            cursor.execute(insert_data, js_datas)

            self.db.commit()
        self.db.close()



        self.browser.quit()









facebook = Facebook(mail="email",password="password")
facebook.sıgnIn()
facebook.group()
facebook.save_db()