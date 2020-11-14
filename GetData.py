import requests
from lxml import etree
import json
import openpyxl #数据写入excel
#----------------------------
##提取国内外疫情数据到excel文件
#------------------------------
url="https://voice.baidu.com/act/newpneumonia/newpneumonia"
response=requests.get(url);#获取网页源代码
html=etree.HTML(response.text);
result=html.xpath('//script[@type="application/json"]/text()')#获取标签列表
result2=html.xpath('//script[@type="application/json"]/text()')#获取标签列表
result=result[0]#所有标签
result2=result2[0]#所有标签
result=json.loads(result)#字符串类型转换成字典
result2=json.loads(result2)
#创建一个工作簿
wb=openpyxl.Workbook()#国内
wb2=openpyxl.Workbook()#国外
#创建一个工作表
ws=wb.active
ws2=wb2.active
ws.titile='国内疫情'
ws2.titile='国外疫情'
ws.append(['省份','累计确诊','死亡人数','治愈人数','现有确诊','新增确诊'])
ws2.append(['国家','累计确诊','死亡人数','治愈人数','现有确诊','新增确诊'])
result=result['component'][0]['caseList']#国内疫情
result2=result2['component'][0]['caseOutsideList']#国外疫情
#"area":"省/国""city":"城市","confirmed":"累计确诊","died":"死亡","crued":"治愈","curConfirm":"累计确诊增量"
# confirmedRelative":"累计治愈增加量","curConfirm":"现有确诊人数",curConfirmRelative "现有确诊增量 diedRelative:"死亡增量
for each in result2:
    ws2.append([each['area'],each['confirmed'],each['died'],each['crued'],each['curConfirm'],each['confirmedRelative']])
for each in result:
    ws.append([each['area'],each['confirmed'],each['died'],each['crued'],each['curConfirm'],each['confirmedRelative']])
wb.save('国内数据.xlsx')
wb2.save('国外数据.xlsx')