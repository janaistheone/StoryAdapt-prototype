import openai
import streamlit as st

# Page Configuration
st.set_page_config(page_title="StoryAdapt AI", page_icon="📝", layout="wide")

st.title("📝 StoryAdapt: AI Adaptive Storytelling Engine")
st.caption(
    "Transform raw news into target-tailored personas while freezing core facts."
)

# API Key Input
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")

if api_key:
  client = openai.OpenAI(api_key=api_key)

  # Raw News Input Interface
  raw_news = st.text_area(
      "Paste Raw Journalistic Article / News Here:",
      height=200,
      placeholder=(
          "Insert the original news article with numbers, dates, and facts..."
      ),
  )

  # Target Persona Selection
  persona = st.selectbox(
      "Select Target Audience Persona:",
      [
          "Gen-Z / Trend Persona (Hooks, Shorts Script, Bullet Points)",
          "Expert / Executive Persona (Data-Dense, Strategic Analysis)",
          "General / Accessible Persona (Plain Language, Simplified Concept)",
      ],
  )

  if st.button("Adapt Story 🚀", type="primary"):
    if not raw_news.strip():
      st.warning("Please paste a news article first.")
    else:
      with st.spinner(
          "Processing Fact-Lock Engine & Generating Adaptation..."
      ):
        system_prompt = """
                You are StoryAdapt, an advanced AI adaptive storytelling engine for newsrooms.
                YOUR CRITICAL RULE IS FACT-LOCK:
                1. Identify and FREEZE all core journalistic anchors: numbers, dates, statistics, proper names, and direct quotes.
                2. Do NOT hallucinate, assume, or alter any factual details from the source text.
                3. Rewrite the story into the requested audience persona while maintaining 100% factual fidelity.
                """

        user_prompt = f"""
                Source Article:
                {raw_news}

                Target Persona: {persona}

                Please output the response structured with:
                - Fact-Lock Status (List extracted verified dates/numbers)
                - Persona Adaptation Content
                """

        try:
          response = client.chat.completions.create(
              model="gpt-4o",
              messages=[
                  {"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_prompt},
              ],
              temperature=0.3,
          )

          result = response.choices[0].message.content
          st.success("Adaptation Complete!")
          st.markdown("---")
          st.markdown(result)

        except Exception as e:
          st.error(f"Error generating output: {e}")
