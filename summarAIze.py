import os
import PyPDF2
from openai import OpenAI
import time
from docx import Document

OPENAI_API_KEY = 'sk-proj-oGkG5hWdwTXHgYqn8fOcT3BlbkFJqdO0xajwcjtRp6F0PN3n'
client = OpenAI(api_key = OPENAI_API_KEY)
    
def read_pdf(pdf_file_path,page):
    pdf_summary_text = ""
    pdf_file = open(pdf_file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    i = 0
    pages= len(pdf_reader.pages)
    for page_num in range(page, pages, 1):
        try:
            summary = ""
            page_text = pdf_reader.pages[page_num].extract_text().lower()
            print(f"page {page_num +1}/{pages}")
            
            while True:
                try:
                    response = client.chat.completions.create(
                                    model="gpt-3.5-turbo",
                                    messages=[
                                        {"role": "system", "content": "You are a helpful research assistant."},
                                        {"role": "user", "content": "Summarize the content {}. Capitalize and bold keywords".format(page_text)}
                                            ],
                                                )
                    page_summary = response.choices[0].message.content
                    print(page_summary)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(60)
            summary +="Page: " + str(page_num) + "\n" + page_summary + "\n\n"
            pdf_summary_text += summary
            pdf_summary_file = pdf_file_path.replace(os.path.splitext(pdf_file_path)[1], "_summary.txt")

            with open(pdf_summary_file, "w+", encoding="utf-8") as file:
                        file.write(pdf_summary_text)
            i += 1
        except Exception as e:
            print(e)
            continue

    pdf_file.close()

def read_word(file):
    doc = Document(file)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text  

if __name__=='__main__':
    pdf_file_path = ""
    page = 0  
    selection = input("Enter the file type: pdf or docx: ")
    if selection == "pdf":
            pdf_file_path = (input("Enter the path to your PDF file: "))
            read_pdf(pdf_file_path,page)
    elif selection == "docx":
            docx_file_path = input("Enter the path to your DOCX file: ")
            text = read_word(docx_file_path)
            print(text)
            response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a helpful research assistant."},
                                {"role": "user", "content": "Summarize the content {}. Capitalize and bold keywords".format(text)}
                                    ],
                                        )
            summary = response.choices[0].message.content
            print(summary)
    else:
            print("Invalid file type")
            exit(1)

  
