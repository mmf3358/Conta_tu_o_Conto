

from project.params import *
from project.model_utils import train


train(
    train_file_path=TRAIN_FILE_PATH,
    model_name=MODEL_NAME,
    output_dir=MODEL_PATH,
    overwrite_output_dir=True,
    per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
    num_train_epochs=NUM_TRAIN_EPOCHS,
    save_steps=SAVE_STEPS
)