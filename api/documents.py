from click import File
from fastapi import APIRouter, HTTPException, UploadFile, Depends
from db.sessions import get_db, create_tables
from sqlalchemy.orm import Session
from db.models.db_models import Documents
from service.document_service import save_document, document_download
from exceptions import DuplicateFileException, FileNotFoundException
document_router = APIRouter()

create_tables()

@document_router.post("/upload")
async def upload_document(document: UploadFile = File(...) , db: Session = Depends(get_db)):
    try:
        content = await document.read()
        return save_document(document_name = document.filename,document_type = document.content_type, document_data = content ,db=db)
    except DuplicateFileException as e:
        raise HTTPException(status_code= 409,detail= str(e)) 
    except Exception as e:
        raise HTTPException(status_code= 500,detail= "Error occured while uploading the document" )  

@document_router.get("/download/{document_name}")
async def download_document(document_name: str, db: Session= Depends(get_db)):
    try:
        return document_download(document_name = document_name, db=db)
    except FileNotFoundException as e:
        raise HTTPException(status_code= 404,detail= str(e)) 
    except Exception as e:
        raise HTTPException(status_code= 500,detail= "Error occured while downloading the document" ) 

    
    
