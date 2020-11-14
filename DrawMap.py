import json
import requests
import re
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
from lxml import etree
class Get_data():#获取国内疫情数据
    def get_data(self):
        url = "https://voice.baidu.com/act/newpneumonia/newpneumonia"
        response = requests.get(url);  # 获取网页源代码
        with open('源文件.txt','w') as file:#存入txt文件中
            file.write(response.text)
    def get_time(self):
        with open('源文件.txt','r') as file:#数据储存在text中
            text=file.read()
        time=re.findall('"mapLastUpdatedTime":"(.*?)"',text)[0]#正则表达式提取时间
        return time
    def parse_data(self):
        with open('源文件.txt','r') as file:
            text=file.read()
        html=etree.HTML(text)#解析
        result=html.xpath('//script[@type="application/json"]/text()')
        result = result[0]
        result = json.loads(result)
        result=result['component'][0]['caseList']
        result=json.dumps(result)#转换成字符串
        with open('data.json','w') as file:
            file.write(result)#数据初提取
class draw_map():
    def city(self,city,confirmed,province,time):
        pieces = [
            {'max': 50000, 'min': 1001, 'label': '>1000', 'color': '#8A0808'},
            {'max': 100, 'min': 51, 'label': '100-51', 'color': '#B40404'},
            {'max': 50, 'min': 11, 'label': '50-11', 'color': '#DF0101'},
            {'max': 10, 'min': 2, 'label': '10-2', 'color': '#F5A9A9'},
            {'max': 5, 'min': 1, 'label': '5-1', 'color': '#F5A9A9'},
            {'max': 0, 'min': 0, 'label': '0', 'color': '#FFFFFF'},
        ]
        c = (
            Map(init_opts=opts.InitOpts(width='1000px', height='880px'))
                .add("累计确诊人数", [list(z) for z in zip(city, confirmed)], province)
                .set_global_opts(
                title_opts=opts.TitleOpts(title=province+"疫情图", subtitle='截至' + time + '疫情分布图'),
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True, pieces=pieces),
            )
                .render(province+"疫情地图.html")
        )
    def China(self,area,confirmed,time):
        pieces=[
            {'max':100000,'min':10001,'label':'>50000','color':'#8A0808'},
            {'max':10000,'min':5001,'label':'100000-10000','color':'#B40404'},
            {'max':5000,'min':1001,'label':'5000-1001','color':'#DF0101'},
            {'max':1000,'min':101,'label':'1000-101','color':'#F5A9A9'},
            {'max':100,'min':1,'label':'100-1','color':'#F5A9A9'},
            {'max':0,'min':0,'label':'0','color':'#FFFFFF'},
        ]
        c=(
            Map(init_opts=opts.InitOpts(width='1000px',height='880px'))
                .add("累计确诊人数",[list(z) for z in zip(area,confirmed)],"china")
                .set_global_opts(
                title_opts=opts.TitleOpts(title="中国疫情图",subtitle='截至'+time+'中国疫情分布图'),
                visualmap_opts=opts.VisualMapOpts(max_=200,is_piecewise=True,pieces=pieces),
            )
            .render("中国疫情地图.html")
        )
def china_map():
   area=[]
   confirmed=[]
   for each in data:
       area.append(each['area'])
       confirmed.append(each['confirmed'])
   a.China(area,confirmed,c)
def province_map():
    for each in data:
        city = []
        Cityconfirmed = []
        province=each['area']
        for each in each['subList']:
            city.append(each['city'])
            Cityconfirmed.append(each['confirmed'])
            a.city(city, Cityconfirmed,province,c)
a = draw_map()#初始化
b=Get_data()#初始化
b.get_data()
b.parse_data()
c=b.get_time()#获取时间
with open('data.json','r') as file:
    data=file.read()
    data=json.loads(data)#转化为字典
china_map()
province_map()
