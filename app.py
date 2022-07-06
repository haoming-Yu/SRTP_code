import json
import os
# import random

from flask import Flask, request

# flask app
app = Flask(__name__)


# root directory
@app.route("/")
def root():
    return {'status': 'success'}


# return data in the table
@app.route("/data", methods=['POST'])
def search():
    try:
        index_list = os.listdir('0021500368')
        data = []

        for index in index_list:
            with open(os.path.join('0021500368', index, 'metadata.json'), 'r') as f:
                metadata = json.load(f)
            data.append(metadata)
        
        return json.dumps({'status': 'succeed', 'data': data})

    except Exception as _:
        print(_)
        return json.dumps({'status': 'failed'})


# animation of trajectories
@app.route("/animation", methods=['POST'])
def movement():
    try:
        # 这里发来的请求需要加个参数 event_id = xxx，选择播放第几个回合的轨迹
        data = json.loads(request.get_data())
        possession_data_path = os.path.join('0021500368', str(data['event_id']))

        with open(os.path.join(possession_data_path, "metadata.json"), "r") as f:
            metadata = json.load(f)

        with open(os.path.join(possession_data_path, "movement_refined_shot_clock.json"), "r") as f:
            movement_data = json.load(f)

        offensive_team = metadata[metadata['offensive_team']]['teamid']
        start_index = metadata['possession_start_index'] + int(data['start_index'])
        end_index = metadata['possession_end_index']
        movement = []
        for item in movement_data[start_index: end_index + 1]:
            item['offensive_team'] = offensive_team
            if item['ball_position'][0] > 47:
                item['ball_position'][0] = 94 - item['ball_position'][0]
                item['ball_position'][1] = 50 - item['ball_position'][1]

                for player in item['player_position']:
                    player[2] = 94 - player[2]
                    player[3] = 50 - player[3]

            movement.append(item)

        return {'status': 'succeed', 'movement': movement, 'metadata': metadata}

    except Exception as _:
        print(_)
        return json.dumps({'status': 'failed'})


if __name__ == "__main__":
    app.run(threaded=True, host="127.0.0.1", port=5001, debug=True)
