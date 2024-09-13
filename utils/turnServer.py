from streamlit_webrtc import RTCConfiguration

def get_server():
    
    try:
        RTC_CONFIGURATION = RTCConfiguration(
                            {
                            "RTCIceServer": [{
                                "urls": ["turn:turn.anyfirewall.com:443?transport=tcp"],
                                "username": "webrtc",
                                "credential": "webrtc",
                                }]
                            }
                        )
        
        return RTC_CONFIGURATION
    
    except:
        RTC_CONFIGURATION: dict[str, list[dict[str, list[str]]]] = {
                    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                }
        
        return RTC_CONFIGURATION
