import re
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from readability import Document
from plugins.plugin_base import Plugin

class webPlugin(Plugin):
    def can_handle(self, message: str) -> bool:
        return "[SEARCH]" in message and "[/SEARCH]" in message

    def handle(self, message: str) -> list[str]:
        pattern = r"\[SEARCH\](.*?)\[/SEARCH\]"
        queries = re.findall(pattern, message, re.DOTALL)
        results = []

        for query in queries:
            query = query.strip()
            summaries = []

            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=2)

                for result in search_results:
                    url = result.get("href") or result.get("url")
                    if not url:
                        continue

                    try:
                        page = requests.get(url, timeout=10)
                        doc = Document(page.text)
                        html = doc.summary()
                        soup = BeautifulSoup(html, "html.parser")
                        text = soup.get_text()
                        cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
                        summary = f"🔗 {result['title']} ({url})\n{cleaned[:600]}...\n"
                        summaries.append(summary)

                    except Exception as e:
                        summaries.append(f"⚠️ Failed to fetch or parse {url}: {e}")

            results.append(f"Web search for: '{query}'\n\n" + "\n\n".join(summaries))
            

        return results
wp = weatherPlugin()
print(wp.handle("[SEARCH] what is the tallest building in the world?[/SEARCH]"))