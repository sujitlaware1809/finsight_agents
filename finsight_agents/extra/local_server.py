from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FinSight AI Local Server", version="1.0.0")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# Simple FinSight AI Agent Implementation
class FinSightAIAgent:
    def __init__(self):
        self.name = "finsight-ai-local"
        self.description = "FinSight AI Financial Advisor - Local Development Server"
    
    def _extract_amount(self, message):
        """Extract monetary amount from message"""
        # Look for patterns like $300,000 or 300000 or 300k
        patterns = [
            r'\$?([\d,]+(?:\.\d{2})?)',  # $300,000 or 300,000
            r'(\d+)k',  # 300k
            r'(\d+)\s*thousand',  # 300 thousand
            r'(\d+)\s*million',  # 3 million
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, message.lower())
            if matches:
                amount_str = matches[0].replace(',', '')
                try:
                    amount = float(amount_str)
                    if 'k' in message.lower():
                        amount *= 1000
                    elif 'million' in message.lower():
                        amount *= 1000000
                    return amount
                except:
                    continue
        return None
    
    def _extract_age(self, message):
        """Extract age from message"""
        patterns = [
            r"i'm (\d+)",
            r"i am (\d+)",
            r"(\d+) years old",
            r"age (\d+)",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, message.lower())
            if matches:
                try:
                    return int(matches[0])
                except:
                    continue
        return None
    
    def _extract_income(self, message):
        """Extract income from message"""
        patterns = [
            r'earn \$?([\d,]+)',
            r'salary \$?([\d,]+)',
            r'income \$?([\d,]+)',
            r'make \$?([\d,]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, message.lower())
            if matches:
                try:
                    return float(matches[0].replace(',', ''))
                except:
                    continue
        return None
    
    def _extract_credit_score(self, message):
        """Extract credit score from message"""
        patterns = [
            r'credit score.*?(\d{3})',
            r'cibil.*?(\d{3})',
            r'score.*?(\d{3})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, message.lower())
            if matches:
                try:
                    score = int(matches[0])
                    if 300 <= score <= 850:  # Valid credit score range
                        return score
                except:
                    continue
        return None
    
    def _calculate_emi(self, principal, annual_rate, years):
        """Calculate EMI for given principal, rate and tenure"""
        monthly_rate = annual_rate / (12 * 100)
        months = years * 12
        if monthly_rate == 0:
            return principal / months
        
        emi = principal * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
        return emi
        
    def process_message(self, message):
        """Process user message and return financial advice"""
        msg_lower = message.lower()
        
        # Extract key financial details from message
        loan_amount = self._extract_amount(message)
        age = self._extract_age(message)
        income = self._extract_income(message)
        credit_score = self._extract_credit_score(message)
        
        # Greeting responses
        if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'greet', 'start', 'looking for', 'help me']):
            return f"""
🌟 **Welcome to FinSight AI Local Server!** 🌟

Your comprehensive financial advisor is running locally! I specialize in:

💰 **Loan Guidance** - Home, personal, education loans
📈 **Investment Planning** - Mutual funds, stocks, SIPs  
📋 **Tax Optimization** - Filing, deductions, planning
📊 **Credit Score Help** - Improve your CIBIL score
💹 **Budget Planning** - Smart money management
🛡️ **Scam Detection** - Protect your finances
🏛️ **Government Schemes** - Subsidies and benefits
💳 **Credit Card Advice** - Choose and use wisely

**Example queries:**
• "I need a home loan for $300,000"
• "How to invest $50,000 at age 30?"
• "Help me improve my 620 credit score"
• "Create a budget for $6,000 monthly income"

What financial guidance can I provide you today? 😊
"""

        # Loan-related queries
        elif any(word in msg_lower for word in ['loan', 'mortgage', 'borrow', 'lending', 'emi']):
            loan_type = "home" if "home" in msg_lower else "personal" if "personal" in msg_lower else "education" if "education" in msg_lower else "general"
            
            response = f"""
🏠 **FinSight AI - {loan_type.title()} Loan Advisory** 🏠

**Your Loan Request Analysis:**
"""
            
            if loan_amount:
                response += f"• **Requested Amount:** ${loan_amount:,}\n"
                if loan_amount >= 200000:
                    response += f"• **Assessment:** Large loan - excellent credit score (750+) recommended\n"
                elif loan_amount >= 50000:
                    response += f"• **Assessment:** Moderate loan - good credit score (700+) sufficient\n"
                else:
                    response += f"• **Assessment:** Small loan - fair credit score (650+) acceptable\n"
            
            response += f"""

**Current {loan_type.title()} Loan Rates & Options:**

**🏠 Home Loans:**
• Interest: 8.5% - 9.5% per annum
• Tenure: Up to 30 years
• Loan-to-Value: Up to 90%
• Processing fee: 0.5% - 1%

**👤 Personal Loans:**
• Interest: 11% - 24% per annum  
• Tenure: 1-7 years
• Amount: $50,000 - $500,000
• Quick approval (24-48 hours)

**🎓 Education Loans:**
• Interest: 9% - 15% per annum
• Tenure: Up to 15 years
• Collateral-free up to $75,000
• Moratorium during study period
"""

            if loan_amount:
                monthly_emi = self._calculate_emi(loan_amount, 8.5, 20) if loan_type == "home" else self._calculate_emi(loan_amount, 15, 5)
                response += f"""

**💰 EMI Calculation for ${loan_amount:,}:**
• Estimated Monthly EMI: ${monthly_emi:,.2f}
• Recommended Monthly Income: ${monthly_emi * 3:,.2f}+
"""

            response += """

**💡 Pro Tips for Better Approval:**
• Maintain credit score above 750
• Keep existing EMIs below 40% of income
• Have stable employment (2+ years)
• Apply to multiple lenders for best rates

**🎯 Next Steps:**
1. Calculate your EMI affordability
2. Compare rates from 3-4 lenders
3. Get pre-approved before finalizing
4. Negotiate processing fees
"""
            return response

        # Investment queries
        elif any(word in msg_lower for word in ['invest', 'investment', 'mutual fund', 'sip', 'stock', 'portfolio', 'wealth building']):
            investment_amount = loan_amount if loan_amount else 10000  # Default if no amount specified
            
            response = f"""
📈 **FinSight AI - Investment Strategy for ${investment_amount:,}** 📈

**Your Investment Profile Analysis:**
"""
            
            if age:
                if age < 30:
                    risk_profile = "Aggressive (80% Equity, 20% Debt)"
                    time_horizon = "30+ years for retirement"
                elif age < 40:
                    risk_profile = "Moderate-Aggressive (70% Equity, 30% Debt)"
                    time_horizon = "20+ years for retirement"
                elif age < 50:
                    risk_profile = "Moderate (60% Equity, 40% Debt)"
                    time_horizon = "15+ years for retirement"
                else:
                    risk_profile = "Conservative (40% Equity, 60% Debt)"
                    time_horizon = "10+ years for retirement"
                
                response += f"• **Age:** {age} years\n"
                response += f"• **Recommended Risk Profile:** {risk_profile}\n"
                response += f"• **Investment Horizon:** {time_horizon}\n"
            
            if investment_amount >= 100000:
                response += f"• **Investment Category:** High-value portfolio\n"
                response += f"• **Diversification:** 5-7 different funds recommended\n"
            elif investment_amount >= 25000:
                response += f"• **Investment Category:** Moderate portfolio\n"
                response += f"• **Diversification:** 3-4 different funds recommended\n"
            else:
                response += f"• **Investment Category:** Starter portfolio\n"
                response += f"• **Diversification:** 2-3 different funds recommended\n"

            response += f"""

**💰 Strategic Allocation for ${investment_amount:,}:**

**🏆 Recommended Fund Mix:**
"""

            if age and age < 35:
                response += f"""
• **Large Cap Funds:** ${int(investment_amount * 0.4):,} (40%) - Stable growth
• **Mid/Small Cap:** ${int(investment_amount * 0.3):,} (30%) - High growth potential  
• **International Funds:** ${int(investment_amount * 0.2):,} (20%) - Global exposure
• **Debt Funds:** ${int(investment_amount * 0.1):,} (10%) - Stability
"""
            else:
                response += f"""
• **Large Cap Funds:** ${int(investment_amount * 0.5):,} (50%) - Stable growth
• **Mid Cap Funds:** ${int(investment_amount * 0.2):,} (20%) - Moderate growth
• **Debt Funds:** ${int(investment_amount * 0.2):,} (20%) - Stability
• **ELSS (Tax Saving):** ${int(investment_amount * 0.1):,} (10%) - Tax benefits
"""

            monthly_sip = investment_amount / 12
            response += f"""

**📅 SIP Strategy:**
• **Monthly SIP Amount:** ${monthly_sip:,.2f}
• **Expected Annual Return:** 12-15%
• **10-Year Projected Value:** ${investment_amount * 3.2:,.2f}
• **20-Year Projected Value:** ${investment_amount * 9.6:,.2f}

**🚀 Investment Action Plan:**
1. **Emergency Fund First:** 6 months expenses
2. **Start SIP:** Automated monthly investments
3. **Step-up SIP:** Increase by 10% annually
4. **Stay Invested:** Don't panic in market dips
5. **Annual Review:** Rebalance portfolio
"""
            return response

        # Credit Score queries
        elif any(word in msg_lower for word in ['credit score', 'cibil', 'credit report', 'improve credit']):
            response = f"""
📊 **FinSight AI - Credit Score Improvement** 📊
"""

            if credit_score:
                if credit_score >= 750:
                    assessment = "Excellent! You're in the top tier."
                    action = "Maintain current habits and consider premium credit cards."
                elif credit_score >= 700:
                    assessment = "Good score! You qualify for most loans."
                    action = "Fine-tune to reach 750+ for best rates."
                elif credit_score >= 650:
                    assessment = "Fair score. Room for improvement."
                    action = "Focus on payment history and utilization."
                else:
                    assessment = "Needs significant improvement."
                    action = "Urgent attention required on all factors."
                
                response += f"""
**Your Credit Score Analysis:**
• **Current Score:** {credit_score}
• **Assessment:** {assessment}
• **Action Plan:** {action}
"""

            response += f"""

**🎯 Credit Score Ranges:**
• **750-850:** Excellent (Best rates & terms)
• **700-749:** Good (Favorable conditions)
• **650-699:** Fair (Average rates)
• **Below 650:** Poor (Limited options)

**⚡ Score Improvement Strategy:**

**Immediate Actions (0-30 days):**
✅ Pay all outstanding dues completely
✅ Keep credit utilization below 30%
✅ Set up auto-pay for all bills
✅ Check credit report for errors

**Short-term (1-3 months):**
✅ Pay more than minimum on credit cards
✅ Don't close old credit accounts
✅ Avoid new credit applications
✅ Maintain old accounts with small purchases

**Long-term (3+ months):**
✅ Build long credit history
✅ Diversify credit types (cards + loans)
✅ Keep utilization below 10%
✅ Regular monitoring & maintenance
"""

            if credit_score and credit_score < 700:
                months_to_improve = max(3, (750 - credit_score) // 20)
                response += f"""

**📈 Your Improvement Timeline:**
• **Target Score:** 750+
• **Estimated Time:** {months_to_improve} months
• **Monthly Progress:** +15-25 points (with consistent effort)
"""

            response += """

**🆓 Free Credit Monitoring:**
• Annual Credit Report (official site)
• Credit card issuer apps
• Banking apps with credit tracking

Start improving today for better financial opportunities!
"""
            return response

        # Budget Planning
        elif any(word in msg_lower for word in ['budget', 'save', 'savings', 'expense', 'planning', 'money management']):
            response = f"""
💹 **FinSight AI - Smart Budget Planning** 💹
"""

            if income:
                response += f"""
**Your Income Analysis:**
• **Monthly Income:** ${income:,}
• **Recommended Budget Breakdown:**
"""
                needs = income * 0.50
                wants = income * 0.30
                savings = income * 0.20
                
                response += f"""
  - **Needs (50%):** ${needs:,.2f}
  - **Wants (30%):** ${wants:,.2f}  
  - **Savings (20%):** ${savings:,.2f}
"""

            response += f"""

**🎯 The 50-30-20 Rule:**
• **50% Needs:** Rent, groceries, utilities, EMIs
• **30% Wants:** Entertainment, dining, shopping  
• **20% Savings:** Emergency fund + investments

**📊 Detailed Budget Categories:**

**Fixed Expenses (40-50%):**
• Rent/Home EMI: 25-30%
• Insurance premiums: 2-3%
• Phone, internet, utilities: 3-5%
• Transportation: 5-10%

**Variable Expenses (25-35%):**
• Groceries: 8-12%
• Dining out: 3-5%
• Entertainment: 3-5%
• Clothing: 2-3%
• Miscellaneous: 5-10%

**Savings & Investments (20-25%):**
• Emergency fund: 5-10%
• Mutual funds/SIP: 10-15%
• Tax-saving investments: 3-5%

**💰 Smart Saving Strategies:**

**Automated Savings:**
1. Auto-transfer on salary day
2. Separate accounts for different goals
3. Round-up savings apps

**Expense Reduction:**
• Cook more, eat out less
• Use public transport/carpooling
• Cancel unused subscriptions
• Buy generic brands
• Plan bulk purchases
"""

            if income:
                emergency_fund = income * 6
                response += f"""

**🎯 Your Financial Goals:**
• **Emergency Fund Target:** ${emergency_fund:,} (6 months expenses)
• **Monthly Investment:** ${savings:,.2f}
• **Annual Investment:** ${savings * 12:,.2f}
"""

            response += """

**📱 Budget Tracking Tools:**
• Mint, YNAB, Personal Capital
• Bank spending analytics
• Simple Excel/Google Sheets

Start budgeting today for financial freedom tomorrow!
"""
            return response

        # Default response for general queries
        else:
            return f"""
🤖 **FinSight AI - Local Server Response** 🤖

I noticed you asked: "{message}"

**I can help you with comprehensive financial advice:**

💰 **Loan Guidance:** "I need a home loan for $300,000"
📈 **Investment Planning:** "How to invest $50,000 at age 30"  
📋 **Tax Help:** "Tax filing help for freelancers"
📊 **Credit Score:** "Improve my 620 credit score"
💹 **Budget Planning:** "Create budget for $6000 income"
🛡️ **Scam Protection:** "Is this investment offer legitimate?"
🏛️ **Government Schemes:** "First-time home buyer programs"
💳 **Credit Cards:** "Best credit card for beginners"

**🔍 For Best Results, Include:**
- Specific amounts (e.g., "$50,000")
- Your age or income level
- Timeline or goals
- Current situation details

**📍 Local Server Status:** ✅ Running on http://localhost:8000

What specific financial topic would you like detailed guidance on? 💡
"""

# Initialize the agent
financial_agent = FinSightAIAgent()
logger.info(f"FinSight AI Local Agent initialized: {financial_agent.name}")

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "agent": financial_agent.name,
        "message": "FinSight AI Local Server is running!",
        "server_url": "http://localhost:8000"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Process the message through the agent
        response = financial_agent.process_message(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/agent-info")
def agent_info():
    return {
        "name": financial_agent.name,
        "description": financial_agent.description,
        "status": "active",
        "server_type": "local_development",
        "capabilities": [
            "Loan Guidance with EMI calculations",
            "Investment Planning with age-based strategies", 
            "Tax Assistance",
            "Credit Score Improvement with timelines",
            "Budget Planning with income analysis",
            "Scam Detection",
            "Government Schemes",
            "Credit Card Advice"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FinSight AI Local Server...")
    print("📍 Server URL: http://localhost:8000")
    print("📋 API Endpoints:")
    print("   - GET  /           - Health check")
    print("   - GET  /agent-info - Agent information")
    print("   - POST /chat       - Chat with agent")
    print("💡 Use this URL in your frontend to connect!")
    
    uvicorn.run("local_server:app", host="0.0.0.0", port=8000, reload=True)
