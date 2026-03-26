import streamlit as st
import requests
import os

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Logic Simulator", layout="centered")

st.title("🧠 Logic Simulator")
st.write("Propositional Logic + Predicate Logic (AI Powered with Groq)")

# -------------------------------
# Propositional Logic Functions
# -------------------------------

def AND(p, q):
    return p and q

def OR(p, q):
    return p or q

def NOT(p):
    return not p

def IMPLIES(p, q):
    return (not p) or q

# -------------------------------
# Groq API Function
# -------------------------------

def analyze_with_groq(text):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "❌ API Key not found. Please set GROQ_API_KEY."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an AI that classifies whether a subject is human or not.

Sentence: "{text}"

Rules:
- If subject is a human → Human: Yes, Mortal: Yes
- If not → Human: No, Mortal: No

Answer ONLY in this format:
Human: Yes/No
Mortal: Yes/No
"""

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Error: {str(e)}"


# -------------------------------
# Tabs UI
# -------------------------------

tab1, tab2 = st.tabs(["🔹 Propositional Logic", "🔹 Predicate Logic (AI)"])

# -------------------------------
# Tab 1: Propositional Logic
# -------------------------------
with tab1:
    st.subheader("Propositional Logic Operations")

    p = st.selectbox("Select value for P", [True, False])
    q = st.selectbox("Select value for Q", [True, False])

    operation = st.selectbox(
        "Choose Operation",
        ["AND", "OR", "NOT", "IMPLIES"]
    )

    if st.button("Calculate Result"):
        if operation == "AND":
            result = AND(p, q)
        elif operation == "OR":
            result = OR(p, q)
        elif operation == "NOT":
            result = NOT(p)
        elif operation == "IMPLIES":
            result = IMPLIES(p, q)

        st.success(f"Result: {result}")

# -------------------------------
# Tab 2: Predicate Logic (AI)
# -------------------------------
with tab2:
    st.subheader("Predicate Logic using Groq AI")

    user_input = st.text_input("Enter a sentence or name")

    if st.button("Analyze Sentence"):
        if user_input.strip() == "":
            st.warning("Please enter something!")
        else:
            result = analyze_with_groq(user_input)

            st.markdown("### 🧾 Result:")
            st.code(result)

            # Optional explanation
            if "Human: Yes" in result:
                st.success("✔ This is identified as Human → Therefore Mortal")
            elif "Human: No" in result:
                st.error("✖ This is NOT Human → Therefore NOT Mortal")
