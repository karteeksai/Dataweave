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
import config
import urllib
import urlparse
import itertools
import requests

def generate_url(base_url,fromCity,toCity,fromCountry,toCountry,hcity,hotel_checkin_date,hotel_checkout_date,flight_dep_date,flight_ret_date):

    if base_url=='':
        print 'URL parameter is missing'
        return

    url_parts = list(urlparse.urlparse(base_url))

    dict_query = dict(urlparse.parse_qsl(url_parts[4], keep_blank_values=0, strict_parsing=0))

    #updating dictionary happens

    if fromCountry!='':
        dict_query['fCountryFrom'] = fromCountry
    else:
        print 'fromCountry parameter is missing'
        return

    if toCountry!='':
        dict_query['fCountryTo'] = toCountry
    else:
        print 'toCountry parameter is missing'
        return

    if hcity!='':
        dict_query['city'] = hcity
    else:
        print 'hcity parameter is missing'
        return

    if fromCity!='':
        dict_query['frcity'] = fromCity
    else:
        print 'fromCity parameter is missing'
        return

    if toCity!='':
        dict_query['tocity'] = toCity
    else:
        print 'toCity parameter is missing'
        return

    if hotel_checkin_date!='':
        dict_query['sdate'] = hotel_checkin_date
    else:
        print 'hotel_checkin_date parameter is missing'
        return

    if hotel_checkout_date!='':
         dict_query['edate'] = hotel_checkout_date
    else:
        print 'hotel_checkout_date parameter is missing'
        return

    if flight_dep_date!='':
        dict_query['f_sdate'] = flight_dep_date
    else:
        print 'flight_dep_date parameter is missing'
        return

    if flight_ret_date!='':
        dict_query['f_edate'] = flight_ret_date
    else:
        print 'flight_ret_date parameter is missing'
        return

    url_parts[4] = urllib.urlencode(dict_query)

    prepared_url = urlparse.urlunparse(url_parts)

    #print "Prepared URL : "+prepared_url

    return prepared_url

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

def indexCities():
    f = open('mmt_city_codes.csv', 'a+')
    i=0
    while i<400:
        seed_url = 'http://www.makemytrip.com/mi8/core/?&st=flight&cc=%3C%3E_0_cityName_%23from_F&id=%23from&term=%3C%3E&s='+str(i)+'&o=50&mr=true'
        print seed_url
        try:
            req = urllib2.Request(seed_url)
            response = urllib2.urlopen(req)
            resp = response.read()
            decoded = json.loads(resp)
            rec_cnt = len(decoded['response']['docs'])
            k=1
            while k<rec_cnt:
                try:
                    country_code = decoded['response']['docs'][k]['fph_cty_s']
                    full_city_name = decoded['response']['docs'][k]['iata_label']
                    full_city_name = full_city_name.replace(",", "");
                    print country_code,full_city_name
                    f.write(full_city_name + ',' + country_code)
                    f.write('\n')
                except:
                    print 'city code could not be found'
                    pass
                k+=1
        except:
            print "No cities available with "
            pass
            # loading into dictionary cities with airports
        i+=50
    f.close()
    return ''

def get_city_list():
    cities = []
    with open('mmt_city_codes.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #print row
            cities.append(row)
    csvfile.close()
    return cities

def indexSeedUrls():
    seed_count = 0
    final_seed_url_list = []
    city_lis = get_city_list()
    #print city_lis
    f = open('mmt_seeds.csv', 'a+')
    listCombined = selfCombine(city_lis, 2)
    for src, dest in listCombined:
        if (src != dest):
            #print src,dest
            base_url = "http://fph.makemytrip.com/site/fph/search?isHotelCity=true&frcity=Hyderabad%2C+India+%28HYD%29&fCountryFrom=IN&tocity=Bangalore%2C+India+%28BLR%29&fCountryTo=IN&city=Bangalore%2C+India+%28BLR%29&hCountry=IN&f_sdate=02012014&f_edate=02062014&sdate=02012014&edate=02062014&trip=R&tripDup=R&hguest=1&fguest=1_0_0&curr=INR&adultAgeCount1=true&childAgeCount1=true"
            #print src[0],src[1],dest[0],dest[1]
            fromCity = src[0]
            toCity = dest[0]
            fromCountry = src[1]
            toCountry = dest[1]
            hcity = dest[0]
            flight_dep_date = '02012014'
            hotel_checkin_date = '02012014'
            hotel_checkout_date = '02042014'
            flight_ret_date = '02042014'
            url1 = generate_url(base_url,fromCity,toCity,fromCountry,toCountry,hcity,hotel_checkin_date,hotel_checkout_date,flight_dep_date,flight_ret_date)
            url2 = generate_url(base_url,toCity,fromCity,toCountry,fromCountry,fromCity,hotel_checkin_date,hotel_checkout_date,flight_dep_date,flight_ret_date)
            print url1
            print url2
            f.write(url1)
            f.write('\n')
            f.write(url2)
            f.write('\n')
            seed_count+=1
    f.close()
    print 'Seed count : '+str(seed_count)
    return final_seed_url_list

def get_Seed_urls():
    final_seed_url_list = []
    f = open("mmt_seeds.csv")
    for line in f:
        #print line
        final_seed_url_list.append(line)
    f.close()
    #print len(final_seed_url_list)
    return final_seed_url_list

def getDetailsFromUrl(url):
    parsed_dict = {}
    parsed_dict = urlparse.parse_qs(urlparse.urlparse(url).query)
    #print parsed_dict
    return parsed_dict

def remove_new_lines(str):
    str = str.splitlines()
    str = ' '.join(str)
    return str

def crawl():
    seed_urls = get_Seed_urls();
    cnt = 1
    fail_cnt=0
    for url in seed_urls:
        if cnt == 20:
            break
        #url = "http://fph.makemytrip.com/site/fph/search?isHotelCity=true&frcity=Hyderabad%2C+India+%28HYD%29&fCountryFrom=IN&tocity=Bangalore%2C+India+%28BLR%29&fCountryTo=IN&city=Bangalore%2C+India+%28BLR%29&hCountry=IN&f_sdate=02012014&f_edate=02062014&sdate=02012014&edate=02062014&trip=R&tripDup=R&hguest=1&fguest=1_0_0&curr=INR&adultAgeCount1=true&childAgeCount1=true"
        details = getDetailsFromUrl(url)
        source = details['frcity']
        destination = details['tocity']
        flight_dep_date = details['f_sdate']
        flight_ret_date = details['f_edate']
        hotel_checkin_date = details['sdate']
        hotel_checkout_date = details['edate']
        hotel_city = details['city']
        #print source, destination, flight_dep_date,flight_ret_date,hotel_checkin_date,hotel_checkout_date,hotel_city
        driver = webdriver.PhantomJS(config.PHANTOM_JS_PATH)
        #driver = webdriver.Chrome(executable_path=config.CHROME_DRIVER_PATH)
        #driver = webdriver.Firefox()
        #driver.set_page_load_timeout(20)
        print "Crawling..." + url
        #driver.implicitly_wait(30)
        #url = "http://fph.makemytrip.com/site/fph/search?isHotelCity=true&frcity=Goa%2C+India+%28GOI%29&fCountryFrom=IN&tocity=Hyderabad%2C+India+%28HYD%29&fCountryTo=IN&city=Hyderabad%2C+India+%28HYD%29&hCountry=IN&f_sdate=12312013&f_edate=01022014&sdate=12312013&edate=01022014&trip=R&tripDup=R&hguest=1&fguest=1_0_0&curr=INR&adultAgeCount1=true&childAgeCount1=true&infantCount1=true"
        driver.get(url)
        time.sleep(5)
        #print driver.page_source
        try:
            check = driver.find_element_by_xpath(config.NO_INFO_PAGE_SELECTOR)
            print "Msg from src : " + check.text
            fail_cnt+=1
        except NoSuchElementException:
            all_items = []
            blocks = driver.find_elements_by_xpath(config.BLOCK_SELECTOR)
            print 'Flight Info Available'
            for b in blocks:
                record = []
                b.find_element_by_xpath(".//p/span/a[@class='flL view_details']").click()
                time.sleep(3)
                #print b.text
                try:
                    actual_price = b.find_element_by_xpath(config.ACTUAL_PRICE_SELECTOR).text
                    #print actual_price
                    actual_price = actual_price.replace(',', '')
                    record.append(actual_price)
                except NoSuchElementException:
                    actual_price = 'NA'
                    record.append(actual_price)
                    pass
                try:
                    offer_price = b.find_element_by_xpath(config.OFFER_PRICE_SELECTOR).text
                    offer_price = offer_price.replace(',', '')
                    record.append(offer_price)
                except NoSuchElementException:
                    offer_price = 'NA'
                    record.append(offer_price)
                    pass
                try:
                    discount_price = b.find_element_by_xpath(config.DISCOUNT_PRICE_SELECTOR).text
                    discount_price = discount_price.replace(',', '')
                    record.append(discount_price)
                except NoSuchElementException:
                    discount_price = 'NA'
                    record.append(discount_price)
                    pass
                record.append(source[0])
                record.append(destination[0])
                record.append(flight_dep_date[0])
                record.append(flight_ret_date[0])
                record.append(hotel_checkin_date[0])
                record.append(hotel_checkout_date[0])
                record.append(hotel_city[0])
                #record.append(travel_date)

                try:
                    departure = b.find_element_by_xpath(config.DEPARTURE_TIME_SELECTOR).text
                    departure = departure.replace(',', '')
                    dep = remove_new_lines(departure)
                    record.append(dep)
                except NoSuchElementException:
                    departure = 'NA'
                    record.append(departure)
                    pass
                try:
                    arrival = b.find_element_by_xpath(config.ARRIVAL_TIME_SELECTOR).text
                    arrival = remove_new_lines(arrival)
                    record.append(arrival)
                except NoSuchElementException:
                    arrival = 'NA'
                    record.append(arrival)
                    pass
                try:
                    hotel_name = b.find_element_by_xpath(config.HOTEL_NAME_SELECTOR).text
                    hotel_name = remove_new_lines(hotel_name)
                    record.append(hotel_name)
                except NoSuchElementException:
                    hotel_name = 'NA'
                    record.append(hotel_name)
                    pass
                try:
                    hotel_add = b.find_element_by_xpath(config.HOTEL_ADDRESS_SELECTOR).text
                    hotel_add = remove_new_lines(hotel_add)
                    record.append(hotel_add)
                except NoSuchElementException:
                    hotel_add = 'NA'
                    record.append(hotel_add)
                    pass
                try:
                    hotel_desc = b.find_element_by_xpath(config.HOTEL_DESCRIPTION_SELECTOR).text
                    hotel_desc = remove_new_lines(hotel_desc)
                    record.append(hotel_desc)
                except NoSuchElementException:
                    hotel_desc = 'NA'
                    record.append(hotel_desc)
                    pass
                try:
                    room_type = b.find_element_by_xpath(config.ROOM_TYPE_SELECTOR).text
                    room_type = remove_new_lines(room_type)
                    record.append(room_type)
                except NoSuchElementException:
                    room_type = 'NA'
                    record.append(room_type)
                    pass
                try:
                    hotel_rating = b.find_element_by_xpath(config.HOTEL_RATING_SELECTOR).text
                    hotel_rating = remove_new_lines(hotel_rating)
                    record.append(hotel_rating)
                except NoSuchElementException:
                    hotel_rating = 'NA'
                    record.append(hotel_rating)
                    pass
                url = remove_new_lines(url)
                record.append(url)
                print record
                all_items.append(record)
            #make_csv(all_items,'makeMyTrip.csv')

        driver.close()
        driver.quit()
        #print record
        cnt += 1
    print "Failed Url's = "+str(fail_cnt)

def make_csv(list,file_name):
    with open(file_name, 'a+') as f:
        writer = csv.writer(f)
        writer.writerows(list)
    f.close()

#== RUN FOR ONCE == INDEXES CITIES INTO mmt_city_codes.csv
#indexCities()
#== RUN FOR ONCE == INDEXES SEED_URLS INTO seeds.csv
#indexSeedUrls()

crawl()

print 'done...'