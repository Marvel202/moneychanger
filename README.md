# 💱 MoneyChanger

![Currency Exchange](https://img.shields.io/badge/Currency-Exchange-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![Azure AI](https://img.shields.io/badge/Azure-AI-0078D4)

A fun and intelligent currency conversion app powered by Azure AI that understands natural language requests and provides real-time exchange rates.

## ✨ Features

- 🗣️ **Natural Language Understanding**: Ask for currency conversions in plain English (or any language!)
- 💰 **Real-time Exchange Rates**: Get the latest conversion rates from the ExchangeRate API
- 🤖 **AI-Powered**: Uses Azure AI to intelligently parse your requests
- 💬 **General Q&A**: Ask any general questions when you're not converting currencies
- 🌐 **Multilingual Support**: Works with queries in multiple languages

## 🖼️ Screenshots

![App Screenshot](https://via.placeholder.com/800x400?text=MoneyChanger+Screenshot)

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Azure AI account with API access
- ExchangeRate API key

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/moneychanger.git
   cd moneychanger
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   GITHUB_TOKEN=your_azure_ai_key_here
   EXCHANGERATE_API_KEY=your_exchangerate_api_key_here
   ```

4. Run the app:
   ```bash
   streamlit run moneychanger.py
   ```

## 🧠 How It Works

The app uses a smart pipeline that:

1. Takes your natural language input
2. Sends it to Azure AI for processing
3. Lets the AI decide whether to:
   - Use the currency conversion tool for exchange rate requests
   - Respond directly for general questions
4. Displays the results in a user-friendly format

### Example Queries

- "Convert 100 USD to EUR"
- "What is 5000 JPY in HKD?"
- "Exchange rate for 200 GBP to CAD"
- "Why is the sky blue?" (general question)

## 🛠️ Technologies Used

- **Streamlit**: For the web interface
- **Azure AI**: For natural language understanding
- **ExchangeRate API**: For real-time currency conversion rates
- **Python**: Core programming language

## 📝 License

This project is licensed for fun purposes only. Not for commercial use.

## 🙏 Acknowledgements

- [ExchangeRate API](https://www.exchangerate-api.com/) for providing currency conversion data
- [Azure AI](https://azure.microsoft.com/en-us/services/cognitive-services/) for natural language processing
- [Streamlit](https://streamlit.io/) for the simple web app framework

---

Made with ❤️ for fun currency conversions
