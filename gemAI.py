import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ---------------- SETUP -----------------
load_dotenv()
client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------------- TOOLS -----------------
def run_command(cmd: str):
    result = os.popen(cmd).read()
    return result if result else "No output or invalid command."

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text.strip()}"
    return "Something went wrong while fetching weather."

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

# ---------------- PROMPT -----------------
SYSTEM_PROMPT = """
You're an AI agent that solves queries step-by-step.

You must follow these phases:
1️⃣ START — acknowledge the query.
2️⃣ PLAN — think about how to solve it.
3️⃣ TOOL — call a tool if needed.
4️⃣ OUTPUT — give final answer.

Each output must be valid JSON in this format:
{"step": "START" | "PLAN" | "TOOL" | "OUTPUT", "content": "string", "tool": "string or null", "input": "string or null"}

Example:
{"step":"START","content":"User asked a math question"}
{"step":"PLAN","content":"I will apply BODMAS rule"}
{"step":"OUTPUT","content":"Answer is 7.5"}
"""

# ---------------- STREAMLIT UI -----------------
st.set_page_config(page_title="AI Reasoning Dashboard", layout="wide")
st.title("🤖 AI Chain-of-Thought Dashboard")
st.markdown("Ask me anything — I'll show my reasoning step-by-step.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = st.chat_input("💬 Type your query here...")

# ---- Chat history ----
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# ---- Process new input ----
if user_query:
    st.chat_message("user").write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    reasoning_output = st.chat_message("assistant")
    placeholder = reasoning_output.empty()
    steps_text = ""

    with st.spinner("Thinking..."):
        while True:
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=st.session_state.messages,
                temperature=0.5,
            )

            result_text = response.choices[0].message.content.strip()
            placeholder.markdown(f"🧠 Raw Model Output:\n```\n{result_text}\n```")

            # Try parsing JSON (sometimes Gemini sends multiple)
            try:
                parsed = json.loads(result_text)
            except:
                break  # stop if not valid JSON

            step = parsed.get("step", "").upper()
            content = parsed.get("content", "")
            tool = parsed.get("tool", None)
            tool_input = parsed.get("input", None)

            if step == "START":
                st.markdown(f"🟢 **START:** {content}")

            elif step == "PLAN":
                st.markdown(f"🧩 **PLAN:** {content}")

            elif step == "TOOL" and tool:
                st.markdown(f"🔧 **TOOL CALL:** `{tool}` with input `{tool_input}`")

                if tool in available_tools:
                    tool_result = available_tools[tool](tool_input)
                    st.markdown(f"🧠 **TOOL RESPONSE:** {tool_result}")

                    # feed observation back to the model
                    st.session_state.messages.append({
                        "role": "developer",
                        "content": json.dumps({
                            "step": "OBSERVE",
                            "tool": tool,
                            "input": tool_input,
                            "output": tool_result
                        })
                    })
                else:
                    st.error(f"Unknown tool: {tool}")

            elif step == "OUTPUT":
                st.success(f"✅ **FINAL ANSWER:** {content}")
                st.session_state.messages.append({"role": "assistant", "content": content})
                break

# ---- Footer ----
st.markdown("---")
st.caption("🚀 Built by **Ayushman Sengupta** — Streamlit + Gemini AI Agent")

