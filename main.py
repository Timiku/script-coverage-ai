import os
import json
import shutil
import io
import gradio as gr
import openai
from colorama import Fore, Style
from convert_to_json import pdf_to_json, fountain_to_json, txt_to_json
from openai_analysis import generate_analysis, generate_analysis_35

cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# Check if the config file exists and load the API key from it
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    api_key = config.get('api_key')
else:
    api_key = ''

# Create the "cache" directory if it doesn't exist
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
    
def analyze_callback(file, model, api_key):
    save_api_key(api_key)
    if file is None:
        return "Please upload a file first"
    return analyze_screenplay(file, model, api_key)
    
def save_api_key(api_key):
    with open(config_file, 'w') as f:
        json.dump({'api_key': str(api_key)}, f)

def analyze_screenplay(file, model, api_key):
    if not api_key:
        raise ValueError("OpenAI API key is required")
    openai.api_key = api_key
            
    # Check if the uploaded file is a supported format
    json_file = os.path.join(cache_dir, 'tmp_screenplay.json')

    if file.name.endswith('.pdf'):
        # Convert PDF to JSON
        with open(file.name, 'rb') as f:
            pdf_data = f.read()
        data = pdf_to_json(pdf_data)

    elif file.name.endswith('.txt'):
        # Convert TXT to JSON
        with open(file.name, 'r') as f:
            txt_content = f.read()
        data = txt_to_json(txt_content)

    elif file.name.endswith('.fountain'):
        # Convert Fountain to JSON
        with open(file.name, 'r') as f:
            fountain_content = f.read()
        data = fountain_to_json(fountain_content)

    elif file.name.endswith('.json'):
        # Load the JSON file directly
        with open(file.name, 'r') as f:
            data = json.load(f)
    else:
        # Unsupported file format
        json_file = None
        raise ValueError("Unsupported file format")

    with open(json_file, 'w') as f:
        json.dump(data, f)

    # Load the JSON file and send it to OpenAI for analysis
    with open(json_file, 'r') as f:
        data = json.load(f)
   
    # Call the generate_analysis function to get the analysis results
    if model == "gpt-3.5-turbo":
        result = generate_analysis_35(data, model)
    #DEBUG: Return tmp json output
    elif model == "debug":
        result = json.dumps(data, indent=4)
    else:
        result = "Not set up yet"
 
    return result
    

file = gr.File(label="Screenplay file (.pdf, .txt, .fountain, or .json)")
api_key = gr.Textbox(value=api_key, label="OpenAI API key")
model = gr.Dropdown(["gpt-3.5-turbo", "text-davinci-003", "debug"], label="OpenAI Model")
# analyze_button = gr.Button(label="Analyze")
output = gr.Textbox(label="Analysis results")

gr.Interface(
    analyze_callback,
    inputs=[file, model, api_key],
    outputs=output,
    title="Script Coverage AI",
    description="Use AI to analyze a screenplay and get professional-level script coverage.",
    theme="default",
).launch()