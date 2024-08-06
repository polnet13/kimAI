import os
import sys


# BASE_DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OCR 커스텀
model_name = 'best_norm_ED'
model_alchitecture = 'None-VGG-BiLSTM-CTC-Seed1111'
OCR_MODEL = os.path.join(BASE_DIR, 'rsc', 'saved_models', model_alchitecture)