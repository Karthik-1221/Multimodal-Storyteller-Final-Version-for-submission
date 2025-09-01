# main.py

import streamlit as st
import google.generativeai as genai
import requests
import json
from PIL import Image
import io
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components
import base64
from elevenlabs.client import ElevenLabs

# Load environment variables at the very beginning of the script.
load_dotenv()


# --- 1. Configuration and Setup ---

# set_page_config() must be the first Streamlit command.
st.set_page_config(layout="wide", page_title="The Multimodal Storyteller", page_icon="🪶")

def load_api_keys():
    """Loads API keys securely from Streamlit secrets or a .env file."""
    try:
        google_api_key = st.secrets["GOOGLE_API_KEY"]
        stability_api_key = st.secrets["STABILITY_API_KEY"]
        elevenlabs_api_key = st.secrets["ELEVENLABS_API_KEY"]
    except (KeyError, FileNotFoundError):
        google_api_key = os.getenv("GOOGLE_API_KEY")
        stability_api_key = os.getenv("STABILITY_API_KEY")
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    return google_api_key, stability_api_key, elevenlabs_api_key


GOOGLE_API_KEY, STABILITY_API_KEY, ELEVENLABS_API_KEY = load_api_keys()

# Configure APIs
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.error("Google API Key not found. Please set it in your secrets or .env file.")
    st.stop()

if not ELEVENLABS_API_KEY:
    st.warning("ElevenLabs API Key not found. High-quality narration will be disabled.")

# --- 2. AI and Helper Functions ---

@st.cache_data
def generate_world_bible(theme, archetype, contradiction):
    """Generates the story's core rules and tone using Gemini."""
    prompt = f"""
    You are a world-building AI. Create a 'World Bible' for a new story based on these inputs:
    Core Theme: {theme}
    Protagonist Archetype: {archetype}
    The World's Core Contradiction: {contradiction}
    """
    with st.spinner("Generating the core of your universe..."):
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text

@st.cache_data
def generate_story_chapter(_story_context, _world_bible, user_choice):
    """Generates the next narrative chapter, choices, and image prompt."""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    generation_config = genai.types.GenerationConfig(temperature=0.9)
    prompt = f"""
    You are a multi-persona Storytelling Engine. Follow these steps precisely.
    The user's choice for the last chapter was: "{user_choice}".
    The full story context so far is: "{_story_context}".
    The secret World Bible for this universe is: "{_world_bible}".

    Step 1: Act as a Literary Artist. Write a rich, descriptive paragraph expanding on the user's choice.
    Step 2: Act as a Plot Theorist. Based on the new paragraph, generate three distinct, single-sentence plot choices. One must be a 'Wildcard'. Format these choices as a valid JSON array of strings.
    Step 3: Act as an Art Director. Based the paragraph from Step 1, write a concise, descriptive prompt for an AI image generator (comma-separated keywords).
    Step 4: Format your entire response as a single, raw JSON object with NO markdown formatting, using these exact keys: "narrative_chapter", "next_choices", and "image_prompt".
    """
    with st.spinner("The Storyteller is weaving the next chapter..."):
        try:
            response = model.generate_content(prompt, generation_config=generation_config)
            cleaned_json_string = response.text.strip().replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned_json_string)
            return data
        except Exception as e:
            st.error(f"Error processing AI response: {e}. The AI may have returned an unexpected format.")
            st.code(response.text)
            return None

@st.cache_data
def generate_image_stability(prompt):
    """Generates an image using the Stability.ai API with a valid model."""
    if not STABILITY_API_KEY:
        st.warning("Stability API Key not found. Image generation is disabled.")
        return None

    engine_id = "stable-diffusion-xl-1024-v1-0"
    API_URL = f"https://api.stability.ai/v1/generation/{engine_id}/text-to-image"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {STABILITY_API_KEY}",
    }
    payload = {
        "text_prompts": [{"text": f"cinematic, epic, high detail, masterpiece, {prompt}"}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }

    with st.spinner("The Stability artist is painting the scene..."):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            image_b64 = data["artifacts"][0]["base64"]
            return Image.open(io.BytesIO(base64.b64decode(image_b64)))
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP error with Stability API: {e.response.status_code}")
            st.json(e.response.json())
            return None
        except Exception as e:
            st.error(f"An error occurred with the Stability API: {e}")
            return None

def generate_and_play_audio(text, music_file="background_music.mp3"):
    """
    Generates audio using ElevenLabs and plays it via a custom HTML component
    that includes looping background music.
    """
    if not ELEVENLABS_API_KEY:
        st.warning("Cannot generate narration. ElevenLabs API Key is missing.")
        return

    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        with st.spinner("The Narrator is preparing their voice..."):
            # FIX: The 'model' parameter is not used in this specific method call.
            audio_data = client.text_to_speech.convert(
                voice_id="21m00Tcm4TlvDq8ikWAM",  # This is the ID for "Rachel". Replace with your chosen Voice ID.
                text=text
            )

        audio_b64 = base64.b64encode(audio_data).decode()
        
        if os.path.exists(music_file):
            with open(music_file, "rb") as f:
                music_b64 = base64.b64encode(f.read()).decode()
        else:
            st.warning(f"Background music file '{music_file}' not found.")
            music_b64 = ""

        components.html(f"""
            <audio id="bg-music" loop>
                <source src="data:audio/mp3;base64,{music_b64}" type="audio/mp3">
            </audio>
            <audio id="narration">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>

            <script>
                const bgMusic = document.getElementById('bg-music');
                const narration = document.getElementById('narration');
                
                // Autoplay background music softly
                bgMusic.volume = 0.2;
                bgMusic.play().catch(e => console.error("Autoplay for music failed:", e));

                // When narration starts playing, lower music volume even more
                narration.onplay = function() {{
                    bgMusic.volume = 0.1;
                }};

                // When narration ends, restore music volume
                narration.onended = function() {{
                    bgMusic.volume = 0.2;
                }};
                
                // Start playing the narration
                narration.play().catch(e => console.error("Autoplay for narration failed:", e));
            </script>
        """, height=0)

    except Exception as e:
        st.error(f"An error occurred with the audio generation: {e}")


# --- 3. Streamlit Application UI and Logic ---

st.title("The Multimodal Storyteller 🪶")
st.markdown("Co-create a unique saga with AI. Forge a world, make choices, and bring your story to life with generated art and audio.")

if 'app_stage' not in st.session_state:
    st.session_state.app_stage = "world_forge"
    st.session_state.world_bible = None
    st.session_state.story_chapters = []
    st.session_state.latest_choices = []

if st.session_state.app_stage == "world_forge":
    with st.form("world_forge_form"):
        st.header("Step 1: Forge Your World")
        theme = st.selectbox("Choose a Core Theme:", ["Revenge", "Discovery", "Betrayal", "Survival", "Redemption"])
        archetype = st.selectbox("Choose a Protagonist Archetype:", ["The Outcast", "The Reluctant Hero", "The Idealist", "The Trickster"])
        contradiction = st.text_input("What is a strange contradiction in this world?", "A city of high magic where everyone is profoundly bored.")
        if st.form_submit_button("Set the Stage"):
            st.session_state.world_bible = generate_world_bible(theme, archetype, contradiction)
            st.session_state.app_stage = "story_start"
            st.rerun()

elif st.session_state.app_stage == "story_start":
    st.header("Step 2: Begin Your Saga")
    st.info("Your world has been created. Start your story with a single, compelling sentence.")
    with st.form("start_story_form"):
        initial_prompt = st.text_area("Your opening sentence:", "The last starship captain woke from cryo-sleep to the sound of a ticking clock.")
        if st.form_submit_button("Start the Saga") and initial_prompt:
            # Use a placeholder for story context as it's the beginning
            ai_response = generate_story_chapter(initial_prompt, st.session_state.world_bible, initial_prompt)
            if ai_response:
                initial_image = generate_image_stability(ai_response["image_prompt"])
                # Add user's first line
                st.session_state.story_chapters.append({"text": initial_prompt, "image": None})
                # Add AI's first response with an image
                st.session_state.story_chapters.append({"text": ai_response["narrative_chapter"], "image": initial_image})
                st.session_state.latest_choices = ai_response["next_choices"]
                st.session_state.app_stage = "story_cycle"
                st.rerun()

elif st.session_state.app_stage == "story_cycle":
    st.header("Your Saga Unfolds...")
    for chapter in st.session_state.story_chapters:
        if chapter["image"]:
            st.image(chapter["image"], use_column_width=True)
        st.markdown(f"*{chapter['text']}*")
        st.markdown("---")

    if st.session_state.story_chapters:
        full_story_text = " ".join([ch['text'] for ch in st.session_state.story_chapters])
        if st.button("🔊 Narrate Full Saga"):
            generate_and_play_audio(full_story_text)

    st.header("What Happens Next?")
    if 'latest_choices' in st.session_state and st.session_state.latest_choices:
        with st.form("choice_form"):
            choice_made = st.radio("Choose a path:", st.session_state.latest_choices, key="choice_radio")
            if st.form_submit_button("Weave Next Chapter"):
                story_so_far = " ".join([ch['text'] for ch in st.session_state.story_chapters])
                ai_response = generate_story_chapter(story_so_far, st.session_state.world_bible, choice_made)
                if ai_response:
                    new_image = generate_image_stability(ai_response["image_prompt"])
                    st.session_state.story_chapters.append({"text": ai_response["narrative_chapter"], "image": new_image})
                    st.session_state.latest_choices = ai_response["next_choices"]
                    
                    # Automatically narrate the new chapter
                    generate_and_play_audio(ai_response["narrative_chapter"])
                    
                    st.rerun()

# --- Restart Button ---
st.sidebar.markdown("---")
st.sidebar.header("Controls")
if st.sidebar.button("Start a New Saga (Restart)"):
    # Clear all session state keys to start fresh
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 10px;">
    <p>Created by <b>Karthik</b></p>
</div>
""", unsafe_allow_html=True)
