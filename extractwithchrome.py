#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv
import requests

#max_page = 5
	
with open('data.csv', 'a') as f:
	writer = csv.writer(f)
	writer.writerow(["Name", "Address", "Phone", "Website"])
	
	for lk in open('base-url.txt','r'):
		soupi = BeautifulSoup(requests.get(lk).content,"lxml")
		page_class = soupi.find("div",class_="page-of-pages")
		max_page = page_class.text.rsplit(None, 1)[-1]
		#print max_page
		page_number = 750
		#print page_number
		while page_number < int(max_page)*10:
			baseurl = lk +'&start={}'.format(page_number)
			driver = webdriver.Chrome()
			driver.get(baseurl)
			html = driver.page_source
			soup = BeautifulSoup(html, "html.parser")
			print baseurl
			urlname = []
			for item in soup.find_all("a", class_="biz-name", href=True):
				comp_name_url = item['href']
				urlname.append(comp_name_url)
			#print urlname	
			for urlnames in urlname:
				inurl = "https://www.yelp.com/" + urlnames
				indriver = webdriver.Chrome()
				indriver.get(inurl)
				html = indriver.page_source
				soupin = BeautifulSoup(html, "html.parser")
	
				for item in soupin.find_all("h1",class_="biz-page-title"):
					name = item.text.strip()

				for item in soupin.find_all("div", class_= "media-story"):
					next = item.find_next("address")
					if next in item:
						address = next.text.strip()
						print address
		
				for item in soupin.find_all("span", class_="biz-phone"):
					phone = item.text.strip()
	
				link = ""
				for item in soupin.find_all("span", class_="biz-website"):
		
					item.span.clear()
					url = item.a.text				
					link = link+ url
		
				writer.writerow([name.encode("ascii","ignore"), address, phone, link])
				indriver.close()
			print "bura gelir?"
			page_number += 10
f.close()
