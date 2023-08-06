from lxml import etree
import xml.etree.ElementTree as ET
import re
import sqlite3
import os

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
                    "actors": [],"rating":"","link":"","smallimage":"","bigimage":""}
            bigimage = html.xpath("//div[@class='column column-video-cover']/a/@href")
            info['bigimage'] = str(bigimage[0])
            for strong, span in zip(strongs, spans):
                title = strong.text
                content = span
                if "番號" in title:
                    info['id'] = content.text
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
        result=[]
        for item in infos:
            result.append(item[s])
        if s=="name":
            return str.join('/',result)
        elif s=="link":
            return str.join(';',result)

    def format(self,info,previewimages,magnets):
        detailinfo= {"id": "", "date": "", "runtime": 0, "javdblink":"","director": "", "directorlink": "", "studio": "", "studiolink": "",
                     "tag": "", "taglink": "","genres": "","genreslink": "","actors": "","actorslink": "","rating":0.00,"ratingnum":0,
                     "smallimage":"","bigimage":"","previewimages":"","magnets":""}

        detailinfo['id']=info['id']
        detailinfo['date'] = info['date']
        if info['runtime']: detailinfo['runtime'] = int(info['runtime'])
        detailinfo['javdblink'] = info['link']
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
            d["title"] = title
            d["date"] = date
            d["javdb_link"] = javdb_link
            d["img"] = img
            d["tags"] = tags
            result.append(d)
        return result

class Save:

    def __init__(self,savepath):
        self.savepath=savepath


    def createdb(self):
        conn = sqlite3.connect(self.savepath)
        c = conn.cursor()
        c.execute('''CREATE TABLE briefinfo
              (uid             TEXT PRIMARY KEY ,
               title           TEXT,
               date        CHAR(10),
               javdb_link        CHAR(50),
               img          TEXT,
               tags         TEXT
               );''')
        conn.commit()
        print("成功创建表 briefinfo")
        c.execute('''CREATE TABLE detailinfo
              (id             TEXT PRIMARY KEY ,
               date           CHAR(10),
               runtime        INTEGER DEFAULT 0,
               javdblink      CHAR(10),
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
               );''')

        conn.commit()
        print("成功创建表 detailinfo")
        conn.close()



    def save(self, detailinfo):
        if not os.path.exists(self.savepath):self.createdb()
        conn = sqlite3.connect(self.savepath)
        cursor = conn.cursor()
        sqltext = f"INSERT INTO movie (id,date,runtime,javdblink,director,directorlink,studio,studiolink,tag,taglink,genres,genreslink,actors,actorslink,rating,ratingnum,smallimage,bigimage,previewimages,magnets) " \
                  f"VALUES ('{detailinfo['id']}', '{detailinfo['date']}', {detailinfo['runtime']}, '{detailinfo['javdblink']}','{detailinfo['director']}','{detailinfo['directorlink']}','{detailinfo['studio']}','{detailinfo['studiolink']}','{detailinfo['tag']}','{detailinfo['taglink']}','{detailinfo['genres']}','{detailinfo['genreslink']}','{detailinfo['actors']}','{detailinfo['actorslink']}',{detailinfo['rating']}, {detailinfo['ratingnum']},'{detailinfo['smallimage']}','{detailinfo['bigimage']}','{detailinfo['previewimages']}','{detailinfo['magnets']}') " \
                  f"ON CONFLICT(id) DO UPDATE SET date = '{detailinfo['date']}',runtime={detailinfo['runtime']},javdblink='{detailinfo['javdblink']}',director='{detailinfo['director']}',directorlink='{detailinfo['directorlink']}',studio='{detailinfo['studio']}',studiolink='{detailinfo['studiolink']}',tag='{detailinfo['tag']}',taglink='{detailinfo['taglink']}',genres='{detailinfo['genres']}',genreslink='{detailinfo['genreslink']}',actors='{detailinfo['actors']}',actorslink='{detailinfo['actorslink']}',rating={detailinfo['rating']},ratingnum={detailinfo['ratingnum']},smallimage='{detailinfo['smallimage']}',bigimage='{detailinfo['bigimage']}',previewimages='{detailinfo['previewimages']}',magnets='{detailinfo['magnets']}';"
        cursor.execute(sqltext)
        conn.commit()
        conn.close()

