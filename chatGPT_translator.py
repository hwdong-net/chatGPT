import openai
import argparse
from google.colab import drive

# Mount Google Drive to access input and output files
drive.mount('/content/drive')

openai.api_key = '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'

def translate_chunk(chunk, model):
    response = openai.Completion.create(
        engine=model,
        prompt=chunk,
        max_tokens=1024,
        temperature=0.5,
        n=1,
        stop=None,
    )
    return response.choices[0].text

def translate_file(input_file, output_file, model):
    # Read in the input file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Define the maximum length of text to be translated at once
    max_chunk_size = 4096

    # Initialize variables to keep track of the current chunk and the output text
    current_chunk = ""
    output_text = ""

    # Iterate through the lines in the input file
    for line in lines:
        # Add the current line to the current chunk
        current_chunk += line

        # If the length of the current chunk exceeds the maximum chunk size
        if len(current_chunk) > max_chunk_size:
            # Translate the current chunk and append the translated text to the output text
            translated_chunk = translate_chunk(current_chunk, model)
            output_text += translated_chunk

            # Reset the current chunk
            current_chunk = ""

    # If there is still text remaining in the current chunk, translate it and append the translated text to the output text
    if current_chunk != "":
        translated_chunk = translate_chunk(current_chunk, model)
        output_text += translated_chunk

    # Write the translated text to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)
        
def main():
  # Get the full path of the input and output files
    input_path = '/content/drive/MyDrive/data/' + "1.md"
    output_path = '/content/drive/MyDrive/data/' + "1_out.md"

    # Translate the input file and save the translated text to the output file
    translate_file(input_path, output_path, args.model)

if __name__ == "__main__":
  main()
     
