from transformers import pipeline
from project.model_utils import generate_text, summarizer
from project.params import *



### texto inicial.
   ### introduzir nome do heroi
   ### idade do heroi
   ### contexto
    


context = f'Once uppon a time, there was a boy called John. One day he went to the castle'

### criar 3 outputs com o modelo cgpt2
### subtrair input dos outputs
### sumarizar 3 outputs.


outputs = []
summarized_outputs = []


for i in range(3):
    output = generate_text(context, GENERATOR_MAX_OUTPUT_LENGTH)
    
    output = output[len(context):]
    outputs.append(output)




        # Display the generated outputs
print("Generated outputs:")
for i, output in enumerate(outputs):
    summary = summarizer(output)
    print(f'\n{output}')
    print(f'\n{summary}')
    
#for i in range(3):
    #print(f'\n\n\n{outputs[i]}\n{summarized_outputs[i]}')
### oferecer escolhas dos outputs sumarizados ao utilizador.



### usar output correspondente à escolha do utilizador como input seguinte.



### volta ao inicio, se não for terminado.