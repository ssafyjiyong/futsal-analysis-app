from service.tracking.model import model
from service import util
import requests
import cv2
import time

class track_service:
    def __init__(self):
        self.source = None
        self.team_A_players = []
        self.team_B_players = []
        self.team_A_goal_post = {}
        self.team_B_goal_post = {}
        self.ball = {
            'x':960,
            'y':540
        }
        self.field = {
            'x1': 0,
            'x2': 1920,
            'y1': 0,
            'y2': 1080
        }
        self.team_A_player_id_map = {}
        self.team_B_player_id_map = {}
        self.lost_players = []
        self.model = model()

    def get_result(self, source):
        self.source = source
        save_path = './service/video/'
        filename = source.split('/')[-1]
        
        start = time.time()
        with requests.get(source, stream=True) as r:
            p = 0
            with open(save_path+filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=100*1024*1024):
                    p+=1
                    print(p)
                    f.write(chunk)
        end = time.time()
        print(end-start)
        result = {'data': []}
         
        cap = cv2.VideoCapture(save_path+filename)

        frame_num = 0
        defined = False
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                frame_num += 1
                track_result = eval(self.model.track(frame)[0].tojson())
                objs_field, objs_goal_post, objs_player = util.obj_divider(track_result)

                self.field = util.validator_field(self.field, objs_field)
                
                detect_result = eval(self.model.detect(frame)[0].tojson())
                if detect_result != None:
                    temp = util.validator_ball(self.field, detect_result)
                    if temp != None:
                        self.ball = temp
                
                if not defined:
                    result_info = util.define_objs(self.field, objs_goal_post, objs_player)
                    self.team_A_players = result_info.get('team_A_players')
                    self.team_B_players = result_info.get('team_B_players')
                    self.team_A_goal_post = result_info.get('team_A_goal_post')
                    self.team_B_goal_post = result_info.get('team_B_goal_post')
                    self.team_A_player_id_map = result_info.get('team_A_player_id_map')
                    self.team_B_player_id_map = result_info.get('team_B_player_id_map')
#                     print('---------------------------------------')
#                     print(self.team_A_player_id_map)
#                     print('---------------------------------------')
#                     print(self.team_B_player_id_map)
#                     print('---------------------------------------')
                    if self.team_A_player_id_map is not None and self.team_B_player_id_map is not None and self.team_A_goal_post is not None and self.team_B_goal_post is not None and self.team_A_players is not None:
                        defined = True
                else:
                    if util.validator_goal_post(objs_goal_post) is not None:
                        self.team_A_goal_post, self.team_B_goal_post = util.validator_goal_post(objs_goal_post)
                    self.team_A_players, self.team_B_players, self.team_A_player_id_map, self.team_B_player_id_map, self.lost_players = util.validator_player(
                        self.field, self.team_A_player_id_map, self.team_B_player_id_map, self.lost_players,
                        objs_player)
                    
                result.get('data').append({
                    'frame_num': frame_num,
                    'ball': self.ball,
                    'team_A_goal_post': self.team_A_goal_post,
                    'team_B_goal_post': self.team_B_goal_post,
                    'team_A_players': self.team_A_players,
                    'team_B_players': self.team_A_players
                })
                print(frame_num)
            else:
                cap.release()
        '''
        보간
        '''
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@done@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return result
