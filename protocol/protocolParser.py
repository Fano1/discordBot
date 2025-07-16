from google import genai
# from .api import GEMINI_KEY
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
    model="gemini-2.0-flash-exp-image-generation",
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