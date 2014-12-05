import json
import urllib2
from flask import jsonify, make_response

with open('config.json') as f:
    config = json.load(f)


# return a failed call - useful for 400 errors, 500 errors, etc
def abort(data, code):
    response = {'data': data, 'success': False}

    return make_response(jsonify(response), code)


# return a successful call
def success(data):
    response = {'data': data, 'success': True}

    return make_response(jsonify(response), 200)


# given a response from abort/success, get a json object


# RIOT static API call
def static_api(call, region='na'):
    url = config['STATIC_API'].format(region=region, call=call)
    return riot_api(url)


# RIOT API call (adds api_key and returns it nicely)
def riot_api(url):
    # check if the call has parameters already
    url += '&' if '?' in url else '?'
    url += 'api_key={key}'.format(key=config['RIOT_API_KEY'])

    print 'API CALL: {url}'.format(url=url)

    try:
        data = urllib2.urlopen(url).read()
    except:
        return None

    return json.loads(data)


# to get the champion names, call the riot static api
champion_data = static_api('champion?dataById=true')
champion_data = champion_data['data']
# same for summoner spell names, riot is retarded
summoner_spell_data = static_api('summoner-spell?dataById=true')
summoner_spell_data = summoner_spell_data['data']
# and items, god forbid they do this in a more normal fashion
item_data = static_api('item')
item_data = item_data['data']
