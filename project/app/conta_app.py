from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from project.model_utils import generate_text, summarizer
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

    outputs = []
    summarized_outputs = []

    for i in range(3):
        output = generate_text(context, GENERATOR_MAX_OUTPUT_LENGTH)
    
        output = output[len(context):]
        outputs.append(output)
    
        summary = summarizer(output)
        summarized_outputs.append(summary)
        
    return outputs, summarized_outputs
     