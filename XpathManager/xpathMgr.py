__author__ = 'sravan'

from checkbox.lib import url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest,time, re
import json
import urllib2
import urlparse
import csv
import urllib
import urlparse
import itertools
import requests
import MySQLdb

def getXpath(id):
    dict = {}
    # Open database connection
    db = MySQLdb.connect("127.0.0.1","root","","regex_manager2" )
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    sql = "SELECT * FROM source_xpath_config \
            WHERE id = '%d'" % (id)
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       for row in results:
          field = row[3]
          xpath = row[4]
          dict[field] = xpath
    except:
       print "Error: unable to fecth data"
    db.close()
    print dict
    return dict

def get_Seed_urls():
    final_seed_url_list = []
    f = open("pw_category_urls.csv")
    for line in f:
        #print line
        final_seed_url_list.append(line)
    f.close()
    print len(final_seed_url_list)
    return final_seed_url_list

def getId(url):
    print "given url : "+url
    dict = {}
    parts = urlparse.urlparse(url)
    cleaned_url = parts.netloc
    cln_url=cleaned_url.replace("www.","")
    print "after cleaning : "+cln_url
    db = MySQLdb.connect("127.0.0.1","root","","regex_manager2" )
    cursor = db.cursor()
    sql = "SELECT id FROM regex_manager2.source_details where source_url LIKE '%"+cln_url+"%'";
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       for row in results:
          cart_id = row[0]
    except:
       print "Error: unable to fecth data"
    db.close()
    return cart_id

def crawl(url):
    src_id = getId(url)
    xpaths = getXpath(src_id)
    driver = webdriver.PhantomJS("/home/sravan/Dw/bin/phantomjs")
    #driver = webdriver.Firefox()
    print "Crawling..." + url
    #driver.implicitly_wait(30)
    driver.get(url)
    try:
        check = driver.find_element_by_xpath(".//body/div[1]/div[2]/div[1]/div[2]/p")
        print "Msg from src : " + check.text
    except NoSuchElementException:
        record = []
        print xpaths['available_price']
        try:
            availablePrice = driver.find_element_by_xpath(xpaths['available_price']).text
            #print availablePrice
            availablePrice = availablePrice.replace(',', '')
            record.append(availablePrice)
        except NoSuchElementException:
            availablePrice = 'NA'
            record.append(availablePrice)
            pass
        try:
            MRP = driver.find_element_by_xpath(xpaths['mrp']).text
            #print availablePrice
            MRP = MRP.replace(',', '')
            record.append(MRP)
        except NoSuchElementException:
            MRP = 'NA'
            record.append(MRP)
            pass
        try:
            description = driver.find_element_by_xpath(xpaths['description']).text
            #print availablePrice
            description = description.replace(',', '')
            record.append(description)
        except NoSuchElementException:
            description = 'NA'
            record.append(description)
            pass
        try:
            category = driver.find_element_by_xpath(xpaths['category']).text
            #print availablePrice
            category = category.replace(',', '')
            record.append(category)
        except NoSuchElementException:
            category = 'NA'
            record.append(category)
            pass
        try:
            meta = driver.find_element_by_xpath(xpaths['meta']).text
            #print availablePrice
            meta = availablePrice.replace(',', '')
            record.append(meta)
        except NoSuchElementException:
            meta = 'NA'
            record.append(meta)
            pass
        try:
            stock = driver.find_element_by_xpath(xpaths['stock']).text
            #print availablePrice
            stock = stock.replace(',', '')
            record.append(stock)
        except NoSuchElementException:
            stock = 'NA'
            record.append(stock)
            pass
        try:
            seller = driver.find_element_by_xpath(xpaths['seller']).text
            #print availablePrice
            seller = seller.replace(',', '')
            record.append(seller)
        except NoSuchElementException:
            seller = 'NA'
            record.append(seller)
            pass
        try:
            shipping_time = driver.find_element_by_xpath(xpaths['shipping_time']).text
            #print availablePrice
            shipping_time = availablePrice.replace(',', '')
            record.append(shipping_time)
        except NoSuchElementException:
            shipping_time = 'NA'
            record.append(shipping_time)
            pass
        try:
            title = driver.find_element_by_xpath(xpaths['title']).text
            #print availablePrice
            title = title.replace(',', '')
            record.append(title)
        except NoSuchElementException:
            title = 'NA'
            record.append(title)
            pass
        print record
    driver.close()
    driver.quit()

url = "http://www.flipkart.com/google-nexus-4/p/itmdzsgjkemg8mzp?q=Google+Nexus+4&as=on&as-show=on&otracker=start&as-pos=p_1&pid=MOBDZBZ9FSEKF2TVs"

crawl(url)

#getId(url)
