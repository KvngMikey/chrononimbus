import os
from dotenv import load_dotenv
load_dotenv()

from google.generativeai import models

available_models = models.list_models()

for m in available_models:
    print("MODEL:", m.name)

    # New SDK: capabilities = part of `model.supported_input_output`
    sio = getattr(m, "supported_input_output", None)
    if sio:
        print("  INPUTS :", sio.input)
        print("  OUTPUTS:", sio.output)
    else:
        print("  (No input/output metadata available)")

    print("-" * 40)
