from time import sleep
import streamlit as st
from av import VideoFrame
from random import choice
from cv2 import flip, rectangle, putText, FONT_HERSHEY_COMPLEX, FILLED
from cvzone.HandTrackingModule import HandDetector
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from base64 import b64encode as encode


st.set_page_config(page_title= "Rock Paper Scissor",
                    page_icon= ":smiley:")

def img_cvt_bs64(image):
        with open(image, 'rb') as image:
            data = image.read()
        return encode(data).decode()

image = img_cvt_bs64("images/bg/game_bg.jpg")

set_bgCmd = f"""
        <style>
        #root > div:nth-child(1) > div.withScreencast > div > div
        {{
            background-color: #0C0908;
            background-image: url('data:image/png;base64,{image}');
            background-position: center;
            background-size: cover;            
        }}
        </style>
        """
st.markdown(set_bgCmd, unsafe_allow_html= True)

detector = HandDetector(detectionCon=0.8, maxHands=1)

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.start_detection = False
        self.detected = False
        self.guesture = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = flip(img, 1)
        hands = []

        if self.start_detection:
            hands, img = detector.findHands(img, flipType=False, draw= False)

        if len(hands) != 0:
            self.detected = True 
            fingures = detector.fingersUp(hands[0])

            if fingures == [1, 0, 0, 0, 0]: self.guesture = "Rock"
            elif fingures == [1, 1, 1, 0, 0]: self.guesture = "Scissors"
            elif fingures == [0, 1, 1, 1, 1]: self.guesture = "Paper"

            bbox = hands[0]["bbox"]
            rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                (255, 0, 255), 2)
            putText(img, self.guesture, (bbox[0] - 30, bbox[1] - 30), FONT_HERSHEY_COMPLEX,
                        1, (255, 255, 255), 2)
        else:
            self.detected = False
            if self.start_detection:
                height, width = img.shape[:2]
                rectangle(img, (0, (height//2) - 30), (width, (height//2) + 15), (0, 0, 0, 128), FILLED)
                putText(img, "Hand Not Visible !", ((width//2) - 150, (height//2)), FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 1)

        return VideoFrame.from_ndarray(img, format="bgr24")

if "user_points" not in st.session_state:
    st.session_state.user_points = 5
    st.session_state.bujji_points = 5
st.session_state.button_disabled = True
st.session_state.winner = "None"
st.session_state["force_exit"] = False
st.session_state["game_ended"] = False


button_container = st.container()
empty_1 = st.empty()
container = st.container(height= 300, border= True)
empty_2 = st.empty()
empty_3 = st.empty()


button_container.button(label= "Exit", key= "exit_game")

user_pointsCol, bujji_pointsCol = empty_1.columns(2)
user_pointsCol.write(f"Points: {st.session_state.user_points}")
bujji_pointsCol.write(f"Points: {st.session_state.bujji_points}")

user_window, bujji_window = container.columns(2)

text_empty = user_window.empty()
text_empty.write("Please Start WebCam !")

with user_window:
    ctx = webrtc_streamer(
                key="webcam",
                video_processor_factory= VideoTransformer,
                sendback_audio= False,
                rtc_configuration={
                    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                }
            )

if ctx.video_transformer:
    text_empty.empty()
    st.session_state.button_disabled = False
    ctx.video_transformer.start_detection = False

bujji_subWindow = bujji_window.empty()
bujji_subWindow.image("images/ai/bujji.png", width= 250)

empty_2.button("Start", key= "start_key", disabled= st.session_state.button_disabled)

user_col, bujji_col = empty_3.columns(2)
user_col.write("YOU")
bujji_col.write("BUJJI")



def getBujji_move():

    choices = ["rock", "paper", "scissors", "paper", "scissors", "rock", "rock", "scissors", "paper"] # This is done to prevent same successive choices
    bujji_choice = choice(choices)
    bujji_subWindow.image(f"images/ai/{bujji_choice}.jpg")

    return bujji_choice

def result(user, bujji):
    compare_criteria = {"paper": "rock",
                        "rock": "scissors",
                        "scissors": "paper"}
    if user is None:
        winner = "foul"
    elif user == bujji:
        winner = "tie"
    elif compare_criteria[user] == bujji:
        winner = "user"
    elif compare_criteria[bujji] == user:
        winner = "bujji"

    return winner

def set_results(round_winner):
    if round_winner == "foul":
        empty_2.write("Foul")
        st.session_state.user_points -= 1

    elif round_winner == "tie":
        empty_2.write("Tie !")
        pass

    elif round_winner == "user":
        empty_2.write("You Won !")
        st.session_state.bujji_points -= 1
    
    elif round_winner == "bujji":
        empty_2.write("Bujji Won !")
        st.session_state.user_points -= 1

def start_game():
    user_move = None
    game_winner = None
    

    while True:
        empty_2.write("Ready !")
        sleep(3)

        timer = 3
        while timer > 0:            

            try:
                detected = ctx.video_transformer.detected
            except:
                detected = False

            if not detected:
                timer = 3
                empty_2.write("Ready !")
            else:
                empty_2.write(f"{timer}")
                timer -= 1

            sleep(1)

        empty_2.write("Go !")
        sleep(1)

        try:
            detected = ctx.video_transformer.detected
        except:
            detected = False
        if not detected: user_move = None
        else:
            try:
                user_move = (ctx.video_transformer.guesture).lower()
            except:
                user_move = None
        
        bujji_move = getBujji_move()
        round_winner = result(user_move, bujji_move)
        set_results(round_winner)

        empty_1.empty()
        user_pointsCol, bujji_pointsCol = empty_1.columns(2)
        user_pointsCol.write(f"Points: {st.session_state.user_points}")
        bujji_pointsCol.write(f"Points: {st.session_state.bujji_points}")

        sleep(3)
        bujji_subWindow.image("images/ai/bujji.png", width= 250)

        if st.session_state.user_points == 0:
            game_winner = "bujji"
            return game_winner
        
        elif st.session_state.bujji_points == 0:
            game_winner = "user"
            return game_winner

        

if "start_key" in st.session_state and st.session_state["start_key"]:
    ctx.video_transformer.start_detection = True
    game_winner = start_game()
    #print(game_winner)
    st.session_state.winner = game_winner
    st.switch_page("pages/results.py")

if st.session_state["exit_game"]:
    try:
        ctx.video_transformer.start_detection = False
    except:
        pass
    st.session_state["force_exit"] = True
    st.switch_page("web.py")


with open("CSS files/style1.css") as game_styler:
    st.markdown(f"<style>{game_styler.read()}</styler>", unsafe_allow_html= True)
