import streamlit as st
from google import genai
from gtts import gTTS
import os

st.set_page_config(page_title="My Movie Recap App", page_icon="🎬")

st.title("🎬 ကိုယ်ပိုင် Movie Recap Generator (Multiple Voices)")
st.write("ရုပ်ရှင်ဇာတ်လမ်းအတွက် Script များနှင့် အသံပုံစံအမျိုးမျိုးကို စိတ်ကြိုက်ရွေးချယ်ပါ")

# Sidebar မှာ Settings တွေ ထည့်ရန်
st.sidebar.header("Settings")
api_key_input = st.sidebar.text_input("Gemini API Key ထည့်ပါ", type="password")

voice_style = st.sidebar.selectbox(
    "🎙️ AI Script ပုံစံ ရွေးပါ",
    [
        "🎭 ဇာတ်လမ်းပြောဆရာ (Dramatic Narrator)",
        "🔥 အက်ရှင်ဆန်ဆန် (Action & Hype)",
        "😂 ဟာသနှောပြီး (Funny & Casual)"
    ]
)

# -------------------------------------------------------------
# အသံအမျိုးအစား (Voice Models) ရွေးချယ်ရန် အပိုင်း
# -------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🔊 အသံထွက် (Voice) ပုံစံများ")
selected_voice_type = st.sidebar.selectbox(
    "အသံအမျိုးအစား ရွေးပါ",
    [
        "🇲🇲 မြန်မာ အသံစံ (Standard Myanmar)",
        "🇬🇧 နိုင်ငံတကာ လေသံ (English - UK Accent)",
        "🇺🇸 အမေရိကန် လေသံ (English - US Accent)"
    ]
)

# Main Section
movie_title = st.text_input("ရုပ်ရှင်နာမည် (သို့) ဇာတ်လမ်းအကြောင်း အတိုချုပ် ရေးပါ")
uploaded_file = st.file_uploader("သို့မဟုတ် ရုပ်ရှင်ဗီဒီယိုဖိုင်ကို တင်ပါ (MP4)", type=["mp4", "mov", "avi"])

st.markdown("---")
st.subheader("🔊 Voice အသံအစမ်း နားဆင်ရန်")
sample_text = st.text_input("အသံထွက်စမ်းရန် စာသား ရိုက်ပါ", "မင်္ဂလာပါဗျ၊ ဒီနေ့ တင်ဆက်ပေးမှာကတော့ စိတ်လှုပ်ရှားစရာ ဇာတ်လမ်းကောင်းပဲ ဖြစ်ပါတယ်။")

if st.button("🎧 အသံနမူနာ ထုတ်မည်"):
    try:
        # ရွေးချယ်ထားသော Voice ပုံစံအလိုက် gTTS သတ်မှတ်ခြင်း
        if "Myanmar" in selected_voice_type:
            tts = gTTS(text=sample_text, lang='my', slow=False)
        elif "UK" in selected_voice_type:
            tts = gTTS(text=sample_text, lang='en', tld='co.uk', slow=False)
        else:
            tts = gTTS(text=sample_text, lang='en', tld='com', slow=False)
            
        tts.save("sample_voice.mp3")
        
        st.audio("sample_voice.mp3", format="audio/mp3")
        st.success("✨ ရွေးချယ်ထားသော အသံပုံစံဖြင့် အသံနမူနာ ထွက်လာပါပြီ!")
    except Exception as e:
        st.error(f"အသံထုတ်ယူရာတွင် အမှားရှိနေပါသည်: {e}")

st.markdown("---")

# -------------------------------------------------------------
# Movie Recap Script ထုတ်မည့် အပိုင်း
# -------------------------------------------------------------
if st.button("🚀 Recap Script စတင်ထုတ်မည်"):
    if not api_key_input:
        st.error("ကျေးဇူးပြု၍ ဘယ်ဘက်ခြမ်းတွင် Gemini API Key ထည့်ပေးပါခင်ဗျာ။")
    elif not movie_title and not uploaded_file:
        st.warning("ကျေးဇူးပြု၍ ရုပ်ရှင်နာမည် ရေးပါ (သို့) ဗီဒီယိုဖိုင် တင်ပေးပါ။")
    else:
        try:
            client = genai.Client(api_key=api_key_input)
            
            with st.spinner(f"Gemini AI က '{voice_style}' ပုံစံနဲ့ Script ရေးနေပါပြီ... ခဏစောင့်ပါ ⏳"):
                prompt = f"ဒီရုပ်ရှင်အတွက် '{voice_style}' ဆိုတဲ့ ပြောဟန်ပုံစံနဲ့ TikTok/YouTube Shorts တင်လို့ကောင်းမယ့် Movie Recap Script တစ်ခု ရေးပေးပါ။ Hook section နဲ့ ဇာတ်လမ်းအကျဉ်း ပါဝင်ပါစေ။"
                
                if uploaded_file is not None:
                    with open("temp_video.mp4", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    video_file = client.files.upload(file="temp_video.mp4")
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[video_file, prompt]
                    )
                    os.remove("temp_video.mp4")
                else:
                    full_prompt = f"ရုပ်ရှင်နာမည်: {movie_title}\n{prompt}"
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[full_prompt]
                    )
                
                st.success("✨ Recap Script ထွက်လာပါပြီ!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"မှားယွင်းမှု ရှိနေပါသည်: {e}")
            
