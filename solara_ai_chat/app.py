"""
# Solara AI Chat Application

A web application built with Solara that provides an interactive chat interface with OpenAI's GPT models.
"""

import solara
from typing import List, Dict, Callable
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
import solara.lab
from solara.lab import task

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Type for chat messages
MessageDict = Dict[str, str]

# Initialize reactive variables
messages: solara.Reactive[List[MessageDict]] = solara.reactive([])
chat_open: solara.Reactive[bool] = solara.reactive(False)  # Control chat panel visibility
show_suggestions: solara.Reactive[bool] = solara.reactive(True)  # Control prompt suggestions visibility

# Define some example prompts
EXAMPLE_PROMPTS = [
    "Tell me a joke",
    "Explain quantum computing",
    "Write a short poem",
    "Give me a coding challenge",
    "What's the meaning of life?",
]

def no_api_key_message():
    """Display a message when no API key is provided."""
    return "⚠️ No OpenAI API key found. Please add your API key to the .env file."

def toggle_chat():
    """Toggle the chat panel open/closed state."""
    chat_open.value = not chat_open.value
    # Reset suggestions visibility when opening chat
    if chat_open.value and not messages.value:
        show_suggestions.value = True

@solara.component
def ChatPanel():
    """Chat panel component."""
    # Add CSS for the chat panel layout
    solara.Style("""
    .chat-panel-container {
        display: flex;
        flex-direction: column;
        height: 100vh !important;
        overflow: hidden;
        padding: 0 !important;
        margin: 0 !important;
        row-gap: 0 !important;
    }
    
    .chat-header {
        padding: 16px;
        background-color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
    }
    
    .chat-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        position: relative;
        height: calc(100vh - 48px - 64px) !important;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 0 16px;
        display: flex;
        flex-direction: column;
    }
    
    .prompt-suggestions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        padding: 0px 16px 8px 16px;
        margin: 0;
        background-color: #ffffff;
    }
    """)
    
    with solara.Column(classes=["chat-panel-container"], style={"row-gap": "0", "padding": "0", "margin": "0"}):
        # Chat header
        with solara.Row(classes=["chat-header"]):
            solara.Text("Chat with AI Assistant")
            solara.Button(
                "✕",
                text=True,
                on_click=toggle_chat
            )
        
        # Prompt suggestions at the top
        if show_suggestions.value:
            with solara.Row(classes=["prompt-suggestions"]):
                for prompt in EXAMPLE_PROMPTS:
                    def create_click_handler(p=prompt):
                        def click_handler():
                            prompt_ai(p)
                        return click_handler

                    solara.Button(
                        prompt,
                        on_click=create_click_handler(),
                        text=True,
                        outlined=True
                    )
        
        # Chat content (messages)
        with solara.Column(classes=["chat-content"]):
            with solara.Column(classes=["chat-messages"]):
                with solara.lab.ChatBox():
                    for item in messages.value:
                        with solara.lab.ChatMessage(
                            user=item["role"] == "user",
                            avatar=True,
                            name="You" if item["role"] == "user" else "AI Assistant"
                        ):
                            solara.Markdown(item["content"])
                
                # Show loading indicator when AI is generating a response
                if prompt_ai.pending:
                    with solara.Row(style={
                        "margin-top": "8px",
                        "display": "flex",
                        "align-items": "center",
                        "gap": "8px"
                    }):
                        solara.Text("AI is thinking...", style={"color": "#666"})
                        solara.ProgressLinear(style={"width": "60px"})

@solara.component
def Page():
    """Main page component."""
    # Add global CSS for the layout
    solara.Style("""
    body {
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }
    
    .app-bar {
        display: flex;
        width: 100%;
        background-color: #1976d2;
        color: white;
        height: 48px;
        align-items: center;
        padding: 0 16px;
        box-sizing: border-box;
        position: relative;
        z-index: 1001;
    }
    
    .app-title {
        flex-grow: 1;
        font-size: 1.25rem;
        font-weight: 500;
    }
    
    .app-buttons {
        display: flex;
        gap: 8px;
        transition: transform 0.3s ease-in-out;
    }
    
    .app-buttons.shifted {
        transform: translateX(-400px);
    }
    
    .chat-panel {
        position: fixed;
        top: 0;
        right: -400px;
        width: 400px;
        height: 100vh;
        background: white;
        box-shadow: -2px 0 12px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease-in-out;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        padding: 0 !important;
        margin: 0 !important;
        row-gap: 0 !important;
        overflow: hidden;
    }
    
    .chat-panel.open {
        transform: translateX(-400px);
    }
    
    .chat-input-container {
        padding: 16px;
        background-color: #ffffff;
        display: flex;
        justify-content: center;
        box-sizing: border-box;
        position: fixed;
        bottom: 0;
        right: -400px;
        width: 400px;
        z-index: 1000;
        transition: transform 0.3s ease-in-out;
    }
    
    .chat-input-container.open {
        transform: translateX(-400px);
    }
    
    /* Fix chat input width */
    .chat-input-container > div {
        width: 100% !important;
        max-width: 368px !important;
    }
    
    .chat-input-container .v-input {
        width: 100% !important;
    }
    
    /* Fix the input field itself */
    .chat-input-container .v-text-field__slot {
        width: 100% !important;
    }
    
    .chat-input-container input {
        width: 100% !important;
    }
    
    .main-content {
        padding: 24px;
        max-width: 1200px;
        margin: 0 auto;
        min-height: calc(100vh - 48px);
    }
    """)
    
    # Custom App Bar
    with solara.Row(classes=["app-bar"]):
        solara.Text("My App", classes=["app-title"])
        
        buttons_classes = ["app-buttons"]
        if chat_open.value:
            buttons_classes.append("shifted")
            
        with solara.Row(classes=buttons_classes):
            solara.Button("Home", text=True)
            solara.Button("About", text=True)
            solara.Button(
                "AI Chat",
                text=True,
                on_click=toggle_chat
            )
    
    # Main content area
    with solara.Column(classes=["main-content"]):
        solara.Markdown("# Welcome to My App")
        solara.Markdown("Click the AI Chat button in the navigation bar to start chatting!")
    
    # Chat panel (outside the main container to allow fixed positioning)
    chat_panel_classes = ["chat-panel"]
    if chat_open.value:
        chat_panel_classes.append("open")
        
    with solara.Column(classes=chat_panel_classes):
        ChatPanel()
    
    # Chat input container (separate from the chat panel to control visibility)
    chat_input_classes = ["chat-input-container"]
    if chat_open.value:
        chat_input_classes.append("open")
        
    with solara.Row(classes=chat_input_classes):
        solara.lab.ChatInput(
            send_callback=prompt_ai,
            disabled_send=prompt_ai.pending,
            autofocus=True
        ).key("chat-input")

@task
async def prompt_ai(prompt: str = ""):
    """Send a prompt to the AI and get a response."""
    if not os.getenv("OPENAI_API_KEY"):
        messages.value = [{"role": "assistant", "content": no_api_key_message()}]
        return

    # Add user message
    if prompt:
        messages.value = messages.value + [{"role": "user", "content": prompt}]
        # Hide suggestions after user sends a message
        show_suggestions.value = False

    # Get AI response
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in messages.value]
        )
        ai_message = completion.choices[0].message.content
        messages.value = messages.value + [{"role": "assistant", "content": ai_message}]
    except Exception as e:
        logging.error(f"Error getting AI response: {e}")
        messages.value = messages.value + [
            {"role": "assistant", "content": f"Sorry, I encountered an error: {str(e)}"}
        ]

# Add a welcome message when the app starts
if not messages.value:
    messages.value = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]
