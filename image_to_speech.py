# -*- coding: utf-8 -*-
"""image_to_speech.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MI7P7CoaRJ0lkp4o8W_c_9aYrvdpX_JJ
"""

!pip install langchain
!pip install transformers
!pip install -U langchain langchain-community
!pip install -U langchain-huggingface
!pip install --upgrade langchain langchain-core

from transformers import pipeline
from langchain import LLMChain, PromptTemplate
from langchain_community.llms import HuggingFaceHub
import matplotlib.pyplot as plt

#convert an image to text using an image captioning model
def img2text(url):
  pipe = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
  text = pipe(url)[0]["generated_text"]
  return text

print(img2text("zwm.png"))

from langchain_huggingface import HuggingFaceEndpoint

repo_id = "tiiuae/falcon-7b-instruct"
hf_token = " # Replace with your actual token"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    huggingfacehub_api_token=hf_token,
    temperature=0.1,
    max_new_tokens=1500,
    verbose=False
)

from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
import os
import textwrap

# Set your Hugging Face token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = " # Replace with your actual token"

# Create LLM with parameters passed explicitly
llm = HuggingFaceEndpoint(
    repo_id="tiiuae/falcon-7b-instruct",
    task="text-generation",
    temperature=0.7,
    max_new_tokens=300
)

# Define the prompt
prompt = PromptTemplate.from_template(
    "Write a detailed, suspenseful story based on this scenario:\n\n{scenario}"
)

# Create the runnable chain using the pipe operator
chain = prompt | llm

# Your input scenario
scenario = "A boy was in depression because he was not getting jobs."

# Invoke the chain
response = chain.invoke({"scenario": scenario})

# Combine scenario and response
full_story = scenario + " " + response

# Wrap the full story for better formatting
wrapped_story = textwrap.fill(full_story, width=100)

# Print the result
print("Generated Story:\n")
print(wrapped_story)

import requests

def text2speech(text, lang_code="eng"):  # default: English
    API_URL = f"https://router.huggingface.co/hf-inference/models/facebook/mms-tts-{lang_code}"
    headers = {"Authorization": "Bearer  # Replace with your actual token"}

    response = requests.post(API_URL, headers=headers, json={"inputs": text})

    if response.status_code == 200:
        return response.content
    else:
        print("TTS Error:", response.status_code, response.text)
        return None

from langchain_core.prompts import PromptTemplate

def generate_story(scenario, llm):
    prompt = PromptTemplate.from_template(
        "Write a detailed, suspenseful story based on this scenario:\n\n{scenario}"
    )
    chain = prompt | llm
    return chain.invoke({"scenario": scenario})

from IPython.display import Audio, display, Markdown
import ipywidgets as widgets
from google.colab import files
import matplotlib.pyplot as plt

# Display the image
img_file = "pic3.jpg"
img = plt.imread(img_file)
plt.imshow(img)

# Generate image caption (scenario)
scenario = img2text(img_file)
print("Image Caption:", scenario)

# Generate story from scenario
story = generate_story(scenario, llm)
display(Markdown(f"**Generated Story:**\n\n{story}"))

# Convert story to speech
audio_bytes = text2speech(story)

if audio_bytes:
    # Save the audio temporarily
    audio_filename = "story_audio.wav"
    with open(audio_filename, "wb") as f:
        f.write(audio_bytes)

    # Play the audio
    display(Audio(audio_filename))

    # Create a download button (only if user clicks)
    def download_audio(b):
        files.download(audio_filename)

    download_button = widgets.Button(description="Download Audio 🎧", button_style='success')
    download_button.on_click(download_audio)

    display(widgets.HTML("<b>Click the button below to download the audio file (optional):</b>"))
    display(download_button)
else:
    print("No audio generated.")