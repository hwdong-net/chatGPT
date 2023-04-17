import openai
import argparse
import time
import os   # process folder

#from google.colab import drive
#drive.mount('/content/drive')

# Define function to translate text using OpenAI API
request_counts_per_minute = 3
last_request_time = 0
request_counts = 0

def limit_request_counts(time_interval=60):
    global request_counts, last_request_time
    if request_counts == 0:
        last_request_time = time.monotonic() 
    request_counts += 1    
    if request_counts==request_counts_per_minute:
        elapsed_time = time.monotonic() - last_request_time
        if elapsed_time < time_interval:
             time.sleep(time_interval - elapsed_time)        
        last_request_time = time.monotonic()
        request_counts = 1
   
#https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions    
def translate_chunk(text, model_,target_language):  
    #limit_request_counts()
    wait_time = 20
    max_wait_time = 300
    if not text:
        return ""  
    while True:
        try: 
            time.sleep(wait_time)
            prompt = f""" I want you translate the text I give you into {target_language} in a way that is faithful to the original text. 
            But do not translate mathematical symbols and formulas such as latex or mathJax formulas. """
            prompt += r"""For example,the following text is a mathjax formulas:
            '$$z^{(i)} = \\pmb w \\odot \\pmb x^{(i)}= w_1 * x_1^{(i)}+w_2 * x_2^{(i)} +...+w_K * x_K^{(i)}+w_0 * x_0^{(i)}$$\n'.
            For mathematical symbols and formulas,the translation should be same as the the original text,you need not do any explanation. 
            If there are special characters such as newline characters '\n', '`' at the beginning or end of the original text, these characters will also be preserved in the translated text.
            """
            prompt += f"Return only the translation and nothing else:\n{text}"
            
            response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{
                                'role': 'system',
                                'content': 'You are a translator assistant.'
                            }, {
                                "role":
                                "user",
                                "content":
                                prompt, #f"Translate the following text into {target_language} in a way that is faithful to the original text.Keep the newline character '\n', mathematical formula symbols, brackets, and special symbols in the original text, such as '\n', '$', '{', '}', '(', ')'. Return only the translation and nothing else:\n{text}",
                            }],
                            temperature=0.7,
            )
        
            #print(response)
            #t_text = (response["choices"][0].get("message").get("content").encode("utf8").decode())              
            t_text = response['choices'][0]['message']['content']
            #t_text = (response["choices"][0].get("message").get("content"))
            #t_text = response["choices"][0].get("text")
            if t_text[-1] != "\n":
                t_text += "\n"
            return  t_text
            #return response.choices[0].text.strip()
        
        except Exception as e:
            print("Exception:"+str(e))   
            if 1:
                wait_time *= 2
                #if wait_time > max_wait_time:
                #   wait_time = max_wait_time
                print("sleep:",wait_time)      
                time.sleep(wait_time)
                     
            continue            

def translate_file(input_file, output_file, model, api_key,target_language):
    print("translating :",input_file)
    openai.api_key = api_key

    max_chunk_size = 100 # The limit of words in a request is set to 2048 tokens (words or symbols).  
    current_chunk = ""
    output_text = ""  
    debug = 1
    
    with open(output_file, "w", encoding="utf-8") as out_file:   # with open(output_file, , 'w') as out_file:
        with open(input_file, "r", encoding="utf-8") as f:     # with open(input_file) as in_file:
            for line in f:                
                if len(current_chunk)+len(line)>=max_chunk_size:          
                     translated_chunk = translate_chunk(current_chunk, model,target_language)                     
                     out_file.write(translated_chunk)                     
                     if debug:
                        print("\n"+repr(current_chunk))      #debug
                        print("===================================翻译的结果：")
                        print(repr(translated_chunk))      #debug
                     current_chunk = line
                else:
                      # Add the current line to the current chunk
                     current_chunk += line  

            if current_chunk != "":
                 translated_chunk = translate_chunk(current_chunk, model,target_language)               
                 out_file.write(translated_chunk)
         
            
def translate_file_(input_file, output_file, model, api_key,target_language):
    print("translating :",input_file)
    openai.api_key = api_key

    # Read in the input file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Define the maximum length of text to be translated at once
    max_chunk_size = 1000 # The limit of words in a request is set to 2048 tokens (words or symbols).

    # Initialize variables to keep track of the current chunk and the output text
    current_chunk = ""
    output_text = ""      
    
    # Iterate through the lines in the input file
    for line in lines:        
        if len(current_chunk)+len(line)>=max_chunk_size:
            # Translate the current chunk and append the translated text to the output text
            translated_chunk = translate_chunk(current_chunk, model,target_language)
            output_text += translated_chunk
            
             # Reset the current chunk
            current_chunk = line
        else:
            # Add the current line to the current chunk
            current_chunk += line

    # If there is still text remaining in the current chunk, translate it and append the translated text to the output text
    if current_chunk != "":
        translated_chunk = translate_chunk(current_chunk, model,target_language)
        output_text += translated_chunk

    # Write the translated text to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)


def translate_folder(folder_path, output_file_prefix, model, api_key,target_language,allowed_extensions):     
    prefix = output_file_prefix  # 前缀字符串

    # 获取文件夹下所有文件的列表
    file_list = os.listdir(folder_path)

    # 遍历所有文件
    for file_name in file_list:
        # 使用绝对路径构建文件路径
        if os.path.splitext(file_name)[1] not in allowed_extensions:
             continue
        file_path = os.path.join(folder_path, file_name)

        # 如果当前路径指向文件而不是文件夹，则进行处理
        if os.path.isfile(file_path):
            # 获取文件名和文件夹路径
            folder_path, old_file_name = os.path.split(file_path)

            # 将前缀字符串和文件名组合成新的文件名
            new_file_name = prefix + old_file_name

            # 构建新的文件路径
            trans_file_path = os.path.join(folder_path, new_file_name)
            
            # 翻译            
            translate_file(file_path, trans_file_path, model, api_key,target_language)
            
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to input Markdown file in Google Drive")
   # parser.add_argument("output_file", help="path to output translated Markdown file in Google Drive")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="name of the OpenAI model to use (default: text-davinci-003)")
    parser.add_argument("--openai_key", required=True, help="OpenAI API key")
    parser.add_argument("--target_language", required=True, help="OpenAI API key")
    args = parser.parse_args()

    # Get the full path of the input and output files
    #input_path = '/content/drive/MyDrive/data/' + "input.md"
    #output_path = '/content/drive/MyDrive/data/' + "output.md"
    input_path = args.input_file
    #output_path = args.output_file     
    
    # Translate the input file and save the translated text to the output file
    # translate_file(input_path, output_path, args.model, args.openai_key,args.target_language)
    
    prefix = "trans_"
    allowed_extensions = [".md", ".txt"]
    if os.path.isdir(input_path):   
        # input path is a folder, scan and process all allowed file types
        print("process folder\n")
        translate_folder(input_path,prefix,args.model, args.openai_key,args.target_language,allowed_extensions)
    elif os.path.isfile(input_path): 
        folder_path, file_name = os.path.split(input_path)          
        trans_file_name = prefix + file_name
        trans_file_path = os.path.join(folder_path, trans_file_name)
        translate_file(input_path,trans_file_path, args.model, args.openai_key,args.target_language)
    else:
       print("The input path is neither a file nor a directory.")
