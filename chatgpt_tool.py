import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatGPTTool:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.conversation_history = []
        self.system_message = "You are a helpful AI assistant."
    
    def set_system_message(self, message):
        """Set a custom system message for the AI"""
        self.system_message = message
    
    def chat(self, user_message):
        """Send a message and get a response from ChatGPT"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_message}
                ] + self.conversation_history,
                temperature=0.7,
                max_tokens=2000
            )
            
            assistant_message = response['choices'][0]['message']['content']
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self):
        """Get conversation history"""
        return self.conversation_history
    
    def change_model(self, model):
        """Change the AI model"""
        self.model = model

def main():
    """Main function for CLI interaction"""
    print("=== ChatGPT AI Tool ===")
    print("Commands: 'clear' to clear history, 'history' to view history, 'model' to change model, 'exit' to quit\n")
    
    chatbot = ChatGPTTool()
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'clear':
            chatbot.clear_history()
            print("Conversation history cleared.")
        elif user_input.lower() == 'history':
            print("\n--- Conversation History ---")
            for msg in chatbot.get_history():
                print(f"{msg['role'].upper()}: {msg['content']}\n")
        elif user_input.lower().startswith('model'):
            model = user_input.split(' ', 1)[1] if ' ' in user_input else "gpt-3.5-turbo"
            chatbot.change_model(model)
            print(f"Model changed to: {model}")
        else:
            response = chatbot.chat(user_input)
            print(f"\nAssistant: {response}\n")

if __name__ == "__main__":
    main()