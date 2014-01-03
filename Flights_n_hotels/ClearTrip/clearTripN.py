#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'sravan'
from checkbox.lib import url
import unittest
import time
import re
import json
import urllib2
import urllib
import urlparse
import csv
import sys
import unicodedata

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


def generate_url(base_url, fromAirport, fromCity, hcity, destCode, state, toCountry, flight_dep_date, flight_ret_date,
                 hotel_checkin_date, hotel_checkout_date):
    if base_url == '':
        print 'URL parameter is missing'
        return

    url_parts = list(urlparse.urlparse(base_url))

    dict_query = dict(urlparse.parse_qsl(url_parts[4], keep_blank_values=0, strict_parsing=0))

    #updating dictionary happens

    if fromAirport != '':
        dict_query['origin'] = fromAirport
    else:
        print 'fromAirport parameter is missing'
        return

    if fromCity != '':
        dict_query['from'] = fromCity
    else:
        print 'fromCity parameter is missing'
        return

    if hcity != '':
        dict_query['city'] = hcity
    else:
        print 'hcity parameter is missing'
        return

    if destCode != '':
        dict_query['dest_code'] = destCode
    else:
        print 'destCode parameter is missing'
        return

    if state != '':
        dict_query['state'] = state
    else:
        dict_query['state'] = ''
        #print 'state parameter is missing'
        #return

    if toCountry != '':
        dict_query['country'] = toCountry
    else:
        print 'toCountry parameter is missing'
        return

    if flight_dep_date != '':
        dict_query['depart_date'] = flight_dep_date
    else:
        print 'flight_dep_date parameter is missing'
        return

    if flight_ret_date != '':
        dict_query['return_date'] = flight_ret_date
    else:
        print 'flight_ret_date parameter is missing'
        return

    if hotel_checkin_date != '':
        dict_query['chk_in'] = hotel_checkin_date
    else:
        print 'hotel_checkin_date parameter is missing'
        return

    if hotel_checkout_date != '':
        dict_query['chk_out'] = hotel_checkout_date
    else:
        print 'hotel_checkout_date parameter is missing'
        return

    url_parts[4] = urllib.urlencode(dict_query)

    prepared_url = urlparse.urlunparse(url_parts)

    print "Prepared URL : " + prepared_url

    return prepared_url


def get_city_codes():
    cities = {}
    with open('city_codes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cities[row[0]] = row[1]
        #print cities
    return cities


def get_dest_codes():
    cities = {}
    with open('ct_normalizedCityCodes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cities[row[0]] = row[1]
            #print row[0]
            #cities.append(row[0])
    return cities


def selfCombine(list2Combine, length):
    listCombined = str(['list2Combine[i' + str(i) + ']' for i in range(length)]).replace("'", '') \
                   + 'for i0 in range(len( list2Combine ) )'
    if length > 1:
        listCombined += str(
            [' for i' + str(i) + ' in range( i' + str(i - 1) + ', len( list2Combine ) )' for i in range(1, length)]) \
            .replace("', '", ' ') \
            .replace("['", '') \
            .replace("']", '')
    listCombined = '[' + listCombined + ']'
    listCombined = eval(listCombined)
    return listCombined

#indexed to city_codes
def indexCities():
    dict = {}
    f = open('city_codes.csv', 'a+')
    for one in range(97, 123):
        query_parameter = chr(one)
        seed_url = "http://www.cleartrip.com/places/airports/search?string=" + query_parameter
        try:
            req = urllib2.Request(seed_url)
            response = urllib2.urlopen(req)
            str = response.read()
            decoded = json.loads(str)
            city_count = len(decoded)
            #print seed_url
            #print city_count
        except:
            print "No cities available with " + query_parameter
            # loading into dictionary cities with airports
        if (city_count > 0):
            i = 0
            while i < city_count:
                print decoded[i]['k'], decoded[i]['v']
                dict[decoded[i]['k']] = decoded[i]['v']
                f.write(decoded[i]['k'] + ',' + decoded[i]['v'])
                f.write('\n')
                # We can persist in Database
                i += 1
    f.close()
    #print dict.__sizeof__()
    return dict


def index_dest_codes(city_codes_file):
    #print city_codes_file
    cities = []
    with open(city_codes_file, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            all_items = []
            city_name = row[0]
            seed_url = "http://www.cleartrip.com/places/hac?&s=" + city_name
            try:
                req = urllib2.Request(seed_url)
                response = urllib2.urlopen(req)
                str = response.read()
                decoded = json.loads(str)
                city_count = len(decoded['r'])
                print seed_url
                print city_count
                if (city_count > 0):
                    i = 0
                    while i < city_count:
                        lis = []
                        dest_code = decoded['r'][i]['k']
                        city = decoded['r'][i]['cy']
                        state_cntry_code = decoded['r'][i]['sc']
                        state_code = decoded['r'][i]['s']
                        dest_code = unicodedata.normalize('NFKD', dest_code).encode('ascii', 'ignore')
                        lis.append(dest_code)
                        city = unicodedata.normalize('NFKD', city).encode('ascii', 'ignore')
                        lis.append(city)
                        state_cntry_code = unicodedata.normalize('NFKD', state_cntry_code).encode('ascii', 'ignore')
                        lis.append(state_cntry_code)
                        state_code = unicodedata.normalize('NFKD', state_code).encode('ascii', 'ignore')
                        if state_code == "":
                            lis.append("NA")
                        else:
                            lis.append(state_code)
                        all_items.append(lis)
                        i += 1
            except:
                e = sys.exc_info()[0]
                #print "Error: %s" % e
                #print "No cities available with " + seed_url
                pass
            print all_items
            make_csv(all_items, 'ct_dest_codes.csv')
    return cities


def make_csv(list, file_name):
    with open(file_name, 'a+') as f:
        writer = csv.writer(f)
        writer.writerows(list)
    f.close()


def get_Seed_urls():
    final_seed_url_list = []
    with open('clear_trip_seeds.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #print row[0]
            final_seed_url_list.append(row[0])
    csvfile.close()
    return final_seed_url_list


def get_city_list():
    cities = []
    with open('ct_normalizedCityCodes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #print row[0]
            cities.append(row[0])
    return cities


def get_states():
    states = {}
    with open('clear_trip_seeds.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #print row[0]
            states[row[0]] = row[4]
    return states


def getCityNames():
    city_names = {}
    with open('ct_normalizedCityCodes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            city_names[row[0]] = row[2]
    return city_names


def get_countries():
    states = {}
    with open('ct_normalizedCityCodes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            country = row[3]
            lis = country.split("-")
            country = lis[0]
            country = country.strip()
            states[row[0]] = country
    return states


"""
AN ASSUMPTION BEING MADE HERE
CHOOSING ONLY CITIES WITH AIRPORT AND HOTEL
"""


def normalize_cities():
    cities = {}
    city_states = {}
    with open('ct_dest_codes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cities[row[1]] = row[0]
            city_states[row[0]] = row[3]
            #print row[0],row[1]
    csvfile.close()
    with open('city_codes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        false_cnt = 0
        all_items = []
        for row in reader:
            #cities[row[1]]=row[0]
            if (cities.has_key(row[1])):
                #print "true"
                lis = []
                lis.append(row[0])
                dest_code = cities[row[1]]
                lis.append(dest_code)
                lis.append(row[1])
                lis.append(row[2])
                lis.append(city_states[dest_code])
                #print lis
                all_items.append(lis)
        print all_items
        make_csv(all_items, 'ct_normalizedCityCodes.csv')
    csvfile.close()
    print false_cnt

    return


def indexSeedUrls():
    f = open('clear_trip_seeds.csv', 'a+')
    final_seed_url_list = []
    #short_city_codes = get_city_codes()
    city_lis = get_city_list()
    cities = get_dest_codes()
    states = get_states()
    countries = get_countries()
    cityNames = getCityNames()
    listCombined = selfCombine(city_lis, 2)
    #date = 20
    base_url = "http://www.cleartrip.com/packages/results?origin=HYD&city=Bangalore&chk_out=3%2F02%2F2014&childs=0&from=HYD&adults=1&dest_code=32550&num_rooms=1&country=IN&children1=0&state=Karnataka&return_date=3%2F02%2F2014&infants=0&chk_in=1%2F02%2F2014&depart_date=1%2F02%2F2014&adults1=1"
    #generate_url(base_url,'HYD','HYD','Bangalore','32550','Karnataka','IN','1/02/2014','3/02/2014','1/02/2014','3/02/2014')
    #generate_url(base_url,fromAirport,fromCity,hcity,destCode,state,toCountry,flight_dep_date,flight_ret_date,hotel_checkin_date,hotel_checkout_date)
    for src, dest in listCombined:
        if (src != dest):
            #print src,dest
            fromAirport = src
            fromCity = src
            hcity = cityNames[dest]
            destCode = cities[dest]
            toCountry = countries[dest]
            if states[dest] != 'NA':
                state = states[dest]
            else:
                state = ''
            flight_dep_date = '1/02/2014'
            flight_ret_date = '3/02/2014'
            hotel_checkin_date = '1/02/2014'
            hotel_checkout_date = '3/02/2014'
            #print flight_dep_date,flight_ret_date,hotel_checkin_date,hotel_checkout_date,toCountry,fromAirport,fromCity,hcity,destCode,state
            url1 = generate_url(base_url, fromAirport, fromCity, hcity, destCode, state, toCountry, flight_dep_date,
                                flight_ret_date, hotel_checkin_date, hotel_checkout_date)
            fromAirport = dest
            fromCity = dest
            hcity = cityNames[src]
            destCode = cities[src]
            toCountry = countries[src]
            if states[dest] != 'NA':
                state = states[src]
            else:
                state = ''
            url2 = generate_url(base_url, fromAirport, fromCity, hcity, destCode, state, toCountry, flight_dep_date,
                                flight_ret_date, hotel_checkin_date, hotel_checkout_date)
            f.write(url1)
            f.write('\n')
            f.write(url2)
            f.write('\n')

    f.close()
    return


def getDetailsFromUrl(url):
    parsed_dict = {}
    parsed_dict = urlparse.parse_qs(urlparse.urlparse(url).query)
    #print parsed_dict
    return parsed_dict


def crawl():
    seed_urls = get_Seed_urls();
    cnt = 1
    fail_cnt = 0
    for url in seed_urls:
        if cnt == 2:
            break
        dict = getDetailsFromUrl(url)
        driver = webdriver.PhantomJS("/home/sravan/Dw/bin/phantomjs")
        #driver = webdriver.Firefox()
        #url = "http://www.cleartrip.com/packages/results?origin=ZAZ&city=Zagreb&chk_out=3%2F02%2F2014&childs=0&from=ZAZ&adults=1&dest_code=101463&num_rooms=1&country=HR&children1=0&state=&depart_date=1%2F02%2F2014&infants=0&chk_in=1%2F02%2F2014&return_date=3%2F02%2F2014&adults1=1"
        #url="http://www.cleartrip.com/packages/results?origin=Bangalore%2C+IN+-+Kempegowda+International+Airport+%28BLR%29&from=BLR&city=Mumbai&dest_code=33719&state=Maharashtra&country=IN&depart_date=26%2F12%2F2013&return_date=30%2F12%2F2013&chk_in=26%2F12%2F2013&chk_out=30%2F12%2F2013&num_rooms=1&adults1=1&adults=1&children1=0&childs=0&infants=0"
        print "Crawling...   " + str(cnt)
        driver.get(url)
        try:
            check = driver.find_element_by_xpath("//div/div[@class='warningMessage']/p[2]")
            fail_cnt += 1
            print "Msg from src : " + check.text
        except NoSuchElementException:
            all_items = []
            print 'Flight Info Available'
            blocks = driver.find_elements_by_xpath("//div/div[3]/div/nav/ul/li[@class ='listItem']")
            for b in blocks:
                #print b.text
                record = []
                try:
                    hotel_name = b.find_element_by_xpath(".//div/h2/a[@class ='hotelDetails truncate']").text
                    #print "Hotel name "+hotel_name
                    record.append(hotel_name.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    hotel_name = 'NA'
                    #print hotel_name
                    record.append(hotel_name)
                    pass
                try:
                    departure = b.find_element_by_xpath(".//div[1]/div[@class='timing']/span").text
                    #print "Departure time "+departure
                    record.append(departure.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    departure = 'NA'
                    #print departure
                    record.append(departure)
                    pass
                try:
                    arrival = b.find_element_by_xpath(".//div[2]/div[@class='timing']/span").text
                    #print "Arrival time "+arrival
                    record.append(arrival.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    arrival = 'NA'
                    #print arrival
                    record.append(arrival)
                    pass
                try:
                    going_duration = b.find_element_by_xpath(".//div[1]/div/small[@class='stops']").text
                    #print "Going duration "+going_duration
                    record.append(going_duration.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    going_duration = 'NA'
                    #print going_duration
                    record.append(going_duration)
                    pass

                try:
                    coming_duration = b.find_element_by_xpath(".//div[2]/div/small[@class='stops']").text
                    #print "Coming duration "+coming_duration
                    record.append(coming_duration.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    coming_duration = 'NA'
                    #print coming_duration
                    record.append(coming_duration)
                    pass

                try:
                    hotel_rating = b.find_element_by_xpath(".//div/div[@class='hotelRatings']/span[@title]")
                    hotel_rating = hotel_rating.get_attribute("title")
                    #print "Hotel rating "+ hotel_rating
                    record.append(hotel_rating.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    hotel_rating = 'NA'
                    #print hotel_roomtype
                    record.append(hotel_rating)
                    pass

                try:
                    tripAdv_rating = b.find_element_by_xpath(".//div/div/div/a/span[@title]")
                    tripAdv_rating = tripAdv_rating.get_attribute("title")
                    #print "tripAdv_rating rating "+ tripAdv_rating
                    record.append(tripAdv_rating.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    tripAdv_rating = 'NA'
                    #print hotel_roomtype
                    record.append(tripAdv_rating)
                    pass

                try:
                    hotel_roomtype = b.find_element_by_xpath(".//div/h3[@class='truncate span span24']").text
                    #print "Hotel type "+hotel_roomtype
                    record.append(hotel_roomtype.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    hotel_roomtype = 'NA'
                    #print hotel_roomtype
                    record.append(hotel_roomtype)
                    pass

                try:
                    original_price = b.find_element_by_xpath(".//small/span[@class='orgPrice']").text
                    #print "Original price "+original_price
                    record.append(original_price.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    original_price = 'NA'
                    #print original_price
                    record.append(original_price)
                    pass

                try:
                    current_price = b.find_element_by_xpath(".//h4/span[@class ='orgPrice']").text
                    #print "Current price "+current_price
                    record.append(current_price.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    current_price = 'NA'
                    #print original_price
                    record.append(current_price)
                    pass

                try:
                    price_savings = b.find_element_by_xpath(".//span[@class='savings']").text
                    #print "Price savings "+price_savings
                    record.append(price_savings.encode('ascii', 'ignore'))
                except NoSuchElementException:
                    price_savings = 'NA'
                    #print price_savings
                    record.append(price_savings)
                    pass
                    #url = remove_new_lines(url)
                record.append(dict['infants'][0])
                record.append(dict['childs'][0])
                record.append(dict['adults'][0])
                record.append(dict['adults1'][0])
                record.append(dict['num_rooms'][0])
                record.append(dict['country'][0])
                record.append(dict['children1'][0])
                record.append(url)
                print record
                all_items.append(record)
            print all_items
            #make_csv(all_items, 'ClearTrip_output.csv')
        cnt += 1
    driver.close()
    driver.quit()
    #cnt+=1
    return

#index_dest_codes('city_codes.csv')

#get_dest_codes()

#normalize_cities()

#indexSeedUrls()

crawl()


