from typing import Tuple, Dict, Union
import os
#from dotenv import load_dotenv
import requests
import json
import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage, FunctionDefinition, ChatCompletionsToolDefinition, ChatCompletionsToolChoicePreset
from azure.core.credentials import AzureKeyCredential


endpoint = "https://models.inference.ai.azure.com"
model_name = "mistral-small-2503"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

load_dotenv()
EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')

def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    response = json.loads(requests.get(url).text)
    print("Exchange API Response:", response)
    # Return as a tuple as per the original function signature
    return (base, target, amount, f'{response["conversion_result"]:.2f}', response["conversion_rate"])

def call_llm(user_input: str):
    """Make a call to the LLM with the user input as the prompt.
    The LLM will decide whether to use tool calls or not based on the input."""

    exchange_info = ChatCompletionsToolDefinition(
        function=FunctionDefinition(
            name="get_exchange_rate",
            description="Convert a given amount of money from one currency to another. Each currency will be represented as a 3-letter code",
            parameters={
                "type": "object",
                "properties": {
                    "base": {
                        "type": "string",
                        "description": "The base or original currency.",
                    },
                    "target": {
                        "type": "string",
                        "description": "The target or converted currency",
                    },
                    "amount": {
                        "type": "string",
                        "description": "The amount of money to convert from the base currency.",
                    },
                },
                "required": ["base", "target", "amount"],
                "additionalProperties": False,
            },
        )
    )

    tools = [exchange_info]              
    
    try:
        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant. If the user asks about currency conversion or exchange rates, use the get_exchange_rate function. For all other queries, respond directly."),
                UserMessage(content=user_input),
            ],
            tools=tools,
            tool_choice="auto",    
            temperature=0.7,
            top_p=0.95,
            max_tokens=1000,
            model=model_name,
        )
        return response
    except Exception as e:
        print(f"Exception {e}")
        raise e

def run_pipeline(user_input: str):
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    try:
        response = call_llm(user_input)
        print("LLM Response:", response)
        
        if response.choices[0].finish_reason == "tool_calls":
            # LLM decided to use tool calls for currency conversion
            tool_call = response.choices[0].message.tool_calls[0]
            if tool_call.function.name == "get_exchange_rate":
                response_arguments = json.loads(tool_call.function.arguments)
                base = response_arguments["base"]
                target = response_arguments["target"]
                amount = response_arguments["amount"]
                
                # Call the get_exchange_rate function with the extracted arguments
                base, target, amount, conversion_result, conversion_rate = get_exchange_rate(base, target, amount)
                
                return {
                    "type": "conversion",
                    "base": base,
                    "target": target,
                    "amount": amount,
                    "conversion_result": conversion_result,
                    "conversion_rate": conversion_rate
                }
            else:
                return {
                    "type": "error",
                    "message": f"Unknown tool call: {tool_call.function.name}"
                }
        elif response.choices[0].finish_reason == "stop":
            # LLM decided to respond directly without tool calls
            return {
                "type": "general",
                "content": response.choices[0].message.content
            }
        else:
            return {
                "type": "error",
                "message": f"Unexpected finish reason: {response.choices[0].finish_reason}"
            }
    except Exception as e:
        return {
            "type": "error",
            "message": str(e)
        }

# Set the title of the app
st.title("AI Assistant with Currency Conversion")

# Create a text input box
user_input = st.text_input("Ask me anything or request currency conversion:")

# Create a submit button
if st.button("Submit"):
    if not user_input:
        st.warning("Please enter a question or currency conversion request.")
    else:
        # Call the pipeline and get the result
        with st.spinner("Processing your request..."):
            result = run_pipeline(user_input)
        
        # Display the result based on its type
        if result["type"] == "conversion":
            # Display the conversion result and rate
            st.success(f"{result['amount']} {result['base']} = {result['conversion_result']} {result['target']}")
            st.info(f"Conversion rate: 1 {result['base']} = {result['conversion_rate']} {result['target']}")
        elif result["type"] == "general":
            # Display the general response
            st.write(result["content"])
        elif result["type"] == "error":
            # Display the error message
            st.error(f"Error: {result['message']}")


# Submit button
if st.button("Submit"):
    # Display the input text below the text box
    run_pipeline(user_input)
