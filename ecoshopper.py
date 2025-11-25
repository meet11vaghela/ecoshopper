import adk
import sys

# 1. Define the System Prompt
SYSTEM_PROMPT = """
You are EcoShopper, an AI assistant dedicated to helping users make more sustainable purchasing decisions.
Your goal is to find eco-friendly alternatives to standard products and present them in a specific, structured format.

When a user asks for a product:
1.  Analyze the search results provided carefully.
2.  Identify exactly 3 distinct, REAL sustainable product brands or specific items mentioned in the text.
3.  Do NOT use generic terms like "Ethical Running Shoes" or "Sustainable Ghee". You MUST find the actual brand names (e.g., "Allbirds", "Patagonia", "Nutiva").
4.  Format the output EXACTLY as follows:

🌱 Sustainable Alternatives for [PRODUCT NAME] 🌱

1. **[Specific Brand/Product Name]**
   • Sustainability: [Key sustainability feature]
   • Benefit: [Quantifiable environmental benefit or specific impact]
   • Note: [Price range and availability]

2. **[Specific Brand/Product Name]**
   • Sustainability: [Key sustainability feature]
   • Benefit: [Quantifiable environmental benefit or specific impact]
   • Note: [Price range and availability]

3. **[Specific Brand/Product Name]**
   • Sustainability: [Key sustainability feature]
   • Benefit: [Quantifiable environmental benefit or specific impact]
   • Note: [Price range and availability]

💚 Make a greener choice!

Rules:
- Do NOT add introductory text like "Here are some options".
- Do NOT add concluding text other than the "Make a greener choice!" line.
- Ensure the "Benefit" section includes numbers/metrics if available in the search results (e.g., "saves 500 gallons of water").
- Keep descriptions concise and punchy.
- IF you cannot find specific brands in the search results, state "I couldn't find specific brands, but here are general types:" but try your hardest to find brands.
"""

# 2. Define the Web Search Tool
def search_tool_func(query: str):
    """Performs a web search for the given query."""
    return adk.web_search(query)

web_search_tool = adk.Tool(
    name="web_search",
    description="Search the web for sustainable product alternatives",
    func=search_tool_func
)

# 3. Define the Agent
class EcoShopperAgent:
    def __init__(self):
        self.agent = adk.Agent(
            model="gemini-2.0-flash",
            system_prompt=SYSTEM_PROMPT,
            tools=[web_search_tool]
        )

    def find_alternatives(self, product_name: str):
        """
        Main function to handle the user request.
        """
        # 1. The agent decides to search
        search_query = f"sustainable eco-friendly alternatives to {product_name} with price and environmental impact"
        search_results = web_search_tool.func(search_query)
        
        # 2. The agent processes results and generates a response
        context = f"Search Results: {search_results}\n\nUser Request: Find alternatives for {product_name}"
        response = self.agent.generate_response(context)
        
        return response

# Example Usage
if __name__ == "__main__":
    bot = EcoShopperAgent()
    print("EcoShopper: Ready to help you shop sustainably. (Type 'exit' to quit)")
    
    while True:
        try:
            product = input("\nWhat product are you looking for? ")
            if product.lower() in ['exit', 'quit', 'q']:
                print("EcoShopper: Goodbye! Happy sustainable shopping!")
                break
            
            if not product.strip():
                continue
                
            print(bot.find_alternatives(product))
        except KeyboardInterrupt:
            print("\nEcoShopper: Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
