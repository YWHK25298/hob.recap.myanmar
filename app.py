import streamlit as st
from google import genai
import os

st.set_page_config(page_title="My Movie Recap App", page_icon="🎬")

st.title("🎬 ကိုယ်ပိုင် Movie Recap Generator")
st.write("Gemini AI ကို အသုံးပြု၍ ရုပ်ရှင် ဗီဒီယို (သို့) ဇာတ်လမ်းနာမည်မှ Recap Script ထုတ်ယူပါ")

# Sidebar မှာ API Key ထည့်ရန်
st.sidebar.header("Settings")
api_key_input = st.sidebar.text_input("Gemini API Key ထည့်ပါ", type="password")

# Main Section - ရုပ်ရှင်နာမည် (သို့) ဗီဒီယိုဖိုင် တင်ရန်
movie_title = st.text_input("ရုပ်ရှင်နာမည် (သို့) ဇာတ်လမ်းအကြောင်း အတိုချုပ် ရေးပါ")
uploaded_file = st.file_uploader("သို့မဟုတ် ရုပ်ရှင်ဗီဒီယိုဖိုင်ကို တင်ပါ (MP4)", type=["mp4", "mov", "avi"])

recap_style = st.selectbox(
    "Recap ပြောမယ့် ပုံစံရွေးပါ",
    ["ဟာသနှောပြီး စိတ်ဝင်စားစရာ", "အက်ရှင်ဆန်ဆန် စိတ်လှုပ်ရှားဖွယ်", "တိုတိုနဲ့ လိုရင်းရောက် (Shorts ပုံစံ)"]
)

if st.button("🚀 Recap Script စတင်ထုတ်မည်"):
    if not api_key_input:
        st.error("ကျေးဇူးပြု၍ ဘယ်ဘက်ခြမ်းတွင် Gemini API Key ထည့်ပေးပါခင်ဗျာ။")
    elif not movie_title and not uploaded_file:
        st.warning("ကျေးဇူးပြု၍ ရုပ်ရှင်နာမည် ရေးပါ (သို့) ဗီဒီယိုဖိုင် တင်ပေးပါ။")
    else:
        try:
            client = genai.Client(api_key=api_key_input)
            
            with st.spinner("Gemini AI က ဇာတ်လမ်းကို စဉ်းစားနေပါပြီ... ခဏစောင့်ပါ ⏳"):
                prompt = f"ဒီရုပ်ရှင်အတွက် '{recap_style}' ပုံစံနဲ့ TikTok/YouTube Shorts တင်လို့ကောင်းမယ့် Movie Recap Script တစ်ခု ရေးပေးပါ။ Hook section နဲ့ ဇာတ်လမ်းအကျဉ်း ပါဝင်ပါစေ။"
                
                if uploaded_file is not None:
                    # ဗီဒီယိုဖိုင် တင်ထားလျှင် Temporary သိမ်းဆည်းပြီး Gemini သို့ ပို့မည်
                    with open("temp_video.mp4", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    video_file = client.files.upload(file="temp_video.mp4")
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[video_file, prompt]
                    )
                    # ပြီးလျှင် ဖိုင်ဖျက်မည်
                    os.remove("temp_video.mp4")
                else:
                    # နာမည်ပဲ ပေးထားလျှင်
                    full_prompt = f"ရုပ်ရှင်နာမည်: {movie_title}\n{prompt}"
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[full_prompt]
                    )
                
                st.success("✨ Recap Script ထွက်လာပါပြီ!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"မှားယွင်းမှု ရှိနေပါသည်: {e}")
