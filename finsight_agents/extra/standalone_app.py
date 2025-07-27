from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FinSight AI Agent", version="1.0.0")

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# Simple FinSight AI Agent Implementation
class FinSightAIAgent:
    def __init__(self):
        self.name = "finsight-ai-agent"
        self.description = "FinSight AI Financial Advisor - Cloud Ready Version"
    
    def _extract_amount(self, message):
        """Extract monetary amount from message"""
        import re
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
        import re
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
        import re
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
        import re
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
🌟 **Welcome to FinSight AI!** 🌟

Your comprehensive financial advisor is here to help! I specialize in:

💰 **Loan Guidance** - Home, personal, education loans
📈 **Investment Planning** - Mutual funds, stocks, SIPs  
📋 **Tax Optimization** - Filing, deductions, planning
📊 **Credit Score Help** - Improve your CIBIL score
💹 **Budget Planning** - Smart money management
🛡️ **Scam Detection** - Protect your finances
🏛️ **Government Schemes** - Subsidies and benefits
💳 **Credit Card Advice** - Choose and use wisely

**Just ask me anything like:**
• "I need a home loan for ₹50 lakhs"
• "How to invest ₹10,000 monthly?"
• "Help me improve my credit score"
• "Create a budget for ₹80,000 salary"

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
• Amount: ₹50,000 - ₹50 lakhs
• Quick approval (24-48 hours)

**🎓 Education Loans:**
• Interest: 9% - 15% per annum
• Tenure: Up to 15 years
• Collateral-free up to ₹7.5 lakhs
• Moratorium during study period

**📋 Required Documents:**
✅ Income proof (3 months salary slips)
✅ Bank statements (6 months)
✅ PAN card, Aadhaar card
✅ Property documents (for home loans)
✅ ITR for last 2 years
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

Need specific loan amount calculation or eligibility check?
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

**� SIP Strategy:**
• **Monthly SIP Amount:** ${monthly_sip:,.2f}
• **Expected Annual Return:** 12-15%
• **10-Year Projected Value:** ${investment_amount * 3.2:,.2f}
• **20-Year Projected Value:** ${investment_amount * 9.6:,.2f}

**🚀 Start Your Investment Journey:**
1. **Emergency Fund First:** 6 months expenses
2. **Start SIP:** Automated monthly investments
3. **Step-up SIP:** Increase by 10% annually
4. **Stay Invested:** Don't panic in market dips
5. **Annual Review:** Rebalance if needed

**📱 Recommended Platforms:**
• Zerodha Coin, Groww, Paytm Money
• Choose direct plans (lower fees)
• Set up auto-debit for SIPs

Ready to start your wealth-building journey?
"""
            return response

        # Tax queries
        elif any(word in msg_lower for word in ['tax', 'itr', 'filing', 'deduction', '80c', 'income tax']):
            return """
📋 **FinSight AI - Tax Planning** 📋

**🎯 Key Tax Saving Sections:**

**Section 80C (₹1.5 Lakh limit):**
• PPF, EPF contributions
• ELSS mutual funds
• Life insurance premiums
• Principal repayment of home loan
• NSC, tax-saving FDs

**Section 80D (Medical Insurance):**
• Self & family: ₹25,000
• Parents: ₹25,000 additional
• Senior citizens: ₹50,000

**Section 24 (Home Loan Interest):**
• Self-occupied: ₹2 lakh limit
• Rented property: No limit

**📝 ITR Filing Deadlines:**
• Salaried: July 31st
• Business: October 31st
• Revised return: December 31st

**💡 Smart Tax Planning Tips:**

**For Salaried Employees:**
1. Maximize 80C investments early
2. Claim HRA if paying rent
3. Submit investment proofs to employer
4. Plan medical expenses strategically

**For Freelancers/Business:**
1. Maintain proper expense records
2. Claim home office expenses
3. Professional fees & equipment costs
4. Consider presumptive taxation if eligible

**🚨 Common Mistakes to Avoid:**
❌ Last-minute tax saving investments
❌ Not maintaining expense receipts
❌ Missing ITR filing deadline
❌ Not claiming all eligible deductions

**📊 Tax Calculation Example:**
Income ₹10 lakhs → Tax ₹1.17 lakhs
With 80C + 80D savings → Tax ₹70,000
**Savings: ₹47,000!**

Need help with specific deductions or ITR filing?
"""

        # Credit score queries
        elif any(word in msg_lower for word in ['credit score', 'cibil', 'credit report', 'improve credit']):
            return """
📊 **FinSight AI - Credit Score Mastery** 📊

**🎯 Credit Score Ranges:**
• **750-900:** Excellent (Best rates)
• **700-749:** Good (Favorable terms)
• **650-699:** Fair (Average rates)
• **Below 650:** Poor (Limited options)

**⚡ Quick Score Boosters:**

**Immediate Actions (0-30 days):**
✅ Pay all outstanding dues completely
✅ Keep credit utilization below 30%
✅ Set up auto-pay for all bills
✅ Check credit report for errors

**Short-term (1-3 months):**
✅ Pay more than minimum on credit cards
✅ Don't close old credit cards
✅ Avoid new credit applications
✅ Maintain old accounts with small purchases

**Long-term (3+ months):**
✅ Build long credit history
✅ Diversify credit types (cards + loans)
✅ Keep utilization below 10%
✅ Regular monitoring & maintenance

**🚫 Score Killers to Avoid:**
❌ Late payments (biggest impact)
❌ High credit utilization (>50%)
❌ Too many credit inquiries
❌ Defaulting on any payment
❌ Closing old credit accounts

**📈 Score Improvement Timeline:**
• **Month 1:** Clear all dues, errors
• **Month 2:** Optimize utilization
• **Month 3:** Consistent good behavior
• **Month 6:** Significant improvement visible

**🆓 Free Credit Report Sources:**
• CIBIL.com (1 free per year)
• Paisabazaar, BankBazaar
• Credit card issuer apps

**💳 Credit Building Strategy:**
1. Start with secured credit card if needed
2. Use card for small purchases monthly
3. Pay full amount before due date
4. Gradually build credit limit
5. Add co-applicant if score is very low

Current score range? I can give personalized advice!
"""

        # Budget planning queries
        elif any(word in msg_lower for word in ['budget', 'save', 'savings', 'expense', 'planning', 'money management']):
            return """
💹 **FinSight AI - Smart Budget Planning** 💹

**🎯 The 50-30-20 Rule:**
• **50% Needs:** Rent, groceries, utilities, EMIs
• **30% Wants:** Entertainment, dining, shopping  
• **20% Savings:** Emergency fund + investments

**📊 Detailed Budget Breakdown:**

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
• PPF/ELSS: 3-5%

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

**📱 Budget Tracking Tools:**
• ET Money, Walnut, Money Lover
• Bank spending analytics
• Simple Excel/Google Sheets

**🎯 Emergency Fund Goal:**
Build 6-12 months of expenses as priority
Example: Monthly expenses ₹50,000 → Emergency fund ₹3-6 lakhs

**📈 Budget Example (₹1 Lakh salary):**
• Needs: ₹50,000
• Wants: ₹30,000  
• Savings: ₹20,000
• Emergency fund: ₹10,000
• Investments: ₹10,000

What's your monthly income? I'll create a personalized budget!
"""

        # Government schemes
        elif any(word in msg_lower for word in ['government scheme', 'subsidy', 'pmay', 'mudra', 'startup india']):
            return """
🏛️ **FinSight AI - Government Schemes** 🏛️

**🏠 Housing Schemes:**

**PMAY (Pradhan Mantri Awas Yojana):**
• Interest subsidy up to ₹2.67 lakhs
• Income limit: ₹6-18 lakhs annually
• Loan amount: Up to ₹65 lakhs
• Apply through banks/PMAY portal

**💼 Business/Startup Schemes:**

**MUDRA Loans:**
• **Shishu:** Up to ₹50,000
• **Kishore:** ₹50,000 - ₹5 lakhs  
• **Tarun:** ₹5 - ₹10 lakhs
• No collateral required

**Startup India:**
• Tax exemption for 3 years
• Fast-track patent examination
• Self-certification compliance
• Government tender benefits

**👥 Social Security:**

**Atal Pension Yojana (APY):**
• Monthly pension ₹1,000-5,000
• Government co-contribution
• Entry age: 18-40 years

**PMJJBY & PMSBY:**
• Life insurance: ₹2 lakhs for ₹330/year
• Accident insurance: ₹2 lakhs for ₹20/year

**👩 Women-Specific Schemes:**

**Sukanya Samriddhi Yojana:**
• Girl child savings scheme
• Interest rate: ~7.6%
• Tax benefits under 80C
• Maturity: 21 years

**Stand-up India:**
• Bank loans ₹10 lakh - ₹1 crore
• For SC/ST/Women entrepreneurs
• Handholding support included

**📚 Education Schemes:**
• Interest subsidy on education loans
• Merit scholarships
• Skill development programs

**✅ How to Apply:**
1. Visit official government portals
2. Check eligibility criteria carefully
3. Prepare required documents
4. Apply online or through banks
5. Track application status regularly

**🚨 Avoid Middlemen:**
Always apply directly through official channels!

Which specific scheme interests you most?
"""

        # Scam detection
        elif any(word in msg_lower for word in ['scam', 'fraud', 'suspicious', 'lottery', 'prize', 'fake']):
            return """
🛡️ **FinSight AI - Scam Alert & Protection** 🛡️

**🚨 Top Financial Scams to Watch Out For:**

**📞 Phone/SMS Scams:**
❌ "Congratulations! You've won ₹25 lakhs"
❌ "Your account will be blocked, share OTP"
❌ "KYC update required immediately"
❌ "Get loan instantly, pay processing fee"

**💳 Banking Frauds:**
❌ Fake bank websites/apps
❌ Phishing emails requesting login details
❌ UPI payment reversals scam
❌ ATM skimming devices

**📈 Investment Scams:**
❌ "Guaranteed 50% returns in 6 months"
❌ Ponzi schemes (early investors paid from new money)
❌ Fake cryptocurrency platforms
❌ Binary trading scams

**🚩 Universal Red Flags:**
• Unsolicited calls/messages
• Pressure to act immediately  
• "Too good to be true" offers
• Requests for upfront payments
• Asking for OTP/PIN/passwords
• Poor grammar in communications

**✅ Protection Strategies:**

**Never Share:**
• OTP, PIN, CVV numbers
• Net banking credentials  
• Credit/debit card details
• Aadhaar/PAN numbers over phone

**Always Verify:**
• Call bank's official number independently
• Check company registration online
• Consult family/friends before investing
• Research investment schemes thoroughly

**📱 Safety Checklist:**
✅ Use official apps only
✅ Enable 2-factor authentication
✅ Regular account monitoring
✅ Set transaction limits
✅ Keep software updated

**🆘 If You're Scammed:**
1. **Immediately:** Block cards, change passwords
2. **Report:** Police, bank, cybercrime.gov.in
3. **Document:** Save all communications
4. **Follow-up:** Track complaint status

**📞 Emergency Numbers:**
• Cyber Crime: 1930
• Banking Ombudsman: 14448
• National Helpline: 155260

**💡 Remember:** 
Legitimate institutions NEVER ask for sensitive info over phone/email!

Describe any suspicious activity you've encountered for specific advice.
"""

        # Credit card queries  
        elif any(word in msg_lower for word in ['credit card', 'card', 'cashback', 'rewards']):
            return """
💳 **FinSight AI - Credit Card Mastery** 💳

**🏆 Best Credit Cards by Category:**

**💰 Cashback Cards:**
• **HDFC MoneyBack:** 5% cashback online
• **SBI SimplyCLICK:** 10X rewards online
• **ICICI Amazon Pay:** Unlimited 1% cashback

**✈️ Travel Cards:**
• **Axis Magnus:** 12 reward points per ₹200
• **HDFC Diners Black:** Airport lounge access
• **Amex Gold:** 4X points on dining

**⛽ Fuel Cards:**
• **HDFC IOCL:** 5% cashback on fuel
• **SBI BPCL:** 13X reward points

**🛍️ Lifestyle Cards:**
• **HDFC Regalia:** Premium dining benefits
• **ICICI Coral:** Movies & dining rewards

**📊 Card Selection Criteria:**

**For Beginners:**
• Annual fee: ₹0-500
• Easy approval (salary ₹25,000+)
• Basic rewards (1-2%)
• Simple terms & conditions

**For Experienced Users:**
• Higher reward rates (5-10%)
• Premium benefits (lounge, insurance)
• Annual fee justified by benefits

**💡 Smart Usage Tips:**

**Maximize Rewards:**
✅ Use right card for right category
✅ Pay bills to earn rewards
✅ Time purchases for bonus offers
✅ Redeem rewards regularly

**Avoid Pitfalls:**
❌ Cash advances (high interest)
❌ Only minimum payments
❌ Overspending for rewards
❌ Missing due dates

**📱 Application Process:**
1. Check eligibility online
2. Compare offers across banks
3. Apply for pre-approved cards first
4. Submit income documents
5. Wait for approval (3-7 days)

**🎯 Monthly Management:**
• Set spending alerts
• Pay full amount by due date
• Review statements for errors
• Keep utilization below 30%

**💳 Ideal Card Portfolio:**
• 1 Cashback card for daily spending
• 1 Travel card for booking trips
• 1 Fuel card if you drive regularly

What's your primary use case and monthly spending pattern?
"""

        # Default response for other queries
        else:
            return f"""
🤖 **FinSight AI - Financial Guidance** 🤖

I understand you're asking about: "{message}"

I'm here to help with comprehensive financial advice! Let me guide you to the right information:

**🎯 I can help you with:**

💰 **Loan Guidance:** "I need a home loan" or "personal loan advice"
📈 **Investment Planning:** "How to invest money" or "mutual fund advice"  
📋 **Tax Help:** "Tax filing help" or "tax saving tips"
📊 **Credit Score:** "Improve credit score" or "CIBIL score help"
💹 **Budget Planning:** "Create a budget" or "saving money tips"
🛡️ **Scam Protection:** "Is this a scam?" or "fraud detection"
🏛️ **Government Schemes:** "PMAY scheme" or "government subsidies"
💳 **Credit Cards:** "Best credit card" or "card recommendations"

**📝 Try asking:**
• "I want to buy a house, help with home loan"
• "Best way to invest ₹50,000?"
• "How to save tax this year?"
• "My credit score is 650, how to improve?"

**🎯 For Best Results:**
Include specific details like:
- Your income range
- Investment amount  
- Specific goals
- Timeline

What specific financial topic would you like detailed guidance on? 💡
"""

# Initialize the agent
financial_agent = FinSightAIAgent()
logger.info(f"FinSight AI Agent initialized: {financial_agent.name}")

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "agent": financial_agent.name,
        "message": "FinSight AI Agent is running successfully!"
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
        "capabilities": [
            "Loan Guidance",
            "Investment Planning", 
            "Tax Assistance",
            "Credit Score Help",
            "Budget Planning",
            "Scam Detection",
            "Government Schemes",
            "Credit Card Advice"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("standalone_app:app", host="0.0.0.0", port=port)
