from google import genai
import io
# from .api import GEMINI_KEY
import serial
import time
import PIL.Image
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types

from .api import GEMINI_KEY

client = genai.Client(api_key= GEMINI_KEY)


def GenerateDefaultText(content):
    response = client.models.generate_content(
        model = "gemini-2.5-flash",

        contents=[content],
        config= genai.types.GenerateContentConfig(
            max_output_tokens=800,
            temperature=0.1 #randomness of the model 
            #holy shit the prompt model fucks everything up, dont touch the topk and bottomk
        )
    )
    return (response.candidates[0].content.parts[0].text)

def GenerateImage(self):
    response = client.models.generate_content(
    # model="gemini-2.0-flash-exp-image-generation",
    model="gemini-2.0-flash-preview-image-generation",
    contents= self,
    config=types.GenerateContentConfig(
          response_modalities=['Text', 'Image']
        )
    )
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save('images\\latest.png')

def InputImage(img_bytes, content):
    image = Image.open(io.BytesIO(img_bytes))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[image, content]
    )
    return (response.text)


def EditImage(img_bytes, content):
    image = Image.open(io.BytesIO(img_bytes))

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[content, image],
        config=types.GenerateContentConfig(
              response_modalities=['Text', 'Image']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save('images\\generated.png')

def LedOn(n):
    arduino = serial.Serial('COM10', 9600, timeout=1)
    time.sleep(2)  # Let Arduino reset

    arduino.write(b'1')  # Turn on LED
    time.sleep(n)
    arduino.write(b'0')
    print("Sent: LED OFF")

    arduino.close()


