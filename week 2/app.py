import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


# --------- YouTube transcript extraction ---------
def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    video_ids = qs.get('v')

    if not video_ids:
        raise ValueError(f"No video id found in URL: {url}")

    return video_ids[0]


# --------- Simple cleaning function ---------
def simple_clean(text):
    lines = text.split("\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]

    skip_words = ["pause the video", "thanks for watching", "feel free to"]
    cleaned_lines = []
    for line in lines:
        if not any(word.lower() in line.lower() for word in skip_words):
            cleaned_lines.append(line)

    cleaned_text = " ".join(cleaned_lines)
    return cleaned_text


# --------- Streamlit UI ---------
st.set_page_config(page_title="YouTube Summarizer", layout="centered")
st.title("🎥 YouTube Video Summarizer")

youtube_url = st.text_input("Enter YouTube video URL")

if st.button("Summarize"):
    if not youtube_url.strip():
        st.error("Please enter a YouTube URL")
    else:
        try:
            # 1️⃣ Extract video id
            video_id = extract_video_id(youtube_url)

            # 2️⃣ Fetch transcript
            api = YouTubeTranscriptApi()
            fetched = api.fetch(video_id, languages=['en'])
            text = "\n".join(snippet.text for snippet in fetched)

            # 3️⃣ Clean text
            cleaned_text = simple_clean(text)

            st.info("Transcript extracted and cleaned successfully!")

            # 4️⃣ Send cleaned text to FastAPI
            URL = "https://pennie-sabulous-rheba.ngrok-free.dev/summarize"
            headers = {"Authorization": "Bearer secret123"}
            payload = {
                "prompt": cleaned_text
            }

            with st.spinner("Summarizing..."):
                res = requests.post(URL, headers=headers, json=payload)
                res.raise_for_status()
                summary = res.json()["response"]

            # 5️⃣ Show result
            st.subheader("📝 Summary")
            st.write(summary)

        except Exception as e:
            st.error(f"Error: {e}")
