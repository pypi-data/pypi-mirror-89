from lxml import etree
import xml.etree.ElementTree as ET
import re
import sqlite3
import os
from Util.Mysqlite import *
import requests
requests.packages.urllib3.disable_warnings()    #关闭警告

class Parse:
    def __init__(self,source_code):
        self.source_code=source_code
        if not self.source_code: raise  Exception("源码为空！")

    def getdate(self,date):
        m=re.search(pattern=r'\d{4}-\d{2}-\d{2}',string=date)
        if m:return m.group()
        else:return ""

    def getdetailinfo(self,sourcecode):
        html = etree.HTML(sourcecode)
        strongs = html.xpath("//nav[@class='panel video-panel-info']/div/strong")
        spans = html.xpath("//nav[@class='panel video-panel-info']/div/span")
        if strongs:
            info = {"id": "", "date": "", "runtime": "", "director": [], "studio": [], "tag": [], "genres": [],
                    "actors": [],"rating":"","link":"","smallimage":"","bigimage":"","title":""}
            info["title"] = html.xpath("//h2[@class='title is-4']/strong")[0].text
            bigimage = html.xpath("//div[@class='column column-video-cover']/a/@href")
            info['bigimage'] = str(bigimage[0])
            for strong, span in zip(strongs, spans):
                title = strong.text
                content = span
                if "番號" in title:
                    info['id'] =''.join(content.itertext())
                    if info["id"]:
                        info["title"]=info["title"].replace(info["id"],"")
                        if info["title"] and info["title"].startswith(" "):info["title"]=info["title"][1:]
                elif "日期" in title:
                    info['date'] = content.text
                elif "時長" in title:
                    searchresult=re.search(pattern='\d+', string=content.text)
                    if searchresult is not None:
                        info['runtime'] = searchresult.group()
                elif "片商" in title or "賣家" in title:
                    inhtml = etree.HTML(ET.tostring(span))
                    alist = inhtml.xpath("//a")
                    studios = []
                    for i in range(len(alist)):
                        studio = {"name": "", "link": ""}
                        studio["name"] = alist[i].text
                        studio["link"] = inhtml.xpath("//a/@href")[i]
                        studios.append(studio)
                    info['studio'] = studios
                elif "系列" in title:
                    inhtml = etree.HTML(ET.tostring(span))
                    alist = inhtml.xpath("//a")
                    tags = []
                    for i in range(len(alist)):
                        tag = {"name": "", "link": ""}
                        tag["name"] = alist[i].text
                        tag["link"] = inhtml.xpath("//a/@href")[i]
                        tags.append(tag)
                    info['tag'] = tags
                elif "導演" in title:
                    inhtml = etree.HTML(ET.tostring(span))
                    alist = inhtml.xpath("//a")
                    directors = []
                    for i in range(len(alist)):
                        director = {"name": "", "link": ""}
                        director["name"] = alist[i].text
                        director["link"] = inhtml.xpath("//a/@href")[i]
                        directors.append(director)
                    info['director'] = directors
                elif "類別" in title:
                    inhtml = etree.HTML(ET.tostring(span))
                    alist = inhtml.xpath("//a")
                    genres = []
                    for i in range(len(alist)):
                        genre = {"name": "", "link": ""}
                        genre["name"] = alist[i].text
                        genre["link"] = inhtml.xpath("//a/@href")[i]
                        genres.append(genre)
                    info['genres'] = genres
                elif "演員" in title:
                    inhtml = etree.HTML(ET.tostring(span))
                    alist = inhtml.xpath("//a")
                    actors = []
                    for i in range(len(alist)):
                        actor = {"name": "", "link": ""}
                        actor["name"] = alist[i].text
                        actor["link"] = inhtml.xpath("//a/@href")[i]
                        actors.append(actor)
                    info['actors'] = actors
                elif "評分" in title:
                    t=''.join(span.itertext())
                    info['rating'] = t.replace(u'\xa0','')
            return info

    def getmagnets(self,sourcecode):
        html = etree.HTML(sourcecode)
        links = html.xpath("//div[@id='magnets-content']/table/tr/td[@class='magnet-name']/a/@href")
        dates = html.xpath("//div[@id='magnets-content']/table/tr/td[@class='sub-column']/span[@class='time']")
        alist = html.xpath("//div[@id='magnets-content']/table/tr/td[@class='magnet-name']/a")

        magnets = []
        for link,date,span in zip(links,dates,alist):
            magnet = {"link": link, "date": date.text, "linkinfo": []}
            inhtml = etree.HTML(ET.tostring(span))
            spans = inhtml.xpath("//span")
            spantext = []
            for s in spans:
                spantext.append(s.text.replace('\n','').replace(" ","").replace(u'\xa0','').replace("(","").replace(")",""))
            magnet["linkinfo"] = spantext
            magnets.append(magnet)
        # print(magnets)
        return magnets


    def parse_detail(self):
        result = {"detailinfo":{},"previewimages":[],"magnets":{}}
        html = etree.HTML(self.source_code)
        result["detailinfo"]=self.getdetailinfo(self.source_code)#详细信息
        result["previewimages"] = html.xpath("//div[@class='tile-images preview-images']/a[@class='tile-item']/@href")#预览图
        result["magnets"] = self.getmagnets(self.source_code)#磁力链接
        return self.format(result["detailinfo"],result["previewimages"],result["magnets"])



    def getinfofromdict(self,infos,s):
        #/v/JPbeq 未知演员
        result=[]
        for item in infos:
            value=item[s]
            if value:result.append(value)
            else:result.append("未知演员")
        if s=="name":
            return str.join('/',result)
        elif s=="link":
            return str.join(';',result)

    def format(self,info,previewimages,magnets):
        detailinfo= {"id": "", "date": "", "runtime": 0, "javdblink":"","title":"","director": "", "directorlink": "", "studio": "", "studiolink": "",
                     "tag": "", "taglink": "","genres": "","genreslink": "","actors": "","actorslink": "","rating":0.00,"ratingnum":0,
                     "smallimage":"","bigimage":"","previewimages":"","magnets":""}

        detailinfo['id']=info['id']
        detailinfo['date'] = info['date']
        if info['runtime']: detailinfo['runtime'] = int(info['runtime'])
        detailinfo['javdblink'] = info['link']
        detailinfo['title'] = info['title'].replace("'","").replace("\n","").replace("\t","").replace("\r","").replace(u"\xa0","")
        detailinfo['director'] = self.getinfofromdict(info['director'],'name').replace("'","")
        detailinfo['directorlink'] = self.getinfofromdict(info['director'],'link')
        detailinfo['studio'] = self.getinfofromdict(info['studio'], 'name').replace("'","")
        detailinfo['studiolink'] = self.getinfofromdict(info['studio'], 'link')
        detailinfo['tag'] = self.getinfofromdict(info['tag'], 'name').replace("'","")
        detailinfo['taglink'] = self.getinfofromdict(info['tag'], 'link')
        detailinfo['genres'] = self.getinfofromdict(info['genres'], 'name').replace("'","")
        detailinfo['genreslink'] = self.getinfofromdict(info['genres'], 'link')
        detailinfo['actors'] = self.getinfofromdict(info['actors'], 'name').replace("'","")
        detailinfo['actorslink'] = self.getinfofromdict(info['actors'], 'link')
        if '分' in info['rating'] and ',' in info['rating']:
            m1=re.search(pattern='\d\.\d+',string=info['rating'].split(',')[0])
            if m1 is not None:detailinfo['rating'] =float(format(float(m1.group()),'1.2f'))
            m2=re.search(pattern='\d+', string=info['rating'].split(',')[1])
            if m2 is not None:detailinfo['ratingnum'] = int(m2.group())
        detailinfo['smallimage'] = info['smallimage']
        detailinfo['bigimage'] = info['bigimage']
        if previewimages:detailinfo['previewimages'] = str.join(';',previewimages)
        if magnets:detailinfo['magnets'] = str(magnets).replace("'","\"")
        return detailinfo


    def parse_single(self):
        html=etree.HTML(self.source_code)
        divs=html.xpath("//div[@class='grid-item column horz-cover']")
        result=[]
        for div in divs:
            d={"uid":"","title":"","date":"","javdb_link":"","img":"","tags":""}
            div = etree.HTML(etree.tostring(div))
            uid=div.xpath("//div[@class='uid']")[0].text
            title=div.xpath("//div[@class='video-title']")[0].text
            date=div.xpath("//div[@class='meta']")[0].text.replace("\n","").replace(" ","")
            javdb_link=div.xpath("//a[@class='box']/@href")[0]
            img=div.xpath("//img/@data-src")[0]
            tags='/'.join(div.xpath("//div[@class='tags has-addons']")[0].itertext()).replace("\n","").replace(" ","")
            d["uid"]=uid
            d["title"] = title.replace("'","’")
            d["date"] = date
            d["javdb_link"] = javdb_link
            d["img"] = img
            d["tags"] = tags
            result.append(d)
        return result


class JAVDB_TEXT_CRAWLER:
    '''
    文字爬虫，形如 /series/western
    '''

    '''
    使用方法
    path=os.path.join(os.getcwd(),"test.db")
    url1 = "https://***.com/series"
    crawler=JAVDB_TEXT_CRAWLER(path,url1)
    crawler.crawl()
    '''



    SQLITE_TABLE='''CREATE TABLE info
                  (id             TEXT PRIMARY KEY ,
                   title           TEXT,
                   number        TEXT
                   );'''

    def __init__(self,db_path,url):
        '''

        :param db_path:要保存的数据库的绝对路径，如 D:\\sample.db
        :param url:要爬取的地址的绝对路径，如 https://baidu.com/series
        '''
        if not os.path.exists(db_path):create_database(db_path,self.SQLITE_TABLE)
        self.url=url
        self.db_path=db_path


    def getheaders(self):
        cookie = self.get_cookies_from_file()
        if cookie is None or len(cookie) <= 0:
            raise Exception("cookie 为空！")
        headers = {
            "Host": "javdb5.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/78.0.3904.108Safari/537.36",
            "Sec-Fetch-User": "?1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Referer": "https",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": str(cookie)
        }
        return headers


    def get_cookies_from_file(self):
        if not os.path.exists('cookie.txt'):
            raise FileNotFoundError("cookie.txt 文件不存在！")

        with open('cookie.txt', 'r') as f:
            return f.read()


    def parse(self,source_code):
        html = etree.HTML(source_code)
        divs = html.xpath("//div[@class='box']")
        result = []
        for div in divs:
            d = {"id": "", "title": "", "number": ""}
            div = etree.HTML(etree.tostring(div))
            id = div.xpath("//a/@href")[0]
            title = div.xpath("//a/strong")[0].text.replace("'","‘")
            number = div.xpath("//a/span")[0].text.replace("(","").replace(")","")
            d["id"] = id
            d["title"] = title
            d["number"] = number
            result.append(d)
        return result

    def save(self,datas):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for detailinfo in datas:
            sqltext = f"INSERT INTO info (id,title,number) " \
                      f"VALUES ('{detailinfo['id']}', '{detailinfo['title']}', '{detailinfo['number']}') " \
                      f"ON CONFLICT(id) DO UPDATE SET title = '{detailinfo['title']}',number = '{detailinfo['number']}';"
            cursor.execute(sqltext)
            conn.commit()
        conn.close()

    def crawl(self):
        idx = 1
        baseurl = self.url + f"?page="
        while True:
            url = baseurl + str(idx)
            print(f"开始爬取第 {str(idx)} 页")
            r = requests.get(url, headers=self.getheaders(), verify=False)
            r.encoding = 'utf-8'
            html = r.text
            if html:
                if '暫無內容' in html:
                    print(f"总共爬取了 {str(idx - 1)} 页")
                    break
                else:
                    datas = self.parse(html)
                    self.save(datas)
                    idx += 1










class Javdb_Sqlite:
    SQLITE_TABLE_BRIEF='''CREATE TABLE brief
              (uid             TEXT PRIMARY KEY ,
               title           TEXT,
               date        CHAR(10),
               javdb_link        CHAR(50),
               img          TEXT,
               tags         TEXT
               );'''
    SQLITE_TABLE_DETAIL='''CREATE TABLE detail
              (id             TEXT PRIMARY KEY ,
               date           CHAR(10),
               runtime        INTEGER DEFAULT 0,
               javdblink      CHAR(10),
               title          TEXT,
               director       TEXT,
               directorlink   TEXT,
               studio         TEXT,
               studiolink     TEXT,
               tag            TEXT,
               taglink        TEXT,
               genres         TEXT,
               genreslink     TEXT,
               actors         TEXT,
               actorslink     TEXT,
               rating         REAL DEFAULT 0.00,
               ratingnum      INTEGER DEFAULT 0,
               smallimage     TEXT,
               bigimage       TEXT,
               previewimages  TEXT,
               magnets        TEXT
               );'''

    SQLITETABLE_MOVIE = "create table if not exists movie (id VARCHAR(50) PRIMARY KEY , title TEXT , filesize DOUBLE DEFAULT 0 , filepath TEXT , subsection TEXT , vediotype INT , scandate VARCHAR(30) , releasedate VARCHAR(10) DEFAULT '1900-01-01', visits INT  DEFAULT 0, director VARCHAR(50) , genre TEXT , tag TEXT , actor TEXT , actorid TEXT ,studio VARCHAR(50) , rating FLOAT  DEFAULT 0, chinesetitle TEXT , favorites INT  DEFAULT 0, label TEXT , plot TEXT , outline TEXT , year INT  DEFAULT 1900, runtime INT  DEFAULT 0, country VARCHAR(50) , countrycode INT DEFAULT 0 ,otherinfo TEXT, sourceurl TEXT, source VARCHAR(10),actressimageurl TEXT,smallimageurl TEXT,bigimageurl TEXT,extraimageurl TEXT)";
    SQLITETABLE_ACTRESS = "create table if not exists actress ( id VARCHAR(50) PRIMARY KEY, name VARCHAR(50) ,birthday VARCHAR(10) ,age INT ,height INT ,cup VARCHAR(1), chest INT ,waist INT ,hipline INT ,birthplace VARCHAR(50) ,hobby TEXT, sourceurl TEXT, source VARCHAR(10),imageurl TEXT)";
    SQLITETABLE_ACTRESS_LOVE = "create table if not exists actresslove ( name VARCHAR(50) PRIMARY KEY,islove INT )";
    SQLITETABLE_LIBRARY = "create table if not exists library ( id VARCHAR(50) PRIMARY KEY, code VARCHAR(50))";
    SQLITETABLE_JAVDB = "create table if not exists javdb ( id VARCHAR(50) PRIMARY KEY, code VARCHAR(50))";



    def __init__(self,path):
        self.path=path


    def createdb(self):
        create_database(self.path,self.SQLITE_TABLE_BRIEF)
        create_database(self.path,self.SQLITE_TABLE_DETAIL)


    def save(self, detailinfo):
        if not os.path.exists(self.path):self.createdb()
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        sqltext = f"INSERT INTO detail (id,date,runtime,javdblink,title,director,directorlink,studio,studiolink,tag,taglink,genres,genreslink,actors,actorslink,rating,ratingnum,smallimage,bigimage,previewimages,magnets) " \
                  f"VALUES ('{detailinfo['id']}', '{detailinfo['date']}', {detailinfo['runtime']}, '{detailinfo['javdblink']}', '{detailinfo['title']}','{detailinfo['director']}','{detailinfo['directorlink']}','{detailinfo['studio']}','{detailinfo['studiolink']}','{detailinfo['tag']}','{detailinfo['taglink']}','{detailinfo['genres']}','{detailinfo['genreslink']}','{detailinfo['actors']}','{detailinfo['actorslink']}',{detailinfo['rating']}, {detailinfo['ratingnum']},'{detailinfo['smallimage']}','{detailinfo['bigimage']}','{detailinfo['previewimages']}','{detailinfo['magnets']}') " \
                  f"ON CONFLICT(id) DO UPDATE SET date = '{detailinfo['date']}',runtime={detailinfo['runtime']},javdblink='{detailinfo['javdblink']}',title='{detailinfo['title']}',director='{detailinfo['director']}',directorlink='{detailinfo['directorlink']}',studio='{detailinfo['studio']}',studiolink='{detailinfo['studiolink']}',tag='{detailinfo['tag']}',taglink='{detailinfo['taglink']}',genres='{detailinfo['genres']}',genreslink='{detailinfo['genreslink']}',actors='{detailinfo['actors']}',actorslink='{detailinfo['actorslink']}',rating={detailinfo['rating']},ratingnum={detailinfo['ratingnum']},smallimage='{detailinfo['smallimage']}',bigimage='{detailinfo['bigimage']}',previewimages='{detailinfo['previewimages']}',magnets='{detailinfo['magnets']}';"
        cursor.execute(sqltext)
        conn.commit()
        conn.close()

    def select_from_detail(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        c.execute(f"SELECT * FROM detail")
        fetchers = c.fetchall()
        conn.close()
        result = []
        for i in range(len(fetchers)):
            detailinfo = {"id": "", "date": "", "runtime": 0, "javdblink": "", "title": "", "director": "",
                          "directorlink": "", "studio": "", "studiolink": "",
                          "tag": "", "taglink": "", "genres": "", "genreslink": "", "actors": "", "actorslink": "",
                          "rating": 0.00, "ratingnum": 0,
                          "smallimage": "", "bigimage": "", "previewimages": "", "magnets": ""}
            keys=[key for key in detailinfo.keys()]
            for j in range(len(keys)):
                key=keys[j]
                detailinfo[key]=fetchers[i][j]
            result.append(detailinfo)
        return result

    def toJvedio(self,targetpath,vediotype=1):
        create_tables(targetpath,self.SQLITETABLE_MOVIE,self.SQLITETABLE_ACTRESS,self.SQLITETABLE_LIBRARY,self.SQLITETABLE_JAVDB)
        #读取信息
        detailinfos=self.select_from_detail()
        # 插入 movie
        conn = sqlite3.connect(targetpath)
        cursor = conn.cursor()
        for detailinfo in detailinfos:
            genre=detailinfo['genres'].replace("/"," ")
            sqltext = "INSERT INTO movie(id,vediotype,title,releasedate,director,genre,tag,actor,actorid," \
                      "studio,rating,runtime,sourceurl,source," \
                      "smallimageurl,bigimageurl,extraimageurl) " \
                      f"values('{detailinfo['id']}',{vediotype},'{detailinfo['title']}','{detailinfo['date']}','{detailinfo['director']}','{genre}','{detailinfo['tag']}'," \
                      f"'{detailinfo['actors']}','{detailinfo['actorslink']}','{detailinfo['studio']}',{detailinfo['rating']}," \
                      f"{detailinfo['runtime']},'{detailinfo['javdblink']}','javdb','{detailinfo['smallimage']}','{detailinfo['bigimage']}','{detailinfo['previewimages']}')" \
                      f"ON CONFLICT(id) DO UPDATE SET vediotype={vediotype},title='{detailinfo['title']}',releasedate='{detailinfo['date']}',director='{detailinfo['director']}',genre='{genre}',tag='{detailinfo['tag']}'," \
                      f"actor='{detailinfo['actors']}',actorid='{detailinfo['actorslink']}',studio='{detailinfo['studio']}',rating={detailinfo['rating']}," \
                      f"runtime={detailinfo['runtime']},sourceurl='{detailinfo['javdblink']}',source='javdb'," \
                      f"smallimageurl='{detailinfo['title']}',bigimageurl='{detailinfo['title']}',extraimageurl='{detailinfo['title']}'";
            cursor.execute(sqltext)
            link=detailinfo['javdblink'].replace("/v/","")
            sqltext2 = f"insert into  javdb(id,code) values('{detailinfo['id']}','{link}') ON CONFLICT(id) DO UPDATE SET code='{link}'";
            cursor.execute(sqltext2)
            conn.commit()
        conn.close()
        #插入 javdb
        print("成功转为 Jvedio 数据库")


