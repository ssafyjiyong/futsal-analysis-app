from flask import Flask, jsonify, request, make_response
from service.track_service import track_service
from service import util
import time

app = Flask(__name__)

@app.route("/api/flask/track", methods=['POST'])
def track_request():
    args_dict = request.get_json()
    instance = track_service()
    source = args_dict.get('url')
    game_id = args_dict.get('game_id')
    start = time.time()
    if source is None or game_id is None:
        return make_response("bad req",400)
    else:
        result = instance.get_result(source)
        result.update({'game_id':game_id})
        
    end = time.time()
    
    print((end-start)/60)
    
    return make_response(jsonify(result), 200)
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=False)
    
    