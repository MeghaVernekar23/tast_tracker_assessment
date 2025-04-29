from click import File
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from db.sessions import create_tables, get_db
from exceptions import DuplicateFileException, FileNotFoundException
from service.auth import get_current_user
from service.document_service import document_download, save_document

document_router = APIRouter()

create_tables()

@document_router.post("/upload", dependencies=[Depends(get_current_user)])
async def upload_document(document: UploadFile = File(...) , db: Session = Depends(get_db)):
    try:
        content = await document.read()
        return save_document(document_name = document.filename,document_type = document.content_type, document_data = content ,db=db)
    except DuplicateFileException as e:
        raise HTTPException(status_code= 409,detail= str(e)) 
    except Exception as e:
        raise HTTPException(status_code= 500,detail= "Error occured while uploading the document" )  

@document_router.get("/download/{document_name}", dependencies=[Depends(get_current_user)])
async def download_document(document_name: str, db: Session= Depends(get_db)):
    try:
        return document_download(document_name = document_name, db=db)
    except FileNotFoundException as e:
        raise HTTPException(status_code= 404,detail= str(e)) 
    except Exception as e:
        raise HTTPException(status_code= 500,detail= "Error occured while downloading the document" ) 

    
    
