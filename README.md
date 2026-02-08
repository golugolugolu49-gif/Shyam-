# ChatGPT AI Tool

A simple yet powerful ChatGPT-like AI tool built with Python and OpenAI API. This project provides both a command-line interface and a Flask REST API for interacting with ChatGPT.

## Features

- ✅ Interactive chat interface with conversation history
- ✅ REST API endpoints for integration
- ✅ Support for system messages (custom AI behavior)
- ✅ Conversation history management
- ✅ Multiple model support (GPT-4, GPT-3.5-turbo, etc.)
- ✅ Easy configuration via environment variables

## Prerequisites

- Python 3.8+
- OpenAI API key (get it from https://platform.openai.com/api-keys)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/golugolugolu49-gif/Shyam-.git
cd Shyam-
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

## Usage

### Command-Line Interface

Run the interactive chat tool:

```bash
python chatgpt_tool.py
```

Example:
```
ChatGPT Tool - Type 'quit' to exit, 'clear' to clear history
--------------------------------------------------

You: Hello! What is Python?

AI: Python is a high-level, interpreted programming language known for its simplicity and readability...

You: Tell me a joke

AI: Why did the Python go to the bank? To get its "bytes" exchanged! 😄

You: quit
Goodbye!
```

### Flask REST API

Start the Flask server:

```bash
python flask_app.py
```

The API will be available at `http://localhost:5000`

#### API Endpoints

##### 1. Chat Endpoint
**POST** `/api/chat`

Send a message and get a response:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is artificial intelligence?",
    "system_message": "You are a helpful assistant."
  }'
```

Response:
```json
{
  "user_message": "What is artificial intelligence?",
  "ai_response": "Artificial intelligence (AI) is...",
  "success": true
}
```

##### 2. Get Conversation History
**GET** `/api/history`

```bash
curl http://localhost:5000/api/history
```

Response:
```json
{
  "history": [
    {
      "role": "user",
      "content": "What is AI?"
    },
    {
      "role": "assistant",
      "content": "AI is..."
    }
  ],
  "success": true
}
```

##### 3. Clear History
**POST** `/api/clear`

```bash
curl -X POST http://localhost:5000/api/clear
```

Response:
```json
{
  "message": "History cleared",
  "success": true
}
```

##### 4. Set Model
**POST** `/api/set-model`

```bash
curl -X POST http://localhost:5000/api/set-model \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4"}'
```

Response:
```json
{
  "message": "Model set to gpt-4",
  "success": true
}
```

##### 5. Health Check
**GET** `/api/health`

```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "ChatGPT Tool API"
}
```

## Project Structure

```
Shyam-/
├── chatgpt_tool.py      # Core ChatGPT implementation
├── flask_app.py         # Flask REST API
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Python Code Examples

### Basic Usage

```python
from chatgpt_tool import ChatGPTTool

# Initialize
chatgpt = ChatGPTTool()

# Single message
response = chatgpt.chat("What is Python?")
print(response)

# With system message
response = chatgpt.chat(
    "Tell me a joke",
    system_message="You are a funny comedian"
)
print(response)

# Get history
history = chatgpt.get_history()
print(history)

# Clear history
chatgpt.clear_history()
```

### Advanced Usage

```python
from chatgpt_tool import ChatGPTTool

chatgpt = ChatGPTTool()

# Change model
chatgpt.set_model("gpt-4")

# Multi-turn conversation
chatgpt.chat("Hi, my name is John")
chatgpt.chat("What did I just tell you?")
chatgpt.chat("Tell me something about myself")

# Get full history
history = chatgpt.get_history()
for message in history:
    print(f"{message['role'].upper()}: {message['content']}")
```

## Configuration

Edit `.env` file to customize:

```env
# OpenAI API Key (Required)
OPENAI_API_KEY=sk-your-api-key-here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

## Models Available

- `gpt-4` - Most capable, but more expensive
- `gpt-4-turbo-preview` - Fast and powerful
- `gpt-3.5-turbo` - Fast and cost-effective (default)
- `gpt-3.5-turbo-16k` - Extended context window

## Cost Estimation

Pricing varies by model. Check [OpenAI Pricing](https://openai.com/pricing) for current rates.

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you have created a `.env` file with your API key
- Verify the key is valid at https://platform.openai.com/api-keys

### API Rate Limits
- Implement rate limiting for production use
- Use exponential backoff for retries

### High Costs
- Start with `gpt-3.5-turbo` for lower costs
- Monitor API usage in your OpenAI dashboard

## Contributing

Feel free to fork, create issues, and submit pull requests!

## License

This project is open source and available under the MIT License.

## Support

For issues with the OpenAI API, check their [documentation](https://platform.openai.com/docs).

---

**Created by golugolugolu49-gif**
