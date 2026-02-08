"""
Unit tests for ChatGPT Tool
Run with: python -m pytest test_chatgpt.py -v
"""

import pytest
import os
from dotenv import load_dotenv
from chatgpt_tool import ChatGPTTool
from advanced_chatgpt import AdvancedChatGPTTool, ChatGPTSpecialist

# Load environment variables
load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')


@pytest.mark.skipif(not API_KEY, reason="OPENAI_API_KEY not set")
class TestChatGPTTool:
    """Test ChatGPT Tool basic functionality"""
    
    @pytest.fixture
    def chatgpt(self):
        """Create a ChatGPT instance for testing"""
        return ChatGPTTool(api_key=API_KEY)
    
    def test_initialization(self, chatgpt):
        """Test tool initialization"""
        assert chatgpt is not None
        assert chatgpt.api_key == API_KEY
        assert chatgpt.model == "gpt-3.5-turbo"
    
    def test_chat_simple_message(self, chatgpt):
        """Test sending a simple message"""
        response = chatgpt.chat("Say 'Hello, World!'")
        assert response is not None
        assert len(response) > 0
        assert "error" not in response.lower() or "Hello" in response
    
    def test_conversation_history(self, chatgpt):
        """Test conversation history tracking"""
        chatgpt.chat("What is 2+2?")
        history = chatgpt.get_history()
        
        assert len(history) >= 2
        assert history[0]['role'] == 'user'
        assert history[1]['role'] == 'assistant'
    
    def test_clear_history(self, chatgpt):
        """Test clearing conversation history"""
        chatgpt.chat("Test message")
        assert len(chatgpt.get_history()) > 0
        
        chatgpt.clear_history()
        assert len(chatgpt.get_history()) == 0
    
    def test_set_model(self, chatgpt):
        """Test changing model"""
        chatgpt.set_model("gpt-4")
        assert chatgpt.model == "gpt-4"


@pytest.mark.skipif(not API_KEY, reason="OPENAI_API_KEY not set")
class TestAdvancedChatGPTTool:
    """Test Advanced ChatGPT Tool features"""
    
    @pytest.fixture
    def advanced_chatgpt(self):
        """Create an Advanced ChatGPT instance for testing"""
        return AdvancedChatGPTTool(api_key=API_KEY)
    
    def test_memory_functionality(self, advanced_chatgpt):
        """Test memory storage and recall"""
        advanced_chatgpt.remember("user_name", "Alice")
        assert advanced_chatgpt.recall("user_name") == "Alice"
    
    def test_system_role_change(self, advanced_chatgpt):
        """Test changing system role"""
        new_role = "You are a pirate."
        advanced_chatgpt.set_system_role(new_role)
        assert advanced_chatgpt.system_role == new_role
    
    def test_temperature_setting(self, advanced_chatgpt):
        """Test temperature setting"""
        advanced_chatgpt.set_temperature(1.5)
        assert advanced_chatgpt.temperature == 1.5
        
        # Test boundary
        advanced_chatgpt.set_temperature(3.0)
        assert advanced_chatgpt.temperature == 2.0
    
    def test_max_tokens_setting(self, advanced_chatgpt):
        """Test max tokens setting"""
        advanced_chatgpt.set_max_tokens(500)
        assert advanced_chatgpt.max_tokens == 500
    
    def test_conversation_length(self, advanced_chatgpt):
        """Test conversation statistics"""
        advanced_chatgpt.chat("Hello")
        stats = advanced_chatgpt.get_conversation_length()
        
        assert stats['total_messages'] >= 2
        assert stats['user_messages'] >= 1
        assert stats['assistant_messages'] >= 1


class TestChatGPTSpecialist:
    """Test ChatGPT Specialist instances"""
    
    def test_code_assistant(self):
        """Test code assistant creation"""
        code_bot = ChatGPTSpecialist.code_assistant()
        assert code_bot is not None
        assert "programming" in code_bot.system_role.lower()
    
    def test_content_writer(self):
        """Test content writer creation"""
        writer = ChatGPTSpecialist.content_writer()
        assert writer is not None
        assert "content" in writer.system_role.lower()
    
    def test_data_analyst(self):
        """Test data analyst creation"""
        analyst = ChatGPTSpecialist.data_analyst()
        assert analyst is not None
        assert "data" in analyst.system_role.lower()
    
    def test_creative_writer(self):
        """Test creative writer creation"""
        creative = ChatGPTSpecialist.creative_writer()
        assert creative is not None
        assert creative.temperature > 0.7


# Basic tests that don't require API
class TestBasicFunctionality:
    """Test basic functionality without API calls"""
    
    def test_missing_api_key(self):
        """Test error handling for missing API key"""
        # Temporarily remove API key
        old_key = os.environ.get('OPENAI_API_KEY')
        os.environ.pop('OPENAI_API_KEY', None)
        
        try:
            with pytest.raises(ValueError):
                ChatGPTTool(api_key=None)
        finally:
            # Restore API key
            if old_key:
                os.environ['OPENAI_API_KEY'] = old_key


if __name__ == "__main__":
    pytest.main([__file__, "-v"])