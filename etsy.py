#!/usr/bin/env python

import requests
import json
import backoff
import sys

RETRY_LIMIT = 4

SEARCH_URL = "https://swapi.co/api/people/?search="

def search(value):
    response = http_get(SEARCH_URL + str(value))
    return response


class ThrottlingException(Exception):
    pass

def giveup(exc):
    print(exc)


@backoff.on_exception(backoff.expo,
                      ThrottlingException,
                      max_tries=2,
                      on_giveup=giveup)
def http_get(endpoint):
    resp = requests.get(endpoint)
    if resp.status_code == 429:
        raise ThrottlingException()
    return resp.json()

def get_char_info(name):
    js = search(name)
    try:
      result = js['results'][0]
    except IndexError, e:
      raise e

    charachter_name = result['name']
    species_name, lifespan = get_species(result["species"][0])
    homeworld = get_homeworld(result["homeworld"])
  
    return charachter_name,species_name,lifespan,homeworld
      
def print_info(charachter_name,species_name,lifespan,homeworld):
    print "Name of Charachter is {}".format(charachter_name) + "\n"
    print "Name of Species is {}".format(species_name) + "\n"
    print "Avg lifespan is {}".format(lifespan) + "\n"
    print "Name of Homeworld is {}".format(homeworld) + "\n"
      
def get_species(species):
    js = http_get(species)
    species_name = js.get("name")
    species_lifespan = js.get("average_lifespan")
    return species_name, species_lifespan
      
def get_homeworld(homeworld):
    js = http_get(homeworld)
    homeworld = js.get("name")
    return homeworld

# name of char comes from parent endpoint
# name of species comes from species endpoint
# avg lifespan comes from species endpoint
# name of homeworld comes from planets endpoint

if __name__ == "__main__":
    name = "r2"
    try:
        charachter_name,species_name,lifespan,homeworld = get_char_info(name)
    except IndexError:
        print("No info retured for {}".format(name))
        sys.exit(1)
    except ThrottlingException:
        print("API Rate Limit reached, try again later")


    print_info(charachter_name,species_name,lifespan,homeworld)


 
