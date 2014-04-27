#!/usr/bin/env python
# -*- coding: UTF8 -*-
# @see http://www.python.org/dev/peps/pep-0263

import requests # HTTP requests made easy
import locale   # Needed for Finnish number formatting (comma as decimal separator)
import json     # JSON encoding support
from bs4 import BeautifulSoup as BSoup # HTML parsing made easy

locale.setlocale(locale.LC_NUMERIC, 'fi_FI.UTF-8')

class Apartment:
  EXPECTED_DATAFIELDS = 11

  def __init__(self, data):
    self.neighborhood  = data[0].string.strip() # Name of the neighborhood apartment is in
    self.floor_plan    = data[1].string.strip() # Floor plan as Finnish string
    self.rooms         = self.__get_rooms()      # Number of rooms as integer
    self.type          = data[2].string.strip()
    self.area          = locale.atof(data[3].string.encode('ascii'))
    self.price         = float(data[4].string)
    self.built         = int(data[6].string)    # year of construction
    self.floor         = data[7].string.strip() # floor in format: x/y
    self.has_elevator  = False if (data[8].string.lower() == 'ei') else True
    self.condition     = data[9].string  # Finnish string describing condition
    self.energy_rating = data[10].string # String describing energy efficiency of building

  def __str__(self):
    return 'Apartment in %s; %s; %s; %d m2, %d €, built: %d' % (self.neighborhood, self.floor_plan, self.type, self.area, self.price, self.built)

  def __get_rooms(self):
    if self.floor_plan[0].isdigit():
      return int(self.floor_plan[0])
    else:
      return -1

  def price_per_sqmeter(self):
    return round(self.price / self.area, 2)

  def price_per_sqfoot(self):
    return round(self.price / self.area_in_sqfeet(), 2)

  def area_in_sqfeet(self):
    return ruond(self.area / pow(.3048, 2), 2)

  def get_as_dict(self):
    return self.__dict__

  def get_as_json(self):
    return json.dumps(self.get_as_dict())

class ApartmentController:
  def __init__(self):
    self.apartments = []

  def get(self, index):
    return self.apartments[index]

  def add_from_bs4row(self, bs4_row):
    data = bs4_row.find_all('td')
    if ( len(data) == Apartment.EXPECTED_DATAFIELDS ):
      self.apartments.append( Apartment(data) )
      return True
    else:
      return False

  def count(self):
    return len(self.apartments)

  def get_as_dict(self):
    list = []
    for apartment in self.apartments:
      list.append(apartment.get_as_dict())
    return list

  def get_as_json(self):
    return json.dumps(self.get_as_dict())


# MAIN
if __name__ == '__main__':
  url = 'http://asuntojen.hintatiedot.fi/haku/'
  # c:  city name (string)
  # cr: search by: 1 = by postal code, 2 = by neighborhood (string)
  # ns: neighborhood name (string)
  # ps: postal code (string or list)
  # r:  amount of rooms (int or list)
  # h:  apartment type: 1 = kerrostalo, 2 = rivitalo, 3 = omakotitalo (string or list)
  # amin: minimum area (float)
  # amax: maximum area (float)
  post_data = { 'cr': 2, 'c': 'Helsinki', 'ns': 'Kallio', 'h': 1, 'r': 2, 'search': 1, 'amin': 47, 'amax': 50 }
  r = requests.post(url, data=post_data)
  resp = r.text.encode('utf-8')

  soup = BSoup(resp)
  apartments = ApartmentController()

  for bs4row in soup.find(id='mainTable').find_all('tbody')[2].find_all('tr'):
    apartments.add_from_bs4row( bs4row )

  print 'Content-Type: application/json'
  print # Empty line needed to separate HTTP response header from response body
  print apartments.get_as_json()