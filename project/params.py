import os


MODEL_PATH = os.environ.get('MODEL_PATH')
TRAIN_FILE_PATH = os.environ.get('TRAIN_FILE_PATH')
MODEL_NAME = os.environ.get('MODEL_NAME')

TRANSLATOR_EN_PT = os.environ.get('TRANSLATOR_EN_PT')
TRANSLATOR_PT_EN = os.environ.get('TRANSLATOR_PT_EN')


### Configuraçoes PEFT
R = 8
LORA_ALPHA = 32
LORA_DROPOUT = 0.1

### Configurações do Modelo
PER_DEVICE_TRAIN_BATCH_SIZE = 16
NUM_TRAIN_EPOCHS = 5.0
SAVE_STEPS = 20
LEARNING_RATE = 5e-3 
LOGGING_STEPS = 20
TEMPERATURE = .6
MAX_LENGTH = 200

### Generator
GENERATOR_MAX_OUTPUT_LENGTH = 50

### Summarizer
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"

