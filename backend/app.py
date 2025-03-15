from fastapi import FastAPI, File, UploadFile

import fitz

app = FastAPI()

"""
Handles receiving the course note and exam PDFs and combining them into one larger bit of text

Arguments:
    files (list[UploadFile]): A list of UploadFile representing the uploaded file
    
Returns:
    The amalgated wall of text of either the course notes or exams
"""
async def extract_text(files:list[UploadFile] = File(...)) -> dict:
    pdf_text = ""
    
    for file in files:
        # Read file bytes and open in as PDF file
        file_content = await file.read()
        doc = fitz.open(stream=file_content, filetype="pdf")
        
        # Get text from PDF file
        for page in doc:
            pdf_text += page.get_text("text")
        
        # Return the combined text
        return { "text": pdf_text }



"""
Extract plaintext of course notes, combine into one string, assign a user
"""
@app.post("/upload-course-notes")
async def upload_course_notes(files: list[UploadFile] = File(...)):
    plain_text: dict = extract_text(files)
    


"""
Handle receiving the PDF exams from the frontend

Input data should be a list of UploadFiles representing the PDF exams.
Extract text from the PDF files and combine into one document
"""
@app.post("/upload-exams")
async def upload_exams(files: list[UploadFile] = File(...)):
    plain_text: dict = extract_text(files)