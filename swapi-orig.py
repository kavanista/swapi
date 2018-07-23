#!/usr/bin/env python

import requests
import json
import backoff

URL = "https://swapi.co/api/people/?search="

def http_get(value):
  resp = requests.get(URL + str(value))
  assert resp.status_code == 200,"Star Wars API service down"
  return resp.content

def main():
  name = "r2"
  json_result = http_get(name)
  js = json.loads(json_result)
  
  results = js['results']

  for result in results:
      charachter_name = result['name']
      name_of_species = get_species(result["species"][0])
      species_name, lifespan = get_species(result["species"][0])
      homeworld = get_homeworld(result["homeworld"])
      print "Name of Charachter is {}".format(charachter_name) + "\n"
      print "Name of Species is {}".format(species_name) + "\n"
      print "Avg lifestyle is {}".format(lifespan) + "\n"
      print "Name of Homeworld is {}".format(homeworld) + "\n"
      

      
def get_species(species):
  species_resp = requests.get(species)
  species_content = json.loads(species_resp.content)
  species_name = species_content.get("name")
  species_lifespan = species_content.get("average_lifespan")
  return species_name, species_lifespan
      
def get_homeworld(homeworld):
  planets_resp = requests.get(homeworld)
  planet_content = json.loads(planets_resp.content)
  homeworld = planet_content.get("name")
  return homeworld
  
      
    
# name of char comes from parent endpoint
# name of species comes from species endpoint
# avg lifespan comes from species endpoint
# name of homeworld comes from planets endpoint

if __name__ == "__main__":
  main()
  
