import openai
import argparse

from google.colab import drive
drive.mount('/content/drive')

# Define function to translate text using OpenAI API
def translate_chunk(text, model_,target_language,):    
    wait_time = 2  # seconds 
    max_wait_time = 60  # seconds    
    if not text:
        return ""
  
    while True:
        try:
            time.sleep(wait_time)
            response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{
                                'role': 'system',
                                'content': 'You are a translator assistant.'
                            }, {
                                "role":
                                "user",
                                "content":
                                f"Translate the following text into {target_language} in a way that is faithful to the original text. Return only the translation and nothing else:\n{text}",
                            }],
                            temperature=0.7,
            )
        
            t_text = (response["choices"][0].get("message").get(
                        "content").encode("utf8").decode())            
            return  t_text
            #return response.choices[0].text.strip()
        
        except Exception as e:
            print(str(e))    
            wait_time *= 2
            if wait_time > max_wait_time:
                wait_time = max_wait_time
            time.sleep(wait_time)
            continue            
 
def translate_file(input_file, output_file, model, api_key,target_language):
    openai.api_key = api_key

    # Read in the input file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Define the maximum length of text to be translated at once
    max_chunk_size = 1024

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
            translated_chunk = translate_chunk(current_chunk, model,target_language)
            output_text += translated_chunk

            # Reset the current chunk
            current_chunk = ""

    # If there is still text remaining in the current chunk, translate it and append the translated text to the output text
    if current_chunk != "":
        translated_chunk = translate_chunk(current_chunk, model,target_language)
        output_text += translated_chunk

    # Write the translated text to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input Markdown file in Google Drive")
    parser.add_argument("output_file", help="path to output translated Markdown file in Google Drive")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="name of the OpenAI model to use (default: text-davinci-003)")
    parser.add_argument("--openai_key", required=True, help="OpenAI API key")
    args = parser.parse_args()

    # Get the full path of the input and output files
    #input_path = '/content/drive/MyDrive/data/' + "input.md"
    #output_path = '/content/drive/MyDrive/data/' + "output.md"
    input_path = args.input_file
    output_path = args.output_file

    print("input_path:",input_path)
    print("output_path:",output_path)
    # Translate the input file and save the translated text to the output file
    translate_file(input_path, output_path, args.model, args.openai_key,"English")
