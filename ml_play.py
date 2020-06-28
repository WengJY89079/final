
from os import path
import pickle

class MLPlay:
    def __init__(self, player):
        self.player = player
        with open(path.join(path.dirname(__file__), 'tree1.pickle'), 'rb') as f:
                self.tree = pickle.load(f)
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        self.coin_num = 0
        self.computer_cars = []
        self.coins_pos = []
        print("Initial ml script")

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        self.car_pos = scene_info[self.player]
        for car in scene_info["cars_info"]:
            if car["id"] == self.player_no:
                self.car_vel = car["velocity"]
                self.coin_num = car["coin_num"]
        self.computer_cars = scene_info["computer_cars"]
        if scene_info.__contains__("coins"):
            self.coins_pos = scene_info["coins"]

        carX = -1
        carY = -1
        forward = -1
        forward_left = -1
        forward_right = -1
        right = -1
        left = -1
        back = -1
        back_left = -1
        back_right = -1

        for car in scene_info['cars_info']:
            if car['id'] == self.player_no:
                carX = car['pos'][0]
                carY = car['pos'][1]
                forward = carY
                back = 800 - carY
                left = carX - 20
                right = 610 - carX
                forward_left = forward
                forward_right = forward
                back_left = back
                back_right = back
        
        for car in scene_info['cars_info']:
            if car['id'] != self.player_no:
                if car['pos'][0] - carX <= 50 and car['pos'][0] - carX >= -50:
                    if car['pos'][1] > carY:
                        if back > car['pos'][1] - carY - 80:
                            back = car['pos'][1] - carY - 80
                    else:
                        if forward > carY - car['pos'][1] - 80:
                            forward = carY - car['pos'][1] - 80
                if car['pos'][0] - carX >= 50 and car['pos'][0] - carX <= 130:
                    if car['pos'][1] > carY:
                        if back_right > car['pos'][1] - carY - 80:
                            back_right = car['pos'][1] - carY - 80
                            if back_right < 0:
                                back_right = 0
                    else:
                        if forward_right > carY - car['pos'][1] - 80:
                            forward_right = carY - car['pos'][1] - 80
                            if forward_right < 0:
                                forward_right = 0
                if  car['pos'][0] - carX <= -50 and car['pos'][0] - carX >= -130:
                    if car['pos'][1] > carY:
                        if back_left > car['pos'][1] - carY - 80:
                            back_left = car['pos'][1] - carY - 80
                            if back_left < 0:
                                back_left = 0
                    else:
                        if forward_left > carY - car['pos'][1] - 80:
                            forward_left = carY - car['pos'][1] - 80
                            if forward_left < 0:
                                forward_left = 0
                if car['pos'][1] - carY <= 80 and car['pos'][1] - carY >= -80:
                    if car['pos'][0] > carX:
                        if right > car['pos'][0] - carX - 40:
                            right = car['pos'][0] - carX - 40
                    else:
                        if left > carX - car['pos'][0] - 40:
                            left = carX - car['pos'][0] - 40

        feature = [[forward_left, forward, forward_right, left, right, back_left, back, back_right, carX, carY]]

        pred = self.tree.predict(feature)

        #print("***")
        #print(self.player_no)
        #print(pred)

        if pred == 8:
            return []
        if pred == 1:
            return ['BREAK']
        if pred == 2:
            return ['MOVE_LEFT']
        if pred == 3:
            return ['MOVE_RIGHT']
        if pred == 4:
            return ['SPEED', 'MOVE_LEFT']
        if pred == 5:
            return ['SPEED', 'MOVE_RIGHT']
        if pred == 6:
            return ['BREAK', 'MOVE_LEFT']
        if pred == 7:
            return ['BREAK', 'MOVE_RIGHT']
        else:
            return ['SPEED']

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
