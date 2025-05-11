import cv2
import cv2.text
import mediapipe as mp 
import math
import time
import random
from ursina import *
import threading

mpHands = mp.solutions.hands
hand_distance = 0
smoothed_distance = 0


hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)


def dist_bet(points_list, a, b):
    dist = math.dist(points_list[a], points_list[b])
    return dist



def scale_switch(ss:bool, ts:bool, dist, dist_thresh, ct, lt, cdt):
    if dist < dist_thresh:
        if not ts and (ct - lt) >= cdt:
            ss = not ss
            lt = ct
            ts = True
    else:
        ts = False
    return ss, ts, lt




def draw_hands(draw, frameRGB, frames):
    processed = hands.process(frameRGB)
    landmarks_list = []

    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        draw.draw_landmarks(frames, hand_landmarks, mpHands.HAND_CONNECTIONS)

        for lm in hand_landmarks.landmark:
            landmarks_list.append((lm.x, lm.y))

    return landmarks_list



def main():
    global hand_distance

    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils

    
    touch_state = False
    switch_state = False
    last_active_time = 0
    cooldowntime = 1
    distance_thresshold = 10

    try:
        while cap.isOpened():
            success, frames = cap.read()

            if not success:
                break

            frames = cv2.flip(frames, 1)
            frameRGB = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
            current_time = time.time()
            
            lm_list = draw_hands(draw, frameRGB, frames)
            
            if lm_list:
                distance = int(dist_bet(lm_list, 8,4) * 100)
                print(distance)
                switch_state, touch_state , last_active_time= scale_switch(
                switch_state, touch_state, distance, distance_thresshold, current_time, last_active_time, cooldowntime
                )
                
                print(switch_state, touch_state)
                if switch_state == True:
                    text = str(distance)
                    h,w, _ = frames.shape
                    cx1, cy1 = int(lm_list[4][0] * w), int(lm_list[4][1] * h)  # 
                    cx2, cy2 = int(lm_list[8][0] * w), int(lm_list[8][1] * h)
                    cv2.circle(frames, (cx1,cy1), 20, (255,80,221), 3)
                    cv2.circle(frames, (cx2,cy2), 20, (0,0,221), 3)
                    cv2.line(frames, (cx1,cy1),(cx2,cy2), (0,0,221), 2)
                    hand_distance = distance
            

            cv2.imshow('Frames', frames)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

# main()

app = Ursina()
window.color = color.black
rotator = Entity()

particles = []
num_particles = 1000
sphere_radius = 2


for i in range (num_particles):

    angle1 = random.uniform(0,math.pi*2) # 2πr = Θ (theta)
    angle2 = random.uniform(0,math.pi) # πr


    x = sphere_radius * math.sin(angle2) * math.cos(angle1)
    y = sphere_radius * math.sin(angle2) * math.sin(angle1)
    z = sphere_radius * math.cos(angle2)

    p = Entity(
        model = 'sphere',
        color = color.azure,
        scale = 0.02,
        position = (x,y,z),
        parent = rotator
        )
    
    # p.emission_color = color.azure
    p.angle1 = angle1
    p.angle2 = angle2
    p.speed = random.uniform(0.2,1.0)
    particles.append(p)


def update():

    global hand_distance,smoothed_distance

    alpha = 0.1
    smoothed_distance = (1-alpha) * smoothed_distance + alpha * hand_distance

    radius = max(smoothed_distance/5, 1)

    rotator.rotation_y += time.dt *20

    for p in particles:
        p.angle1 += time.dt * p.speed
        p.angle2 += time.dt * p.speed
        
        x = radius * math.sin(p.angle2) * math.cos(p.angle1)
        y = radius * math.sin(p.angle2) * math.sin(p.angle1)
        z = radius * math.cos(p.angle2)

        p.position = (x,y,z)


EditorCamera()

threading.Thread(target=main, daemon=True).start()
app.run()
