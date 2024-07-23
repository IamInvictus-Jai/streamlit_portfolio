from json import load
import streamlit as st
from datetime import datetime
import google.generativeai as genai
from streamlit_lottie import st_lottie
from base64 import b64encode as encode
from PIL.Image import open as load_img
from st_social_media_links import SocialMediaIcons