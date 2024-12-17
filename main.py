from injuries import get_injuries
from depth import get_depth
from out_or_d2d import get_status
from playerprofile import get_player_profile
from flask import Flask, jsonify
#from flask_cors import CORS, cross_origin

app = Flask(__name__)
#cors = CORS(app) # allow CORS for all domains on all routes.
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def greet():
    return jsonify(message="NBA API for thenbalog")

@app.route('/injuries', methods=['GET'])
def getInjuries():
    return get_injuries()


@app.route('/depth', methods=['GET'])
def getDepth():
    return get_depth()

@app.route('/status', methods=['GET'])
def getStatus():
    return get_status()

@app.route('/playerprofile', methods=['GET'])
def getPlayerProfile():
    return get_player_profile()

if __name__ == '__main__':
    app.run(debug=True)