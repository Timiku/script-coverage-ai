import os
import json
import openai
from colorama import Fore, Style

def generate_analysis(data, model):
    screenplay = json.dumps(data['metadata']) + '\n' + json.dumps(data['content'])
    prompt = f"You are a professional screenplay analyzer. Provide script notes for this screenplay:\n\n{screenplay}\n\nSummary:\n"
    response = openai.Completion.create(
        model_engine=model,
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.8,
    )
    
    # Extract the relevant information from the OpenAI response
    summary = response.choices[0].text
    audience = response.choices[1].text
    budget_level = response.choices[2].text
    viability = response.choices[3].text
    # Print the response for debug
    print(Fore.GREEN + response + Style.RESET_ALL)
    # Return the analysis results as a formatted string
    result = f"Summary: {summary}\n\nAudience: {audience}\n\nBudget Level: {budget_level}\n\nViability: {viability}"
    return result
    
def generate_analysis_35(data, model):
    sc_metadata = json.dumps(data['metadata'])
    sc_content = json.dumps(data['content'])
    screenplay = sc_metadata + '\n' + sc_content
    #debug
    print(f"{Fore.YELLOW}Sending the screenplay to OpenAI: {Fore.CYAN}{sc_metadata}{Style.RESET_ALL}")
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      max_tokens=512,
      n=1,
      stop=None,
      temperature=0.8,
      messages=[
            {"role": "system", "content": "You are a professional Screenplay analyzer, rating scripts if they are worth reading for busy producers. Be critical. Analyze User's screenplay and provide script coverage with the format:\n(TITLE) by (AUTHOR):\nRating:[Pass,Consider,Recommend](Pass=No,Consider=Maybe,Recommend=Greenlight)\nGenre:\nSetting:(locale or location)\nTime Period:\nBudget:(Low=Student or Indie,Medium=Studio,High=Blockbuster)\nLogline:\nSynopsis:\nAudience:\nComments:\n"},
            {"role": "user", "content": f"Screenplay:\n{screenplay}"},

        ]
    )
    # Print the response for debug
    print(Fore.GREEN + str(response) + Style.RESET_ALL)
    # Return the analysis results as a formatted string
    result = response['choices'][0]['message']['content']
    return result