#############################################################################
#                      AI-Friend | Ai-powered health &                      #
#                          emotional support chatbot                        #
#                                                                           #
#                                                                           #             
#                                                                           #
#                    ------For Research Purpose------                       #
#############################################################################



def get_cdc_answer(question, api_key):
    url = "https://api.cdc.gov/api/v2/COVID-19/answers"
    params = {
        "q": question,
        "limit": 1,
        "sort": "relevance",
        "api_key": api_key  # Some APIs use "key" or "apikey" instead
    }
    response = requests.get(url, params=params).json()
    return response['data'][0]['answer'] if response.get('data') else "See CDC guidelines at www.cdc.gov"

# Usage
api_key = "wth4RWucjpkZwqydC3UOWUPYe2ql9nOkQFgwgUkO"
print(get_cdc_answer("How to treat mild fever?", api_key))



import requests

def get_cdc_answer(question, api_key="DEMO_KEY"):  # Replace DEMO_KEY with yours
    url = "https://api.cdc.gov/api/v2/resources/answers"
    headers = {
        "Authorization": f"Bearer {api_key}",  # API key in header
        "Content-Type": "application/json"
    }
    params = {
        "q": question,
        "limit": 1,
        "sort": "relevance"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise HTTP errors
        data = response.json()
        
        if data.get('data'):
            return data['data'][0]['answer']
        return "See CDC guidelines at www.cdc.gov"
    
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return "Couldn't access CDC resources. Please try again later."

# Usage
api_key = "wth4RWucjpkZwqydC3UOWUPYe2ql9nOkQFgwgUkO"
print(get_cdc_answer("How to treat mild fever?", api_key))