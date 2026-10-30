import streamlit as st
from google import genai

st.set_page_config(page_title="My Movie Recap App", page_icon="🎬")

st.title("🎬 ကိုယ်ပိုင် Movie Recap Generator")
st.write("Gemini AI ကို အသုံးပြု၍ ရုပ်ရှင်အကျဉ်းချုပ် ဇာတ်လမ်းများကို အလွယ်တကူ ထုတ်ယူနိုင်ပါပြီ။")

# Sidebar မှာ API Key ထည့်ရန်
st.sidebar.header("Settings")
api_key_input = st.sidebar.text_input("AQ.Ab8RN6KKOLIO4TH5a7WZuvc47RNN3KRMHOJqMRp0yxXgMo-W8Q", type="password")

# Main Section
movie_title = st.text_input("ရုပ်ရှင်နာမည် (သို့) ဇာတ်လမ်းအကြောင်း အတိုချုပ် ရေးပါ")
recap_style = st.selectbox(
    "Recap ပြောမယ့် ပုံစံရွေးပါ",
    ["ဟာသနှောပြီး စိတ်ဝင်စားစရာ", "အက်ရှင်ဆန်ဆန် စိတ်လှုပ်ရှားဖွယ်", "တိုတိုနဲ့ လိုရင်းရောက် (Shorts ပုံစံ)"]
)

if st.button("🚀 Recap Script စတင်ထုတ်မည်"):
    if not api_key_input:
        st.error("ကျေးဇူးပြု၍ ဘယ်ဘက်ခြမ်းတွင် Gemini API Key ထည့်ပေးပါခင်ဗျာ။")
    elif not movie_title:
        st.warning("ကျေးဇူးပြု၍ ရုပ်ရှင်နာမည် သို့မဟုတ် ဇာတ်လမ်းအကြောင်း ထည့်ပါ။")
    else:
        try:
            # Gemini Client ချိတ်ဆက်ခြင်း
            client = genai.Client(api_key=api_key_input)
            
            with st.spinner("Gemini AI က စိတ်ဝင်စားစရာ Recap Script ရေးနေပါပြီ... ခဏစောင့်ပါ ⏳"):
                prompt = f"ဒီရုပ်ရှင် '{movie_title}' အတွက် '{recap_style}' ပုံစံနဲ့ TikTok/YouTube Shorts တင်လို့ကောင်းမယ့် Movie Recap Script တစ်ခု ရေးပေးပါ။ Hook section နဲ့ ဇာတ်လမ်းအကျဉ်း ပါဝင်ပါစေ။"
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt]
                )
                
                st.success("✨ Recap Script ထွက်လာပါပြီ!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"မှားယွင်းမှု ရှိနေပါသည်: {e}")
          
