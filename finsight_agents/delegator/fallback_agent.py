"""
Minimal FinSight AI agent for cloud deployment
This version works without external dependencies on sub-agents
"""

class SimpleFinSightAgent:
    def __init__(self):
        self.name = "finsight-ai-simple"
        self.description = "FinSight AI Financial Advisor - Simplified cloud version"
        
    def run(self, message):
        """
        Process user message and return financial advice
        """
        # Convert message to lowercase for easier processing
        msg_lower = message.lower()
        
        # Greeting responses
        if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'greet']):
            return """
Hello! Welcome to FinSight AI! 👋

I'm your comprehensive financial advisor, here to help you with:
• 💰 Loan guidance (personal, home, education loans)
• 💳 Credit card recommendations and advice
• 📈 Investment strategies and portfolio planning
• 🏛️ Government financial schemes and subsidies
• 📊 Credit score improvement strategies
• 📋 Tax filing assistance and optimization
• 🛡️ Scam detection and financial security
• 💹 Budget planning and expense tracking

What specific financial topic would you like help with today?
"""

        # Loan-related queries
        if any(word in msg_lower for word in ['loan', 'mortgage', 'borrow', 'lending']):
            return """
🏠 **Loan Guidance - FinSight AI**

For your loan inquiry, here's comprehensive guidance:

**Types of Loans Available:**
• **Home Loans**: 6.5-9% interest, up to 30 years tenure
• **Personal Loans**: 10-24% interest, up to 7 years tenure  
• **Education Loans**: 8-15% interest, up to 15 years tenure
• **Car Loans**: 7-12% interest, up to 7 years tenure

**Key Documents Required:**
✓ Income proof (salary slips, ITR)
✓ Identity & address proof
✓ Bank statements (6 months)
✓ Property documents (for home loans)

**Tips for Better Approval:**
• Maintain credit score above 750
• Keep debt-to-income ratio below 40%
• Have stable employment history
• Compare rates from multiple lenders

**Next Steps:**
1. Check your credit score
2. Calculate EMI affordability
3. Compare offers from 3-4 banks
4. Get pre-approval before house hunting

Would you like specific advice for any particular type of loan?
"""

        # Investment-related queries
        if any(word in msg_lower for word in ['invest', 'investment', 'portfolio', 'mutual fund', 'stock', 'sip']):
            return """
📈 **Investment Guidance - FinSight AI**

Smart investment strategy based on your query:

**Investment Options by Risk Level:**

**Low Risk (6-8% returns):**
• Fixed Deposits & PPF
• Government bonds
• Conservative mutual funds

**Medium Risk (8-12% returns):**
• Balanced mutual funds
• Index funds
• Corporate bonds

**High Risk (12%+ potential):**
• Equity mutual funds
• Direct stocks
• ELSS funds

**Age-Based Strategy:**
• **20s-30s**: 70% equity, 30% debt
• **40s**: 60% equity, 40% debt  
• **50s+**: 40% equity, 60% debt

**Investment Principles:**
✓ Start early, invest regularly
✓ Diversify across asset classes
✓ Review portfolio annually
✓ Don't panic during market volatility

**Recommended Action Plan:**
1. Start SIP with ₹5,000-10,000/month
2. Choose 2-3 good mutual funds
3. Increase investment by 10% annually
4. Keep 6-month emergency fund separate

What's your age and investment amount you're considering?
"""

        # Tax-related queries
        if any(word in msg_lower for word in ['tax', 'filing', 'itr', 'deduction', '80c']):
            return """
📋 **Tax Filing Assistance - FinSight AI**

Tax optimization guidance for you:

**Key Tax-Saving Sections:**
• **80C**: ₹1.5L limit (PPF, ELSS, life insurance)
• **80D**: Medical insurance premiums
• **24B**: Home loan interest (up to ₹2L)
• **80E**: Education loan interest

**Important Deductions for Salaried:**
✓ Standard deduction: ₹50,000
✓ HRA exemption (if applicable)
✓ Professional tax
✓ Transport allowance

**For Freelancers/Business:**
✓ Office rent & utilities
✓ Equipment & software
✓ Professional fees
✓ Travel expenses

**Tax Filing Deadlines:**
• ITR filing: July 31st
• Advance tax: Quarterly
• TDS certificates: Check Form 16

**Smart Tax Planning Tips:**
1. Invest in ELSS early in the year
2. Keep all receipts organized
3. Plan medical expenses in one year
4. Consider NPS for additional 50K deduction

**Required Documents:**
• Form 16/16A, bank statements
• Investment proofs, rent receipts
• Medical bills, donation receipts

Need help with specific tax situation or deductions?
"""

        # Credit score related queries
        if any(word in msg_lower for word in ['credit score', 'cibil', 'credit report', 'improve credit']):
            return """
📊 **Credit Score Improvement - FinSight AI**

Your guide to building excellent credit:

**Current Credit Score Ranges:**
• 750-900: Excellent (best loan rates)
• 700-749: Good (favorable terms)
• 650-699: Fair (higher interest)
• Below 650: Poor (limited options)

**Quick Score Improvement Actions:**
✓ Pay all EMIs/credit cards on time
✓ Keep credit utilization below 30%
✓ Don't close old credit cards
✓ Avoid multiple loan inquiries
✓ Check report for errors monthly

**30-60-90 Day Plan:**

**Month 1:**
• Get free credit report
• Pay all outstanding dues
• Set up auto-pay for bills

**Month 2:**
• Reduce credit card usage
• Pay more than minimum amount
• Dispute any errors found

**Month 3:**
• Continue timely payments
• Consider credit limit increase
• Monitor score improvement

**Long-term Strategy:**
• Maintain 2-3 credit cards
• Keep accounts active with small purchases
• Aim for credit history of 3+ years
• Never use more than 30% of credit limit

**Free Credit Report Sources:**
• CIBIL, Experian, Equifax, CRIF

Current score range you're working with? I can provide specific guidance!
"""

        # Budget and planning queries
        if any(word in msg_lower for word in ['budget', 'save', 'savings', 'expense', 'planning']):
            return """
💹 **Budget Planning - FinSight AI**

Smart budgeting strategy for financial success:

**50-30-20 Rule Breakdown:**
• 50% - Needs (rent, food, utilities)
• 30% - Wants (entertainment, dining)
• 20% - Savings & investments

**Monthly Budget Categories:**

**Fixed Expenses:**
• Rent/EMI, insurance premiums
• Utilities, subscriptions
• Loan payments

**Variable Expenses:**
• Groceries, transportation
• Entertainment, shopping
• Medical, miscellaneous

**Savings Goals:**
• Emergency fund (6 months expenses)
• Short-term goals (1-3 years)
• Long-term investments (retirement)

**Smart Saving Tips:**
✓ Automate savings on salary day
✓ Use separate accounts for goals
✓ Track expenses with apps
✓ Review and adjust monthly

**Budget Planning Steps:**
1. Calculate total monthly income
2. List all fixed expenses
3. Track variable expenses for a month
4. Set realistic savings targets
5. Monitor and adjust regularly

**Emergency Fund Priority:**
Build ₹50,000-100,000 emergency fund before aggressive investing.

What's your monthly income range? I can help create a personalized budget!
"""

        # Scam detection queries
        if any(word in msg_lower for word in ['scam', 'fraud', 'suspicious', 'lottery', 'prize']):
            return """
🛡️ **Scam Detection Alert - FinSight AI**

**🚨 Common Financial Scams to Avoid:**

**Lottery/Prize Scams:**
❌ "You've won a lottery you never entered"
❌ "Pay fees to claim your prize"
❌ Asking for bank details/OTP

**Loan Scams:**
❌ "Guaranteed loan approval"
❌ "Pay processing fee first"
❌ No proper documentation

**Investment Scams:**
❌ "Get rich quick" schemes
❌ Guaranteed high returns (>15%)
❌ Pressure to invest immediately

**Banking Scams:**
❌ Fake bank calls asking for OTP
❌ Suspicious links via SMS
❌ Requests to update KYC urgently

**Red Flags to Watch:**
🚩 Unsolicited calls/messages
🚩 Requests for upfront payment
🚩 Pressure tactics
🚩 Too good to be true returns
🚩 Poor grammar/unprofessional communication

**Safety Guidelines:**
✅ Never share OTP/PIN with anyone
✅ Verify caller identity independently
✅ Check company credentials online
✅ Consult family/friends before big decisions
✅ Report scams to cybercrime.gov.in

**If You Suspect a Scam:**
1. Don't provide any information
2. Hang up/ignore immediately
3. Block the number
4. Report to authorities
5. Warn friends and family

Stay safe! When in doubt, always verify independently.
"""

        # Government schemes queries
        if any(word in msg_lower for word in ['government scheme', 'subsidy', 'pmay', 'mudra', 'startup']):
            return """
🏛️ **Government Financial Schemes - FinSight AI**

Popular schemes you might be eligible for:

**Housing Schemes:**
• **PMAY**: Subsidized home loans
• **CLSS**: Interest subsidy up to ₹2.67L
• Eligibility: Annual income up to ₹18L

**Business/Startup:**
• **MUDRA Loan**: Up to ₹10L for small business
• **Startup India**: Tax benefits, easier compliance
• **Stand-up India**: SC/ST/Women entrepreneurs

**Social Security:**
• **APY**: Pension scheme with government co-contribution
• **PMJJBY**: Life insurance for ₹330/year
• **PMSBY**: Accident insurance for ₹20/year

**Education:**
• **Education loans**: Government backing
• **Scholarships**: Merit and need-based
• **Skill development**: Free training programs

**Women-Specific:**
• **Mahila Udyam Nidhi**: Business loans
• **Sukanya Samriddhi**: Girl child savings
• **Women entrepreneur schemes**

**Application Process:**
1. Check eligibility online
2. Gather required documents
3. Apply through official portals
4. Follow up regularly
5. Avoid middlemen/agents

**Official Portals:**
• india.gov.in
• janaushadhi.gov.in
• pmay-urban.gov.in

Which specific scheme interests you most?
"""

        # Credit card queries
        if any(word in msg_lower for word in ['credit card', 'card', 'cashback', 'rewards']):
            return """
💳 **Credit Card Guidance - FinSight AI**

Smart credit card selection advice:

**Best Cards by Category:**

**For Beginners:**
• HDFC MoneyBack (5% cashback)
• SBI SimplyCLICK (5% online shopping)
• ICICI Amazon Pay (unlimited cashback)

**For Travel:**
• Axis Magnus (travel rewards)
• HDFC Diners Black (airport lounge)
• American Express Gold (reward points)

**For Fuel:**
• HDFC IOCL (fuel surcharge waiver)
• SBI BPCL (accelerated rewards)

**Premium Cards:**
• HDFC Infinia (luxury benefits)
• AMEX Platinum (comprehensive coverage)

**Key Features to Compare:**
✓ Annual fee vs. benefits
✓ Reward rate (1-5% typical)
✓ Welcome bonus
✓ Lounge access
✓ Insurance coverage

**Smart Usage Tips:**
• Pay full amount by due date
• Keep utilization below 30%
• Use for planned purchases only
• Set up auto-pay
• Review statements monthly

**Application Requirements:**
• Minimum salary: ₹25,000-50,000
• Credit score: 700+
• 6-month bank statements
• Income proof

**Red Flags to Avoid:**
❌ Too many cards
❌ Cash advances
❌ Minimum payment trap
❌ Overspending for rewards

What's your monthly income and primary use case for the card?
"""

        # General financial advice
        else:
            return """
💰 **FinSight AI - Your Financial Guide**

I can help you with comprehensive financial guidance in these areas:

**🏠 Loans & Mortgages**
Get advice on home loans, personal loans, education loans, and loan comparisons.

**📈 Investment Planning**  
Learn about mutual funds, stocks, SIPs, and building a diversified portfolio.

**📋 Tax Planning**
Maximize deductions, understand ITR filing, and optimize your tax liability.

**📊 Credit Score**
Improve your CIBIL score and access better loan terms.

**💹 Budget Planning**
Create effective budgets, build emergency funds, and track expenses.

**🛡️ Scam Protection**
Identify and avoid financial frauds and suspicious schemes.

**🏛️ Government Schemes**
Explore subsidies, loans, and benefits you're eligible for.

**💳 Credit Cards**
Choose the right cards and use them smartly for maximum benefits.

**How to Get Specific Help:**
Simply ask me about any financial topic like:
• "I need a home loan"
• "How to invest ₹50,000?"
• "Help with tax filing"
• "Improve my credit score"

What specific financial guidance do you need today? 🤔
"""

# Create the simple agent instance
root_agent = SimpleFinSightAgent()
