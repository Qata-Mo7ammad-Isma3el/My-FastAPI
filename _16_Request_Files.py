# Request Files
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#
#> You can define files to be uploaded by the client using File. FastAPI provides two main ways to handle file uploads:

#> • File() - Receives files as bytes, storing the entire content in memory
#> • UploadFile - Provides a file-like object with metadata and streaming capabilities
#? Why Two Different Approaches?
#> • File() as bytes: Good for small files, simple to use, entire content loaded into memory
#> • UploadFile: Better for larger files, provides metadata, supports streaming, more memory efficient

## Import File Classes
#> First, import File and UploadFile from fastapi:
from fastapi import FastAPI, File, UploadFile

#!------------------ Key Concepts ------------------!#

## File as Bytes
#> When you declare a parameter with File(), FastAPI reads the entire file and provides it as bytes:
from fastapi import FastAPI, File

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

## UploadFile Class
#> For more control and better performance with larger files, use UploadFile:
from fastapi import FastAPI, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {
        "file":file.file,
        "filename": file.filename,
        "content_type": file.content_type
    }
### UploadFile Attributes
#> UploadFile provides useful metadata and methods:
#> • filename: Original filename (if provided by client)
#> • content_type: MIME type (e.g., "text/plain", "image/jpeg")
#> • file: File-like object for reading content
#> • read(): Read entire file content
#> • seek(): Move file pointer position
#> • close(): Close the file

## Multiple Files
#> You can also receive multiple files:

@app.post("/files/")
async def create_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

## Form Data Requirement
#> Files are sent as "form data" (multipart/form-data), which requires the python-multipart package to be installed.

#!------------------ Best Practices ------------------!#
#> • Use UploadFile for files larger than a few KB to avoid memory issues
#> • Always validate file types and sizes for security
#> • Check file.content_type to ensure acceptable file formats
#> • Use file.filename cautiously - sanitize before saving to disk
#> • Consider file size limits to prevent abuse
#> • Handle file upload errors gracefully

#!------------------ Common Pitfalls ------------------!#
#> • Using File() for large files: Can cause memory issues - use UploadFile instead
#> • Not validating file types: Security risk - always check content_type
#> • Trusting filename: Sanitize filenames before saving to prevent path traversal
#> • Missing python-multipart: File uploads won't work without this package
#> • Not handling upload errors: Always implement proper error handling



