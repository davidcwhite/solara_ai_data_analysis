"""
# Solara AI Data Analysis

A web application built with Solara that provides an interactive chat interface with OpenAI's GPT models.
"""

import solara
from typing import List, Dict, Callable, cast
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
import solara.lab
from solara.lab import task
import pandas as pd
import numpy as np
from ipyaggrid import Grid
import ipywidgets as widgets
from IPython.display import display as ipy_display

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

# Define some example prompts related to data analysis
EXAMPLE_PROMPTS = [
    "What are the top-selling products?",
    "Show me sales trends by region",
    "Which customer segment has the highest revenue?",
    "Compare Q1 vs Q2 performance",
    "Identify underperforming products",
]

# Generate sample sales data
def generate_sample_data(rows=100):
    """Generate sample sales data for demonstration."""
    np.random.seed(42)  # For reproducibility
    
    # Define possible values for categorical columns
    regions = ['North', 'South', 'East', 'West', 'Central']
    product_categories = ['Electronics', 'Clothing', 'Home Goods', 'Groceries', 'Books']
    customer_segments = ['Retail', 'Corporate', 'Small Business', 'Government', 'Education']
    payment_methods = ['Credit Card', 'Cash', 'Bank Transfer', 'PayPal', 'Check']
    
    # Generate data
    data = {
        'Order ID': [f'ORD-{i:04d}' for i in range(1, rows + 1)],
        'Date': pd.date_range(start='2023-01-01', periods=rows),
        'Region': np.random.choice(regions, size=rows),
        'Product Category': np.random.choice(product_categories, size=rows),
        'Product Name': [f'Product {i}' for i in range(1, rows + 1)],
        'Quantity': np.random.randint(1, 20, size=rows),
        'Unit Price': np.round(np.random.uniform(10, 500, size=rows), 2),
        'Customer Segment': np.random.choice(customer_segments, size=rows),
        'Payment Method': np.random.choice(payment_methods, size=rows),
    }
    
    # Calculate total sales
    df = pd.DataFrame(data)
    df['Total Sales'] = df['Quantity'] * df['Unit Price']
    
    # Add some seasonality and trends
    month = df['Date'].dt.month
    df.loc[month.isin([11, 12]), 'Total Sales'] *= 1.5  # Holiday season boost
    df.loc[df['Product Category'] == 'Electronics', 'Total Sales'] *= 1.2  # Electronics premium
    
    return df

# Create sample data
sales_data = generate_sample_data(100)

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
def AgGrid(df, grid_options):
    """A wrapper component for ipyaggrid that works with Solara."""
    # Create a reactive height
    height = solara.use_reactive(500)
    
    # Create the grid element
    el = Grid.element(
        grid_data=df,
        grid_options=grid_options,
        theme="ag-theme-balham",
        columns_fit="auto",
        index=False,
        height=height.value
    )
    
    # Use effect to update the grid when data changes
    def update_grid():
        widget = cast(Grid, solara.get_widget(el))
        widget.grid_options = grid_options
        widget.update_grid_data(df)
        
        # Handle height properly - this is a workaround for ipyaggrid's height handling in Solara
        if isinstance(widget.height, int):
            height.set(f"{widget.height}px")
    
    solara.use_effect(update_grid, [df, grid_options])
    
    return el

@solara.component
def DataGrid():
    """Data grid component using ipyaggrid."""
    # Configure the grid options
    grid_options = {
        'columnDefs': [
            {'headerName': 'Order ID', 'field': 'Order ID', 'filter': True, 'sortable': True},
            {'headerName': 'Date', 'field': 'Date', 'filter': True, 'sortable': True},
            {'headerName': 'Region', 'field': 'Region', 'filter': True, 'sortable': True},
            {'headerName': 'Product Category', 'field': 'Product Category', 'filter': True, 'sortable': True},
            {'headerName': 'Product Name', 'field': 'Product Name', 'filter': True, 'sortable': True},
            {'headerName': 'Quantity', 'field': 'Quantity', 'filter': True, 'sortable': True},
            {'headerName': 'Unit Price', 'field': 'Unit Price', 'filter': True, 'sortable': True, 'type': 'numericColumn'},
            {'headerName': 'Customer Segment', 'field': 'Customer Segment', 'filter': True, 'sortable': True},
            {'headerName': 'Payment Method', 'field': 'Payment Method', 'filter': True, 'sortable': True},
            {'headerName': 'Total Sales', 'field': 'Total Sales', 'filter': True, 'sortable': True, 'type': 'numericColumn'},
        ],
        'defaultColDef': {
            'flex': 1,
            'minWidth': 100,
            'filter': True,
            'sortable': True,
            'resizable': True,
        },
        'enableRangeSelection': True,
        'animateRows': True,
        'pagination': True,
        'paginationPageSize': 10,
    }
    
    # Convert DataFrame to dictionary for the grid
    data = sales_data.to_dict('records')
    
    # Create a container for the grid
    with solara.Column(style={"height": "500px", "width": "100%"}):
        # Create the grid
        grid = Grid(
            grid_data=data,
            grid_options=grid_options,
            theme="ag-theme-balham",
            columns_fit="auto",
            index=False,
            height=500  # Integer value as required by ipyaggrid
        )
        solara.display(grid)

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
        solara.Text("Sales Data Analysis", classes=["app-title"])
        
        buttons_classes = ["app-buttons"]
        if chat_open.value:
            buttons_classes.append("shifted")
            
        with solara.Row(classes=buttons_classes):
            solara.Button("Dashboard", text=True)
            solara.Button("Reports", text=True)
            solara.Button(
                "AI Chat",
                text=True,
                on_click=toggle_chat
            )
    
    # Main content area
    with solara.Column(classes=["main-content"]):
        solara.Markdown("# Sales Data Dashboard")
        solara.Markdown("""
        This dashboard displays sales data that you can analyze. Use the AI Chat feature to ask questions about the data.
        
        Try asking questions like:
        - What are the top-selling products?
        - Show me sales trends by region
        - Which customer segment has the highest revenue?
        """)
        
        # Add the data grid
        DataGrid()
    
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
        # Create a system message that provides context about the data
        system_message = """
        You are an AI assistant helping with data analysis of sales data. The data includes:
        - Order information (Order ID, Date)
        - Product details (Category, Name, Quantity, Unit Price)
        - Customer information (Region, Customer Segment)
        - Payment details (Payment Method)
        - Sales metrics (Total Sales = Quantity * Unit Price)
        
        Provide insightful analysis and answer questions about the data. Be concise but thorough.
        """
        
        # Create the messages array with the system message
        message_list = [{"role": "system", "content": system_message}]
        message_list.extend([{"role": m["role"], "content": m["content"]} for m in messages.value])
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_list
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
        {"role": "assistant", "content": "Hello! I'm your AI data analysis assistant. I can help you analyze the sales data displayed in the dashboard. What would you like to know about the data?"}
    ]
