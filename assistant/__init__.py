"""Student Support AI assistant package.

This package exposes the main public API used by the CLI and any UI:
Basically regroup every modules the UI needs to run the program into a package

"""
# Re-export commonly used types forconvenient imports
from assistant.config import AssistantConfig
from assistant.models import AssistantResponse, ConversationStats
from assistant.support_assistant import SupportAssistant

# Public package interface
__all__ = ["AssistantConfig", "AssistantResponse", "ConversationStats", "SupportAssistant"]
