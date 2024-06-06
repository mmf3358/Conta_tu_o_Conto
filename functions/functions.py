from transformers import pipeline

def generate_text():
    stop_flag = False
    # Get user input
    user_input = input("Enter your input: ")

    while not stop_flag:

        # Check if the user wants to stop
        user_exit_input = input("Type 'stop' to exit or anything else to continue: ")

        if user_exit_input.lower() == "stop":
            stop_flag = True
            break

        # Generate text using the GPT-2 model
        generator = pipeline('text-generation',
                             model='gpt2',
                             truncation=True,
                             pad_token_id=50256, )
        outputs = generator(user_input,
                            # max_length=100,
                            num_return_sequences=3,
                            max_new_tokens=50)
        summarizer = pipeline("summarization",
                              model="facebook/bart-large-cnn")

        # Display the generated outputs
        print("Generated outputs:")
        for i, output in enumerate(outputs):
            summary = summarizer(output['generated_text'],
                                 max_length=20,
                                 min_length=10,
                                 do_sample=False)

            print(f"{i+1}, {summary[0]['summary_text']}")
            print(f"{i+1}. {output['generated_text']}")

        # Get user's choice
        choice = int(input("Choose an output (1-3): "))

        # Use the chosen output as the next input
        user_input = outputs[choice-1]['generated_text']

generate_text()
