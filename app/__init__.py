from flask import Flask
from api.v1.summoners import summoners_api
import common

ls = Flask(__name__)
#ls.config.from_object('settings')
ls.config.update(common.config)
ls.register_blueprint(summoners_api)

from app import views
