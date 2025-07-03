import yaml
import datetime
from fetch import fetch_historic_cef_price_nav, fetch_cef_dividends, evaluate_cefs
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json
from pydantic import BaseModel, Field

class CEFOutput(BaseModel):
    ticker: str = Field(..., description="The ticker symbol of the CEF")
    final_decision: str = Field(..., description="The final investment decision")
    rating: int = Field(..., ge=1, le=10, description="The rating of the CEF")
    reasoning: str = Field(..., description="The reasoning behind the investment decision")

def load_tickers(file_path):
    """
    Load tickers from a YAML file.
    
    Args:
        file_path (str): Path to the YAML file containing tickers.
        
    Returns:
        list: A list of tickers.
    """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data.get('tickers', [])

'''
{
  "ticker": "TICKER",
  "final_decision": "buy | hold | reject",
  "rating": 1–10,
  "reasoning": "Brief explanation of how the fund aligns or fails to align with Selengut's strategy"
}
'''
output_format = {
    "ticker": "<TICKER>",
    "final_decision": "buy | hold | reject",
    "rating": "<1–10>",
    "reasoning": "<Brief explanation of how the fund aligns or fails to align with Selengut's strategy>"
}

if __name__ == "__main__":
    
    llm = ChatOllama(
        model="llama3.2",
        temperature=0.1,
        max_tokens=20000,
    )
    llm = llm

    # Load the prompt for evaluating CEFs
    with open('prompt.md', 'r') as file:
        prompt = file.read()

    # Define the system prompt for langchain prompt template
    system_prompt_template = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "CEF JSON: {data}")
    ])
    llm = system_prompt_template | llm
    
    # Example usage
    tickers = load_tickers('tickers.yaml')
    print("Loaded tickers:", tickers)
    # You can now use the `tickers` list in your application
    # For example, you can pass it to the `evaluate_cefs` function from fetch
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        price_nav = fetch_historic_cef_price_nav(ticker)
        # fetch based on today and two years ago
        cef_dividends = fetch_cef_dividends(ticker, (datetime.datetime.now() - datetime.timedelta(days=730)).strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%Y-%m-%d"))
        #if price_nav:
        #    print(f"Price and NAV for {ticker}: {price_nav}")
        #else:
        #    print(f"No data found for {ticker}")
        

        recommendations = evaluate_cefs([ticker])

        context = {
            "ticker": ticker,
            "price_nav_date": price_nav,
            "cef_dividends": cef_dividends,
        }
        #model_prompt = system_prompt_template.invoke({'data': context})

        output = llm.invoke({'data': context})
        print(f"Model output for {ticker}:\n{output.content}")


        