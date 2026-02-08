import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# Load environment variables
load_dotenv()

class AdvancedChatGPTTool:
    """Advanced ChatGPT tool with additional features like memory, context management, and custom behaviors"""
    
    def __init__(self, api_key=None, system_role="You are a helpful assistant."):
        """
        Initialize the Advanced ChatGPT tool
        
        Args:
            api_key (str): OpenAI API key
            system_role (str): System role/behavior for the AI
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found. Please set it in .env file.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"
        self.system_role = system_role
        self.conversation_history = []
        self.memory = {}  # Custom memory storage
        self.temperature = 0.7
        self.max_tokens = 2000
    
    def set_system_role(self, role):
        """Change the system role/behavior"""
        self.system_role = role
    
    def set_temperature(self, temperature):
        """Set temperature (0-2). Higher = more creative, Lower = more focused"""
        self.temperature = max(0, min(2, temperature))
    
    def set_max_tokens(self, max_tokens):
        """Set maximum response length"""
        self.max_tokens = max_tokens
    
    def remember(self, key, value):
        """Store information in memory"""
        self.memory[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
    
    def recall(self, key):
        """Retrieve stored information"""
        return self.memory.get(key, {}).get('value', None)
    
    def clear_memory(self):
        """Clear all stored memory"""
        self.memory = {}
    
    def chat(self, user_message):
        """
        Send a message with enhanced features
        
        Args:
            user_message (str): The user's message
        
        Returns:
            str: The AI's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare messages
        messages = [
            {"role": "system", "content": self.system_role}
        ]
        messages.extend(self.conversation_history[-10:])  # Keep last 10 messages for context
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def summarize_conversation(self):
        """Get a summary of the conversation"""
        if len(self.conversation_history) < 2:
            return "No conversation to summarize yet."
        
        summary_prompt = "Summarize the conversation above in 2-3 sentences."
        
        messages = [
            {"role": "system", "content": self.system_role},
        ]
        messages.extend(self.conversation_history)
        messages.append({
            "role": "user",
            "content": summary_prompt
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_conversation_length(self):
        """Get conversation statistics"""
        return {
            'total_messages': len(self.conversation_history),
            'user_messages': len([m for m in self.conversation_history if m['role'] == 'user']),
            'assistant_messages': len([m for m in self.conversation_history if m['role'] == 'assistant'])
        }


class ChatGPTSpecialist:
    """Specialized ChatGPT instances for specific roles"""
    
    @staticmethod
    def code_assistant():
        """Create a code assistant specialist"""
        return AdvancedChatGPTTool(
            system_role="You are an expert programming assistant. Help with coding questions, debugging, and best practices."
        )
    
    @staticmethod
    def content_writer():
        """Create a content writer specialist"""
        return AdvancedChatGPTTool(
            system_role="You are a professional content writer. Create engaging, well-structured, and original content."
        )
    
    @staticmethod
    def data_analyst():
        """Create a data analyst specialist"""
        return AdvancedChatGPTTool(
            system_role="You are an expert data analyst. Help with data analysis, visualization, and insights."
        )
    
    @staticmethod
    def creative_writer():
        """Create a creative writer specialist"""
        return AdvancedChatGPTTool(
            system_role="You are a creative fiction writer. Create engaging stories and imaginative content.",
            temperature=1.0
        )


if __name__ == "__main__":
    try:
        # Example: Code Assistant
        print("=" * 60)
        print("ChatGPT Advanced Tool - Code Assistant Example")
        print("=" * 60)
        
        code_bot = ChatGPTSpecialist.code_assistant()
        
        # Store some context
        code_bot.remember("project", "Python Flask Web App")
        
        print("\nCode Assistant initialized")
        print(f"Remembered project: {code_bot.recall('project')}")
        
        print("\nConversation started. Type 'quit' to exit, 'summary' for summary, 'stats' for statistics\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            if user_input.lower() == 'summary':
                print(f"\nSummary: {code_bot.summarize_conversation()}\n")
                continue
            
            if user_input.lower() == 'stats':
                stats = code_bot.get_conversation_length()
                print(f"\nStats: {stats}\n")
                continue
            
            if not user_input:
                continue
            
            print("\nAssistant: ", end="", flush=True)
            response = code_bot.chat(user_input)
            print(response + "\n")
    
    except ValueError as e:
        print(f"Error: {e}")