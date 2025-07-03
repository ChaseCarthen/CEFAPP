from langchain_community.utilities import SearxSearchWrapper
s = SearxSearchWrapper(searx_host="http://localhost:8080/search",     headers={"User-Agent": "Mozilla/5.0"},  params={"engines": "google", "format": "json"})
out = s.run("what are some example stock tickers? what is the GUT stock ticker?")

print(out)
