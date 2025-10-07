 CLI Prompting

 🤖 Agentic AI Assistant with Chain-of-Thought Reasoning

An intelligent AI assistant built with Google's Gemini 2.5 Flash that uses chain-of-thought reasoning to solve problems step-by-step. The assistant can plan, use tools, and provide structured outputs while maintaining conversation context.

 ✨ Features

- Chain-of-Thought Reasoning: The AI breaks down problems into logical steps (PLAN → TOOL → OUTPUT)
- Tool Integration: Built-in tools for weather information and system command execution
- Structured JSON Output: Uses Pydantic for validated, structured responses
- Conversation Memory: Maintains context across multiple interactions
- Step-by-Step Transparency: See the AI's thinking process in real-time

 🛠️ Available Tools

1. get-weather(city: str): Fetches current weather information for any city
2. run-command(cmd: str): Executes Linux system commands (use with caution)

 📋 Prerequisites

- Python 3.8+
- Google Gemini API access
- OpenAI Python SDK

 🚀 Installation

1. Clone the repository:
 bash
git clone https://github.com/Sayushman/CLI-Prompting.git
cd CLI-Prompting 


2. Install required dependencies:
bash
pip install python-dotenv openai requests google-generativeai pydantic


3. Create a .env file in the project root:
 env
OPENAI-API-KEY=your-gemini-api-key-here


4. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

 💻 Usage

Run the assistant:

bash
python main.py


 Example Interactions

 Math Problem:

💁♂  Can you solve 2 + 3 * 5 / 10?
🤔   Seems like user is interested in math problems
🤔   Looking at the problem, we should solve this using BODMAS approach
🤔   First, we must multiply 3 * 5 = 15
🤔   Now the equation is 2 + 15 / 10
🤔   We must perform divide: 15 / 10 = 1.5
🤔   Now finally let's add: 2 + 1.5 = 3.5
🤖   3.5


 Weather Query:

💁♂  What is the weather in London?
🤔   User wants to know the weather of London
🤔   I have get-weather tool available for this query
🔧   get-weather(london)
🔧   get-weather(london) = The weather in london is Clear +15°C
🤔   Great, I got the weather info about London
🤖   The current weather in London is 15°C with clear skies


 🏗️ Architecture

The assistant follows a structured reasoning pattern:

1. PLAN: Breaks down the user query into logical steps
2. TOOL: Calls external tools when needed (weather, commands, etc.)
3. OBSERVE: Processes tool outputs
4. OUTPUT: Provides the final answer to the user

  Message Flow


User Input → System Prompt + History → Gemini Model → Structured Output
                    ↓                                        ↓
              Tool Execution ← TOOL Step                  PLAN Steps
                    ↓                                        ↓
              OBSERVE Step → Continue Planning          OUTPUT Step


 📁 Project Structure

agentic-ai-assistant/
├── main.py               Main application file
├── .env                  Environment variables (not in repo)
├── .gitignore            Git ignore file
├── requirements.txt      Python dependencies
└── README.md             This file


 🔧 Configuration

The system prompt can be customized in SYSTEM PROMPT variable. You can:
- Modify reasoning steps
- Add new tools
- Change output format
- Adjust examples

 🛡️ Security Considerations

⚠️  Warning: The run command tool executes system commands. Use with extreme caution:
- Never expose this publicly
- Validate all inputs
- Consider removing this tool in production
- Implement proper sandboxing

 📦 Dependencies


python-dotenv
openai
requests
google-generativeai
pydantic


Install all at once:

bash
pip install -r requirements.txt


 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

 🙏 Acknowledgments

- Google Gemini for the powerful language model
- OpenAI SDK for the convenient API interface
- wttr.in for weather data

 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions

 🔮 Future Enhancements

- [ ] Add more tools (calculator, file operations, web search)
- [ ] Implement streaming responses
- [ ] Add conversation export functionality
- [ ] Create web interface
- [ ] Add error recovery mechanisms
- [ ] Implement tool sandboxing
- [ ] Add unit tests

---

Made with ❤️ using Google Gemini 2.5 Flash
