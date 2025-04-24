
from db.models.db_models import Documents
from sqlalchemy.orm import Session
from exceptions import DuplicateFileException, FileNotFoundException
from fastapi.responses import StreamingResponse
import io

def save_document(document_name: str,document_type: str, document_data: bytes, db: Session):
    document_exists  = db.query(Documents).filter(Documents.document_name == document_name).first()
    if document_exists:
        raise DuplicateFileException()  
    documents = Documents(document_name = document_name,document_type = document_type, document_data = document_data)
    db.add(documents)
    db.commit()
    db.refresh(documents)
    return {"message": "Document uploaded successfully"}


def document_download(document_name: str, db: Session):
    document_exists  = db.query(Documents).filter(Documents.document_name == document_name).first()
    if not document_exists:
        raise FileNotFoundException()  
    
    return StreamingResponse(
        io.BytesIO(document_exists.document_data),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={document_exists.document_name}"}
    )    




