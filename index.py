#%%
import streamlit as st 
import os 
import requests 
import json 
#%%
def save_uploaded_file(uploaded_file, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    #Save the file to specific directory
    with open(os.path.join(save_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.get_buffer())
    st.success('File saved successfully')

# Function to send file to API and get results
def process_file(file):
    url = 'https://the-ocr-experiment-hlvqp3d7wq-uc.a.run.app/getOCR/paddle/'
    files = {'file_': file}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        return str(json.loads(response.json()['textResult']))
    else:
        return "Unable to Process"

def main_func():
    st.set_page_config(
        page_title="Image Digitisation",
        page_icon=":whale:",
        initial_sidebar_state="auto"
        ) 

    st.title('Hello World!')
    __ocrtype_help = ''

    label = 'Select OCR'

    _ocrtype = st.radio(label = label,
                            options = ['Paddle OCR'],
                            horizontal=True,
                            index=None,
                            help = __ocrtype_help)
    st.write('You selected: ', _ocrtype)
     
    #Upload File
    uploaded_file = st.file_uploader("Upload File", type = ['png', 'jpg', 'jpeg'], accept_multiple_files=False)

    #Define the directory
    save_dir = "DataDump"

    if uploaded_file is not None:
        image = uploaded_file.read()
        st.image(image, caption = 'Uploadded Image', use_column_width=True)

        #Save the uploaded file 
        # save_uploaded_file(uploaded_file, save_dir)
        result = process_file(uploaded_file)

        if result is not None:
            st.write("API Results:")
            st.json(result)
        else:
            st.error("Failed to get results from API")


if __name__ == '__main__':
    main_func()

