import datetime
from app import common
from flask import Blueprint

path = common.config['API_PATH']
summoners_api = Blueprint('summoners', __name__, template_folder='templates')


@summoners_api.route(path + '/summoners/<int:summoner_id>', methods=['GET'])
def get_summoner(summoner_id=None):
    data = {
        'summoner': get_basic_info(summoner_id),
        'matches': get_ranked_games(summoner_id),
        'leagues': get_league_data(summoner_id)
    }

    return common.success(data)


def get_basic_info(summoner_id=None, summoner_name=None, region='na'):
    if not summoner_id and not summoner_name:
        return common.abort('Missing SUMMONER_ID or SUMMONER_NAME', 403)

    # if we have the summoner_id, use that
    if summoner_id:
        call = summoner_id
    else:
        summoner_id = summoner_name
        call = 'by-name/{id}'.format(id=summoner_id)

    url = common.config['SUMMONER_API'].format(region=region, call=call)
    summoner = common.riot_api(url)

    if summoner:
        return summoner[str(summoner_id).lower()]

    return None


def get_ranked_games(summoner_id=None, region='na'):
    if not summoner_id:
        return common.abort('Missing SUMMONER_ID', 403)

    url = common.config['MATCH_HISTORY_API'].format(region=region,
                                                    call=summoner_id)
    matches = common.riot_api(url)
    # TODO: pull that info from our own DB, and if that fails call the API

    if matches == {} or not matches:
        return None

    # We don't care about everything they send, just track:
    #   Win/Loss, Game Type, Champion, Summoners, Items, K/D/A, CS
    #   TODO: Enemy Champions (separate API call) so user can pick lane enemy
    return_matches = []
    for match in matches['matches']:
        stats = match['participants'][0]
        gameType = match['queueType']
        champId = stats['championId']
        summoners = (
            common.summoner_spell_data[str(stats['spell1Id'])]['key'],
            common.summoner_spell_data[str(stats['spell2Id'])]['key']
        )
        champion = common.champion_data[str(champId)]['key']
        length = match['matchDuration']
        m, s = divmod(length, 60)
        h, m = divmod(m, 60)
        if h:
            length = "{h}:{m:0>2d}:{s:0>2d}".format(h=h, m=m, s=s)
        else:
            length = "{m:0>2d}:{s:0>2d}".format(m=m, s=s)
        created = match['matchCreation']/1000
        created = datetime.datetime.fromtimestamp(created)
        created = created.strftime('%m-%d-%Y')

        # drop into the actual game stats
        stats = stats['stats']
        winner = stats['winner']
        items = []
        for i in ['item0', 'item1', 'item2', 'item3',
                  'item4', 'item5', 'item6']:
            if stats[i] == 0:
                items.append((stats[i], None))
            else:
                items.append((stats[i],
                             common.item_data[str(stats[i])]['name']))

        kda = (stats['kills'], stats['deaths'], stats['assists'])
        minions = stats['minionsKilled']
        jungle_creeps = stats['neutralMinionsKilled']
        link = common.config['SCOREBOARD'].format(region=region.upper(),
                                                  match_id=match['matchId'])

        return_matches.append({
            'id': match['matchId'],
            'winner': winner,
            'gameType': gameType,
            'champion': champion,
            'champId': champId,
            'summoners': summoners,
            'items': items,
            'kills': kda[0],
            'deaths': kda[1],
            'assists': kda[2],
            'minions': minions,
            'jungle_creeps': jungle_creeps,
            'link': link,
            'duration': length,
            'created': created
        })
    return_matches.reverse()
    return return_matches


def get_league_data(summoner_id=None, region='na'):
    if not summoner_id:
        return common.abort('Missing SUMMONER_ID', 403)

    url = common.config['LEAGUES_API'].format(region=region, call=summoner_id)
    leagues = common.riot_api(url)
    # TODO: pull that info from our own DB, and if that fails call the API

    if leagues == {} or not leagues:
        return None

    return_leagues = {}
    for league in leagues[str(summoner_id)]:
        gameType = league['queue']
        l = {}
        l['leagueName'] = league['name']
        l['tier'] = league['tier']
        l['participantId'] = league['participantId']
        for entry in league['entries']:
            if l['participantId'] == entry['playerOrTeamId']:
                l['points'] = entry['leaguePoints']
                l['new'] = entry['isFreshBlood']
                l['hotStreak'] = entry['isHotStreak']
                l['inactive'] = entry['isInactive']
                l['veteran'] = entry['isVeteran']
                l['playerOrTeamName'] = entry['playerOrTeamName']
                l['division'] = entry['division']
                l['wins'] = entry['wins']

        return_leagues[gameType] = l

    return return_leagues
