import responses
from swapi import http_get
from swapi import get_char_info, search
from swapi import ThrottlingException
import json

@responses.activate
def testsearch():
    search_response = {
    "count": 1, 
    "results": [
        {
            "name": "R2-D2", 
            "homeworld": "https://swapi.co/api/planets/8/", 
            "species": [
                "https://swapi.co/api/species/2/"
            ], 
            "url": "https://swapi.co/api/people/3/"
        }
    ]
    }
 
    responses.add(responses.GET,"https://swapi.co/api/people/?search=r2",json=search_response,status=200)
    js = search("r2")
    assert js["count"] == 1
    assert js["results"][0]["name"] == "R2-D2"

    species_response = {
        "name": "Droid", 
        "average_lifespan": "indefinite", 
        "url": "https://swapi.co/api/species/2/"
    }    

    responses.add(responses.GET,"https://swapi.co/api/species/2/",json=species_response,status=200)
    
    planets_response = { 
        "name": "Naboo", 
    }

    responses.add(responses.GET,"https://swapi.co/api/planets/8/",json=planets_response,status=200)

    charachter_name,species_name,lifespan,homeworld = get_char_info("r2")
    assert charachter_name == "R2-D2"
    assert species_name == "Droid"
    assert lifespan == "indefinite"
    assert homeworld == "Naboo"

@responses.activate
def test_empty_search():
    bogus_response = {
    "count": 0, 
    "results": []
    }
    responses.add(responses.GET,"https://swapi.co/api/people/?search=bogus",json=bogus_response,status=200)
    try:
        get_char_info("bogus")
        assert False
    except Exception, e:
        assert isinstance(e, IndexError)


@responses.activate
def test_throttling():
    responses.add(responses.GET,"https://swapi.co/api/people/?search=r2",json={},status=429)
    try:
        get_char_info("r2")
        assert False
    except Exception, e:
        assert isinstance(e, ThrottlingException)

        
    

        


   
