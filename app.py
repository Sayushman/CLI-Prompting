import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional

# ------------------- SETUP ---------------------
load_dotenv()
client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# ------------------- TOOL FUNCTIONS ---------------------
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

# ------------------- PROMPT ---------------------
SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You must follow a structured reasoning process with START, PLAN, and OUTPUT steps.
You can call available tools when necessary.

Rules:
- Always return a valid JSON with:
  {"step": "START" | "PLAN" | "TOOL" | "OUTPUT", "content": "string", "tool": "string", "input": "string"}

Available Tools:
- get_weather(city:str)
- run_command(cmd:str)
"""

# ------------------- OUTPUT MODEL ---------------------
class MyOutputFormat(BaseModel):
    step: str = Field(..., description="Step ID: START, PLAN, TOOL, OUTPUT")
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None

# ------------------- STREAMLIT UI ---------------------
st.set_page_config(page_title="AI Agent Dashboard", layout="wide")
st.markdown("""
<h1 style="
    text-align: center;
    font-family: sans-serif;
    font-size: 60px;
">
🤖 Aayu-Agentic
</h1>
""", unsafe_allow_html=True)
# st.title("🤖 Aayu-Agentic")
st.write("Ask your query below and see how the AI reasons step-by-step using tools...")

user_query = st.text_input("💬 Enter your query here based on real-time tools:", placeholder="e.g., Enter your query here ..... ")

if user_query:
    message_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    message_history.append({"role": "user", "content": user_query})

    plan_output = []
    final_output = ""

    with st.spinner("🤔 Thinking..."):
        while True:
            response = client.chat.completions.parse(
                model="gemini-2.5-flash",
                response_format=MyOutputFormat,
                messages=message_history
            )

            parsed = response.choices[0].message.parsed
            raw = response.choices[0].message.content
            message_history.append({"role": "assistant", "content": raw})

            # Display each reasoning step
            if parsed.step == "START":
                st.markdown(f"**🔥 START:** {parsed.content}")  

            elif parsed.step == "PLAN":
                st.markdown(f"**🤔 PLAN:** {parsed.content}")
                plan_output.append(parsed.content)

            elif parsed.step == "TOOL":
                st.markdown(f"**🔧 TOOL CALL:** `{parsed.tool}` with input `{parsed.input}`")
                if parsed.tool in available_tools:
                    tool_response = available_tools[parsed.tool](parsed.input)
                    st.markdown(f"**🧠 TOOL RESPONSE:** {tool_response}")

                    # Feed observation back into message history
                    message_history.append({
                        "role": "developer",
                        "content": json.dumps({
                            "step": "OBSERVE",
                            "tool": parsed.tool,
                            "input": parsed.input,
                            "output": tool_response
                        })
                    })
                else:
                    st.error(f"Unknown tool: {parsed.tool}")

            elif parsed.step == "OUTPUT":
                final_output = parsed.content
                st.success(f"**✅ FINAL OUTPUT:** {final_output}")
                break

# ------------------- FOOTER ---------------------
st.markdown("---")
st.markdown(" 🔵 **Developed by Ayushman Sengupta** — AI Agent Dashboard with real-time tools") 
