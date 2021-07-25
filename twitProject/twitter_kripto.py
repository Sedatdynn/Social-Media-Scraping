from selenium import  webdriver
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from webdriver.dbconnection import connect

class Twitter:

    def __init__(self,username,password,hasthag,keyword):

        options = webdriver.ChromeOptions()
        options.add_argument("disable-notifications")
        options.add_argument('--no-sandbox')
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches",
                                        ["ignore-certificate-errors", "safebrowsing-disable-download-protection",
                                         "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

        self.username = username
        self.password = password
        self.hashtag = hasthag
        self.keyword = keyword
        pc_username = os.getenv("USERNAME")
        options.add_argument("--excludeSwitches")
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-infobars')
        options.add_argument(f"user-data-dir=C:\\Users\\{pc_username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        self.browser = webdriver.Chrome(executable_path=f"C:\\Users\\{pc_username}\\Desktop\\SedatTasks\\webdriver\\chromedriver.exe",options=options)
        self.browser.maximize_window()
        self.db = connect()

    def sıgnIn(self):
        self.browser.get("https://www.twitter.com/login")
        time.sleep(5)

        if self.browser.current_url == 'https://twitter.com/home':
            self.Search(self.hashtag)

        else:
            try:

                userInput = WebDriverWait(self.browser,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')));

                passwordInput = self.browser.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')

                userInput.send_keys(self.username)
                passwordInput.send_keys(self.password)
            except:
                print("Bir hata çıktı!")


            try:
                login = WebDriverWait(self.browser,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')));
                login.click()
                time.sleep(5)
                self.browser.maximize_window()
                time.sleep(2)
            except:
                print("Giriş yapılırken bir hata ile karşılaşıldı!")
                time.sleep(3)


            time.sleep(3)
            self.Search(self.hashtag)

    def Search(self, hashtag):
        searchInput = self.browser.find_elements_by_tag_name("input")[1]
        time.sleep(3)
        searchInput.send_keys(hashtag)
        time.sleep(3)
        searchInput.send_keys(Keys.ENTER)


        time.sleep(4)
        i = 0
        while i <= 3000:
            self.browser.execute_script(f"window.scrollTo(0, {i})")

            time.sleep(2)
            i += 500

        time.sleep(10)

        page_source = self.browser.page_source
        data = BeautifulSoup(page_source, "html.parser")


        all_tweets = data.find_all('article', class_='css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg')



        tweet_datas = { "datas":[] }

        for i in range(0, len(all_tweets)):
            user_nickname = all_tweets[i].find('div', class_='css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t').find('span').text
            tweet_texts = all_tweets[i].find('div',class_='css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0').text


            if self.keyword in tweet_texts:
                to_js = {
                    'username': user_nickname,
                    'tweet': tweet_texts,
                    'keyword': self.keyword
                }

            else:
                to_js = {
                    'username': user_nickname,
                    'tweet': tweet_texts,
                    'keyword': "no keyword"
                }



            tweet_datas['datas'].append(to_js)




        self.saveDB(tweet_datas)

    def saveDB(self, data:dict):
        cursor = self.db.cursor()

        try:
            cursor.execute(
                "CREATE TABLE twitterdatas ( id int NOT NULL AUTO_INCREMENT, user_name  TEXT, tweet_text TEXT, keyword TEXT,"
                "PRIMARY KEY (id) ) ")
        except Exception as err:
            print(err)

        insert_data = (
            "INSERT INTO twitterdatas (  user_name, tweet_text, keyword )"
            "VALUES ( %s, %s, %s)"
        )
        for item in data['datas']:
            js_datas = (item["username"], item['tweet'], item['keyword'])

            cursor.execute(insert_data, js_datas)

            self.db.commit()


        self.browser.quit()

        self.show_graph()

    def show_graph(self):
        all_datas = self.readDB()

        with_keyword = []
        no_keyword = []

        for item in all_datas:
            if item[3] == self.keyword:
                with_keyword.append("1")

            no_keyword.append("0")

        labels = 'With Keyword', 'No Keyword'
        sizes = [len(with_keyword), len(no_keyword)]
        explode = (0, 0)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')

        plt.show()

    def readDB(self):
        my_database = self.db.cursor()
        sql_statement = "SELECT * FROM twitterdatas"
        my_database.execute(sql_statement)
        output = my_database.fetchall()
        self.db.close()

        return output


twitter = Twitter(username="username/email",password="password",hasthag="Kripto Para", keyword="bitcoin")
twitter.sıgnIn()



