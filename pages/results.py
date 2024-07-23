import streamlit as st
from base64 import b64encode as encode

def img_cvt_bs64(image):
        with open(image, 'rb') as image:
            data = image.read()
        return encode(data).decode()

image = img_cvt_bs64("images/bg/result_bg.jpg")

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



empty_container = st.empty()
image_, text_ = empty_container.columns([1, 2])
image_.image("images/ai/bujji.png", width= 250)


if "winner" in st.session_state:
    if st.session_state.winner == "user":
        with text_:
            st.title("Congratulations Buddy !")
            st.subheader("You Won the Game")
            st.balloons()
    elif st.session_state.winner == "bujji":
        with text_:
            st.title("Nice Try Buddy !")
            st.subheader("This time I won !")
            st.snow()
    
    empty_container2 = st.empty()
    button1, button2 = empty_container2.columns(2)
    button1.button("Play Again ?", use_container_width= True, key= "play_again_key")
    button2.button("Exit Game", use_container_width= True, key= "terminate_key")

    if "play_again_key" in st.session_state and st.session_state["play_again_key"]:
        st.session_state.user_points = 5
        st.session_state.bujji_points = 5
        st.switch_page("pages/game.py")
    
    elif "terminate_key" in st.session_state and st.session_state["terminate_key"]:
        st.session_state["game_ended"] = True
        st.switch_page("web.py")

else:
    text_.subheader("ERROR: 404")
    text_.write("Something went wrong !")

with open("CSS files/style2.css") as styler_2:
    st.markdown(f"<style>{styler_2.read()}</styler>", unsafe_allow_html= True)