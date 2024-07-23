import required_modules as mod


mod.st.set_page_config(page_title= "My Portfolio",
                       layout= "wide",
                       page_icon= ":smiley:")


def custom_background():
    def img_cvt_bs64(image):
        with open(image, 'rb') as image:
            data = image.read()
        return mod.encode(data).decode()

    image = img_cvt_bs64("images/bg/web_bg.jpg")

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
    mod.st.markdown(set_bgCmd, unsafe_allow_html= True)

def apply_styler():
    with open("CSS files/style.css") as styler:
        mod.st.markdown(f"<style> {styler.read()} </style>", unsafe_allow_html= True)

def web_header():
    js_script = f"""
                <body>
                    <header>
                        <a href= '#bf31a0d2' >Pulasari Jai</a>
                        <nav>
                            <a href= '#i-m-jai-s-ai-bot' >AI</a>
                            <a href= '#my-youtube-channel' >YouTube</a>
                            <a href= '#developed-projects' >Projects</a>
                            <a href= '#socials' >Socials</a>
                            <a href= '#contact' >Contacts</a>
                        </nav>
                    </header>
                </body>
                <script>

                </script>
            """
    mod.st.html(js_script)

def profile_section():

    profile = mod.st.container()

    col1, col2 = profile.columns([2, 1])
    col1.subheader("🙏 Namaste 🙏")
    col1.write(" ")
    col1.caption("WHO's THIS ?")

    with open("text/myIntro.txt", encoding='utf8') as introduction:
        intro = introduction.read()
        col1.write(intro)
    
    my_pic = mod.load_img("images/profile_pic.jpg").resize((450,500))
    col2.image(my_pic)
    col2.write("Invictus Jai")
    profile.title(" ")

def aiBot_section():

    ai_bot = mod.st.container()
    ai_bot.subheader("I'm Jai's AI BOT !")

    def sub_section1():
        api_key = mod.st.secrets["GOOGLE_API_KEY"]
        mod.genai.configure(api_key= api_key)
        model = mod.genai.GenerativeModel('gemini-1.5-flash')

        

        with open("Animaion/Bot Animation.json", encoding='utf8') as file:
            animation = mod.load(file)
        with ai_bot:
            mod.st_lottie(animation)
        ai_bot.write(" ")

        user_ques = ai_bot.text_input(label= "Wanna know something about him, I'll answer on his behaf", placeholder= "Ask anything...")
        ai_bot.button("ASK", key= "ask_bot")
        response_container = ai_bot.empty()

        with open("text/persona.txt") as persona:
            prompt = f"{persona.read()} , Here is the question that the user asked -> {user_ques}"

        if mod.st.session_state["ask_bot"]:
            try:
                response = model.generate_content(prompt)
                response_container.write(response.text)
            except:
                response_container.write("I can't answer this question !")
    
    def sub_section2():

        empty_1 = ai_bot.empty()
        empty_2 = ai_bot.empty()
        empty_3 = ai_bot.empty()

        with empty_1:
            mod.st.image("images/ai/bujji.png", caption= "BUJJI", width= 160)
        with empty_2:
            text_container = mod.st.container()
            text_container.subheader("Hello I am Bujji")
            text_container.subheader("Wanna play a game ?")
        with empty_3:
            col1, col2 = mod.st.columns(2)
            col1.button("Yes", use_container_width= True, key= "response_yes")
            col2.button("No", use_container_width= True, key= "response_no")

        if "response_yes" in mod.st.session_state and mod.st.session_state["response_yes"]:
            empty_2.empty()
            empty_3.empty()

            empty_2.subheader("Excellent! Want to know the rules?")

            col1, col2 = empty_3.columns(2)
            col1.button("Tell Me", use_container_width= True, key= "listen_instructions")
            col2.button("I know the rules", use_container_width= True, key= "skip_instructions")
        
        elif "response_no" in mod.st.session_state and mod.st.session_state["response_no"]:    
            empty_2.empty()
            empty_3.empty()

            empty_2.subheader("No problem, will play next time !")

        if "listen_instructions" in mod.st.session_state and mod.st.session_state["listen_instructions"]:
            empty_2.empty()
            empty_3.empty()

            instruct_box = empty_2.container()
            instruct_box.write("- This is a Computer Vision game and requires WebCam to be enabled.")
            instruct_box.write("- Make sure you are in a well lit environment and your hand is clearly visible in the camera.")
            instruct_box.write("- To start, you must start the WebCam by Start button below the webcam window.")
            instruct_box.write("- Face your palm towards camera while showing your guesture.")
            instruct_box.write("- On the count of one, You have to show the guesture with your hand.")
            instruct_box.write("- The game will not continue unless your hand is visible in the WebCam.")
            instruct_box.write("- If your hand is not visible in the camera when count ends, your points will be cut for the foul.")
            instruct_box.write("- The one who loses 5 points first, will lose the game.")
            instruct_box.write(" ")
            instruct_box.write("Best of Luck !")

            empty_3.button("Next", use_container_width= True, key= "next_button")
        
        elif ("skip_instructions" in mod.st.session_state and mod.st.session_state["skip_instructions"]) or ("next_button" in mod.st.session_state and mod.st.session_state["next_button"]):
            empty_2.empty()
            empty_3.empty()

            mod.st.switch_page("pages/game.py")

    def sub_section3(mode):
        container_ = ai_bot.empty()
        if mode == "completed":
            content_holder = container_.container()
            bujji_cont, text_cont = content_holder.columns([1, 2])
            bujji_cont.image("images/ai/bujji.png", caption= "BUJJI", width= 250)
            text_cont.subheader("That was a great game! Let’s play again sometime.")
        else:
            content_holder = container_.container()
            bujji_cont, text_cont = content_holder.columns(2)
            #bujji_cont = content_holder.empty()
            bujji_cont.image("images/ai/bujji.png", caption= "BUJJI", width= 250)
            
            text_empty = text_cont.empty()
            text_empty.subheader("Wanna Continue the Game Again ?")

            button_empty = content_holder.empty()
            button_column1, button_column2 = button_empty.columns(2)
            button_column1.button("Continue Game", use_container_width= True, key= "continue")
            button_column2.button("No Thanks !", use_container_width= True, key= "end")

            if mod.st.session_state["continue"]:
                container_.empty()
                mod.st.switch_page("pages/game.py")

            elif mod.st.session_state["end"]:
                text_empty.empty()
                button_empty.empty()

                text_empty.subheader("Ok ! Let’s have a rematch soon.")
    sub_section1()
    ai_bot.title(" ")

    if "game_ended" in mod.st.session_state and mod.st.session_state["game_ended"]:
        sub_section3("completed")
    elif "force_exit" in mod.st.session_state and mod.st.session_state["force_exit"]:
        sub_section3("exit")
    else:
        sub_section2()
    ai_bot.title(" ")

def youtube_section():

    youtube = mod.st.container()
    youtube.subheader("My Youtube Channel", divider= "orange")
    col1, col2 = youtube.columns(2)

    col1.title(" ")
    col1.write("- Tech Enthusiast 🔥")
    col1.write("- Amazing Projects 💻")
    col1.write("- Living the software dream. 🌐")
    col1.write("- Creating magic with every line of code. ✨")
    col1.write("- Keep coding and stay peculiar. 🚀")

    col2.video("https://youtu.be/CWFUKrfj4ec?feature=shared")
    col2.link_button("Visit",
                     url= "https://youtu.be/CWFUKrfj4ec?feature=shared",
                     use_container_width= True)
    youtube.title(" ")

def setup_section():

    setup = mod.st.container()
    setup.subheader("My Setup", divider= "orange")

    setup_bg = mod.load_img("images/my_setup.jpg").resize((980, 750))
    setup.image(setup_bg)
    setup.title(" ")

def skills_section():

    skills = mod.st.container()
    skills.subheader("My Skills", divider= "orange")

    skills.slider("Programming", 0, 100, 75)
    skills.slider("Problem Solving", 0, 100, 80)
    skills.slider("Learnability", 0, 100, 90)
    skills.slider("Multi Tasking", 0, 100, 85)

    skills.title(" ")

def projects_section():

    def img_cvt_bs64(image):
        with open(image, 'rb') as image:
            data = image.read()
        return mod.encode(data).decode()

    projects = mod.st.container()
    projects.subheader(" ", divider= 'blue')

    # col1, col2 = projects.columns(2)
    projects.subheader("Developed Projects")
    
    #ol2.write("Yet to upload !")

    img1 = img_cvt_bs64("images/projects/projects_1.jpg")
    img2 = img_cvt_bs64("images/projects/projects_2.jpg")
    img3 = img_cvt_bs64("images/projects/projects_3.jpg")
    img4 = img_cvt_bs64("images/projects/projects_4.jpg")
    img5 = img_cvt_bs64("images/projects/projects_5.jpg")

    with projects:
        with open("CSS files/slider.html") as slider:
            mod.st.html(slider.read().format(img1, img2, img3, img4, img5))
    
    projects.link_button("Github",
                         url= "https://github.com/IamInvictus-Jai")
    

    projects.subheader(" ", divider= 'blue')
    projects.title(" ")

def socialsMedia_section():

    socials = mod.st.container()
    socials.subheader("SOCIALS", divider= 'rainbow')
    socials.subheader(" ")

    with socials:
        social_media_links = [
            "https://youtube.com/@iaminvictus_jai?feature=shared",
            "https://www.instagram.com/i.am_unknown_8?igsh=eWd6NG42dnV0aGtw",
            "https://github.com/IamInvictus-Jai"
        ]
        social_media_icons = mod.SocialMediaIcons(social_media_links)
        social_media_icons.render()
    
    socials.title(" ")

def other_skills():

    other_skills = mod.st.container()
    other_skills.subheader("Love Rhythm and Arts ?", divider= "rainbow")
    expanded_box = other_skills.expander("🌟 Discover mesmerizing dance moves and breathtaking artistry on my vibrant social platforms. 🎨")
    expanded_box.subheader("Some of my Works")

    videos = expanded_box.container()

    counter = 1
    for row_img in range(3):
        for col in videos.columns(3):
            col.image(f"images/Skills/skills_{counter}.jpg")
            counter += 1

    col10, col11 = other_skills.columns(2)    
    col10.link_button("YouTube Channel",
                    url= "https://www.youtube.com/@invictusjai7162",
                    use_container_width= True)
    col11.link_button("Insta",
                    url= "https://www.instagram.com/invictus_jai/",
                    use_container_width= True)
    
    for row in range(1, 4):
        for img_count in range(1, 4):
            mod.st.markdown(f"""
                            <style>
                            #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(11) > div > div > div.st-emotion-cache-0.eqpbllx4 > details > div > div > div > div > div.st-emotion-cache-0.e1f1d6gn0 > div > div > div:nth-child({row}) > div:nth-child({img_count}) > div > div > div > div > div > div > div > img
                            {{
                                transition: transform 0.8s;    
                            }}
                            #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(11) > div > div > div.st-emotion-cache-0.eqpbllx4 > details > div > div > div > div > div.st-emotion-cache-0.e1f1d6gn0 > div > div > div:nth-child({row}) > div:nth-child({img_count}) > div > div > div > div > div > div > div > img:hover
                            {{
                                transform: scale(1.05);
                            }}
                            </style>
                            """, unsafe_allow_html= True)

    other_skills.subheader(" ")

def contacts_section():

    contacts = mod.st.container()
    contacts.title("CONTACT")
    contacts.subheader("For any querries, you can cantact me through:")
    contacts.write("prof.techinvictus@gmail.com")
    contacts.subheader(" ")

def web_footer():

    footer = mod.st.container()
    footer.subheader(" ", divider= 'grey')
    cur_year = mod.datetime.now().year
    footer.write(f"Copyright © {cur_year} Pulasari Jai")


if __name__ == "__main__":
    custom_background()
    apply_styler()
    web_header()
    profile_section()
    aiBot_section()
    youtube_section()
    setup_section()
    skills_section()
    projects_section()
    socialsMedia_section()
    other_skills()
    contacts_section()
    web_footer()