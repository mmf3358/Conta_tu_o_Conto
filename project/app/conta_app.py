from fastapi import FastAPI
import torch
from nltk.tokenize import word_tokenize
from fastapi.middleware.cors import CORSMiddleware
from project.model_utils import generate_text, summarizer,translator,DotStoppingCriteria
from project.params import *

app = FastAPI()
#app.state.model = load_model(stage='Staging')

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get('/generate_outputs')
def generate_outputs(context):

    stopping_criteria = DotStoppingCriteria()
    outputs = []
    summarized_outputs = []

    for i in range(3):

        context_en = translator(f"translate Portuguese to English:{context}",TRANSLATOR_PT_EN)[0]['translation_text']
        output_en = generate_text(context_en,stopping_criteria=stopping_criteria)
        output_pt = translator(output_en[0]['generated_text'][len(context_en):],TRANSLATOR_EN_PT)[0]['translation_text']
        outputs.append(output_pt)

    # # Display the generated outputs
        print("Generated outputs:")
        print(outputs)

        length = len(word_tokenize(output_pt))
        summary = summarizer(output_pt, max_length = length-5, min_length = length-10,stopping_criteria=stopping_criteria)[0]['summary_text']
        summarized_outputs.append(summary)

    return outputs,summarized_outputs
