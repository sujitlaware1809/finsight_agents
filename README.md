# 💰 finsightAI – Your Intelligent Financial Copilot

finsightAI is a modular, multi-agent financial assistant powered by Google's Agent Development Kit (ADK) and Gemini LLMs. It delivers tailored financial insights using real-time user context sourced via a secure FI MCP (Financial Information Multi-Context Platform) server.

---

## ✨ Features

- 🔍 Personalized financial advice backed by real-time financial context  
- 🧠 Modular multi-agent architecture using Google ADK  
- 🔗 FI MCP API integration to fetch net worth, transactions, EPF, MF, stock data, etc.  
- 🛠️ Built on Google’s Gemini ecosystem (ADK, Vertex AI)  
- 📈 Tools for credit, loans, taxes, investments, scam detection & more  
- 🚀 Designed for extensibility and easy tool addition  

---

## 🧠 Agent Capabilities

| Agent Name              | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `loan_helper`           | Recommends optimal loans based on credit and income                         |
| `gov_scheme_suggestor`  | Suggests relevant government schemes based on eligibility                   |
| `credit_card_provider`  | Matches users with suitable credit cards                                    |
| `credit_score_improver` | Provides actionable steps to improve credit score                           |
| `tax_filing_helper`     | Guides the user in tax filing and deduction planning                        |
| `investment_guide`      | Recommends investment strategies based on user goals                        |
| `stock_analyst`         | Analyzes stock transactions and suggests improvements                       |
| `budget_planner`        | Creates a personal budget plan using transaction patterns                   |
| `scam_detector`         | Flags suspicious transactions or patterns indicative of scams               |

All agents autonomously query the FI MCP server to retrieve real-time financial data before making decisions.

---

## 🧰 Google Tech Stack

This project leverages Google’s next-generation agent and AI ecosystem:

| Tool / API                      | Purpose                                                                                   |
|---------------------------------|-------------------------------------------------------------------------------------------|
| **Agent Development Kit (ADK)** | Agent orchestration, memory, tools, and execution pipelines                              |
| **Gemini API (via ADK)**        | LLM for reasoning, conversation, and tool execution                                       |
| **Vertex AI (Gemini Models)**   | Agent deployment and scaling on Google Cloud                                              |
| **Google Search Tool**          | Used within agent tools to perform real-time web lookups                                  |
| **Tool Calling Framework (ADK)**| Custom tools like `get_net_worth`, `get_transactions`, etc., built using ADK SDK         |
| **Web ADK Console**             | Used for testing, running, and debugging agent workflows                                  |

Additional tools:
- Python 3.10+  
- REST APIs for the FI MCP Server  
- Secure environment variables managed with `.env`

---

## 🔐 FI MCP Integration

A central feature of finsightAI is the ability to pull contextual financial data using the FI MCP server. Each agent checks the MCP before answering to ensure relevance.

Typical APIs used:

- `GET /net-worth`
- `GET /bank-transactions`
- `GET /epf-details`
- `GET /mf-transactions`
- `GET /stock-transactions`
- …and more

This enables highly contextual and personalized guidance.

---

## 🛠️ Project Structure

```plaintext
finsightAI/
│
├── sub_agents/                 # Modular subagents (loan, investment, scam detection, etc.)
│   ├── credit_card_provider/
│   ├── gov_scheme_suggestor/
│   └── ...
│
├── main.py                         # ADK root agent runner
├── requirements.txt                # Python dependencies
├── .env                            # Secrets/configs (ignored)
└── README.md


---

## ⚙️ Setup Instructions

Follow these steps to get finsightAI up and running locally:

### 1. Clone the Repository

```bash
git clone https://github.com/divyansh-tripathi7/finsightAI.git
cd finsightAI

```

### 2. Create and Activate a Virtual Environment
```bash

python3 -m venv venv
source venv/bin/activate  # for macOS/Linux



# For Windows:
# venv\Scripts\activate

```
### 3. Install Required Dependencies
```bash

pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a .env file in the root directory and fill it with the required keys (you can refer to .env.example if provided):

```bash

cp .env.example .env
Edit the .env file and add:

GOOGLE_API_KEY=your_google_api_key
PROJECT_ID=your_vertex_project_id
MCP_API_KEY=your_mcp_key
ADK_LOG_LEVEL=DEBUG
(Optional) Add your Gemini model config if needed.

```

### 5. Launch the Agent Using Google ADK
Make sure you have the Google Agent Development Kit installed:

```bash

pip install google-generativeai
pip install --upgrade google-generativeai[adk]
Run the local web interface:


adk web

```
The ADK interface will launch at http://localhost:8080



