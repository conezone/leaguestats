#!venv/bin/python
from app import ls
ls.run(debug=ls.config['DEBUG'], host='0.0.0.0', port=80)
