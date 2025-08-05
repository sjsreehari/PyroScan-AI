from ddgs import DDGS



def go_websearch(location: str):
    
    query = f"Can you provide an analysis of past fire incidents in {location}?"
    
    print(f"[~] Performing web search for: {query}")

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=10)
            
            
        if not results or not isinstance(results, list):
            print("[!] No search results found.")
            return "No relevant data found."
        
        
        summaries = []
        
        
        for result in results:
            title = result.get("title", "")
            snippet = result.get("body", "")
            url = result.get("href", "")
            print(f"- {title}: {url}\n  {snippet}")
            
            
            if snippet:
                summaries.append(snippet.lower())
                
                
        if not summaries:
            return "No relevant data found."
        
        combined_text = " ".join(summaries)
        
        
        if "no fire" in combined_text or "no active" in combined_text:
            return "No active forest fire incidents reported near this location."
        elif "wildfire" in combined_text or "fire incident" in combined_text or "burning" in combined_text:
            return "Possible active wildfire or recent incident reported near this location."
        else:
            return "Could not conclusively determine fire status from web search."
        
        
    except Exception as e:
        return f"Error during web search: {str(e)}"