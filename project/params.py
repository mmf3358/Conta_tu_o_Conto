

### Configuraçoes PEFT
R = 8
LORA_ALPHA = 32
LORA_DROPOUT = 0.1


### Configurações do Modelo
MODEL_PATH = 'model'
TRAIN_FILE_PATH = 'raw_data/data_cleaned.csv'
MODEL_NAME = 'gpt2'
PER_DEVICE_TRAIN_BATCH_SIZE = 16
NUM_TRAIN_EPOCHS = 5.0
SAVE_STEPS = 20

LEARNING_RATE = 5e-3 
LOGGING_STEPS = 20