from streamlit_webrtc import webrtc_streamer

import threading

import cv2
import streamlit as st
from matplotlib import pyplot as plt

st.set_page_config(page_title="Streamlit WebRTC Example", page_icon=":guardsman:", layout="wide")
lock = threading.Lock()
img_container = {"img": None}


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img

    return frame

col1, col2 = st.columns(2)

with col1:
    ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback, 
                      media_stream_constraints={"video": True, "audio": False},
                      rtc_configuration={"iceServers": [{"urls": ["stun:stun.relay.metered.ca:80"]},
                                                        {"urls":["turn:asia.relay.metered.ca:80"],
                                                        "username": "1d26b67f6210bea330a0b203",
                                                        "credential": "TgLT2SkILgzDDrOu"},
                                                        {"urls":["turn:asia.relay.metered.ca:80?transport=tcp"],
                                                        "username": "1d26b67f6210bea330a0b203",
                                                        "credential": "TgLT2SkILgzDDrOu",},
                                                        {"urls":["turn:asia.relay.metered.ca:443"],
                                                        "username": "1d26b67f6210bea330a0b203",
                                                        "credential": "TgLT2SkILgzDDrOu",},
                                                        {"urls":["turns:asia.relay.metered.ca:443?transport=tcp"],
                                                        "username": "1d26b67f6210bea330a0b203",
                                                        "credential": "TgLT2SkILgzDDrOu",}]})
imgout_place = col2.empty()

fig_place = st.empty()
fig, ax = plt.subplots(1, 1)

while ctx.state.playing:
    with lock:
        imgin = img_container["img"]
    if imgin is None:
        continue
    imgout = cv2.flip(imgin, 1)
    imgout_place.image(imgout, channels="BGR")
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ax.cla()
    # ax.hist(gray.ravel(), 256, [0, 256])
    # fig_place.pyplot(fig)
