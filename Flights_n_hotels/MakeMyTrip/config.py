__author__ = 'sravan'

# CONFIGURATION FOR MMT

NO_INFO_PAGE_SELECTOR = "//div[@class='flL error_text']"

BLOCK_SELECTOR = "//div/div[@class='shadow_genrator clearFix append_bottom']"

ACTUAL_PRICE_SELECTOR = ".//div/p[@class='actual_price']"

OFFER_PRICE_SELECTOR = ".//div/p[@class='offer_price']"

DISCOUNT_PRICE_SELECTOR = ".//div/p/span[@class='flR price_wdth']"

DEPART_FLIGHT_OPERATOR_SELECTOR = ".//div[1]/p[2]/span[@class='flight_name flL']"

RETURN_FLIGHT_OPERATOR_SELECTOR = ".//div[2]/p[2]/span[@class='flight_name flL']"

DEPARTURE_TIME_SELECTOR = ".//div[2]/div[1]/p[2]/span[3]/span[@class='grey_2']"

ARRIVAL_TIME_SELECTOR = './/div[2]/div[1]/p[2]/span[4]/span[@class="grey_2"]'

HOTEL_NAME_SELECTOR = ".//div/h2/a[@class='hotelNameLk']"

HOTEL_ADDRESS_SELECTOR = ".//div/div[1]/p[@class='hotelAddress clearFix']"

HOTEL_DESCRIPTION_SELECTOR = ".//div/div[1]/p[@class='leasure append_bottomHalf']"

ROOM_TYPE_SELECTOR = ".//div/div[1]/p[3]/span[@class='room_type_info flL']"

HOTEL_RATING_SELECTOR = ".//div[2]/p[2]/span[1]/span[@class='triper_rate green noBg flL']"

INTERNAL_STOP1_SELECTOR = ''

INTERNAL_STOP2_SELECTOR = ''

DURATION_SELECTOR = ""

#=================================================================#

PHANTOM_JS_PATH = "/home/sravan/Dw/bin/phantomjs"

CHROME_DRIVER_PATH = "/home/sravan/Dw/bin/chromedriver"
