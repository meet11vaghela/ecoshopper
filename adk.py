"""
ADK library wrapper for Google Gemini API and DuckDuckGo Search (ddgs).
"""
import os
import google.generativeai as genai
from ddgs import DDGS

class Agent:
    def __init__(self, model, system_prompt=None, tools=None):
        self.model_name = model
        self.system_prompt = system_prompt
        self.tools = tools or []
        
        # Configure Gemini
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_prompt
        )

    def generate_response(self, prompt):
        """
        Generates a response using the Gemini model.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

class Tool:
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func

def web_search(query):
    """
    Performs a web search using ddgs.
    """
    print(f"[ADK Search] Searching for: {query}")
    try:
        results = DDGS().text(query, max_results=5)
        formatted_results = []
        if results:
            for r in results:
                formatted_results.append(f"Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}")
            return "\n\n".join(formatted_results)
        return "No results found."
    except Exception as e:
        print(f"Search error: {e}")
        return f"Error performing search: {str(e)}"
