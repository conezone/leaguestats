from app import ls, common
from api.v1 import summoners
from flask import render_template, request, redirect, url_for
import json


@ls.route('/')
@ls.route('/index')
def index():
    return render_template('index.html',
                           title='Home')


@ls.route('/summoners/<int:summoner_id>')
def summoner(summoner_id=None):
    if not summoner_id:
        return common.abort('Requires a SUMMONER_ID', 403)

    response = summoners.get_summoner(summoner_id)
    response = json.loads(response.response[0])

    if not response['success']:
        return render_template('error.html',
                               error=response['data'])

    summoner = response['data']
    return render_template('summoner.html',
                           matches=summoner['matches'],
                           summoner=summoner['summoner'],
                           leagues=summoner['leagues'],
                           game_version=common.config['GAME_VERSION'],
                           title=summoner['summoner']['name'] + "'s Profile")


@ls.route('/search', methods=['POST'])
def search():
    # search for summoners and redirect to the summoner page
    # TODO: search for champions as well (first?)
    summoner_name = request.form['search']
    if summoner_name == '':
        info = None
    else:
        info = summoners.get_basic_info(summoner_name=summoner_name)

    if info:
        return redirect(url_for('summoner', summoner_id=info['id']))
    return render_template('error.html',
                           error='User not found')


# TODO: Remove this test function
@ls.route('/test/<string:call>/<string:param>')
def test_static(call, param):
    test = common.static_api(call + '/' + param + '?champData=image')
    print test
    #pprint.pprint(test[0].response)
    #return common.abort('test', 200)
    if not test:
        return common.abort('Static API failed', 500)
    return test
