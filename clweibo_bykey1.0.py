import requests
from bs4 import BeautifulSoup
import re

cookies = dict(cookies_are = '_T_WM=0c09a3f08dcbe8dacf208915bc197a72; WEIBOCN_FROM=1110006030; SUB=_2A252Y52EDeRhGeRG6VUW-C_KyziIHXVVryPMrDV6PUJbkdAKLUqlkW1NUjqcCiF1nalG-fphLGTIKRhPyMWpQd5r; SUHB=0JvxVsut0c53KK; SCF=ArjYH8sDE7jbEpA6md5JajMm4djOR2vIf2HGawxb4_kkmR8LeWtdoHbqhPE6NJgdoC7FiXdYgG-caL8_XMBCcmw.; SSOLoginState=1533537748; MLOGIN=1; M_WEIBOCN_PARAMS=lfid%3D102803%26luicode%3D20000174%26uicode%3D20000174')


def getHTMLText(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}
	try:
		r = requests.get(url,cookies=cookies,headers=headers)
		r.raise_for_status()
		r.encoding = 'utf-8'
		return r.text
	except:
		return "Error"

def getweibo():

	id = 1809686260		#个人id
	pages = 1         #爬取总页数
	info_num = 0
	loc_num = 0
	name_num = 0
	result = ''		  #结果存储字符串
	keyw = '华中科技大学'	  #关键字
	name = 'key : ' + keyw

	pattern = re.compile(r'<a.+a>')			#去除网页链接
	pattern_name = re.compile(r'https://wei[^"]+')	#提取个人主页
	pattern_loc = re.compile(r'[男女]/[^ ]+')    #地区信息
	pattern_time = re.compile(r'\d.+来')			#时间信息


	for i in range(1,pages+1):				#对每一页循环操作
		url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=' + keyw + '&page=' + str(i)
		html = getHTMLText(url).replace('<br>','').replace('<br/>','') 	#除br标签
		soup = BeautifulSoup(html,'html.parser')

		infolist = soup.find_all('span','ctt')	#微博内容列表
		namelist = soup.find_all('a','nk')
		namelist = pattern_name.findall(str(namelist))  #个人主页列表
		timelist = soup.find_all('span','ct')

		if len(infolist) == 0:
			print('Awful!')         # No info
			return 

		for x in range(0,len(namelist)):
			info = infolist[x]
			nameurl = namelist[x]
			timet = timelist[x]

			# time = pattern_time.search(str(timet)).group(0)
			matcht = pattern_time.search(str(timet))
			if matcht:
				time = matcht.group(0)
			else:
				time = '未知'
			time = time.replace('\xa0来','')
			result = result + time + ' '

			try:
				nhtml = getHTMLText(nameurl)
				match = pattern_loc.search(nhtml[3000:6000])	#提取地理信息
				if match:
					loc = match.group(0)
					result = result + loc + ' '

				#整理标签内容
				text = str(info).replace('<span class="kt">华中科技大学</span>','华中科技大学').replace('<span class="ctt">','').replace('</span>','')
				text = pattern.sub('',text)
				text = text +'\n\n'
				result = result + text
			except:
				result = result + 'wrong\n'
				print('Something wrong')

		name_num = name_num + len(namelist)

		name_num = '爬取数：' + str(name_num) + '\n'		

		key_info = '关键字：' + keyw + '\n'

	with open('/Users/xuyunjie/Desktop/MyData/'+ name +'.txt','w') as f:
		f.write('\n' + key_info + name_num + '\n' + result)

def main():
	getweibo()

main()

