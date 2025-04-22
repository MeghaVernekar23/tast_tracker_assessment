
from db.models.db_models import Documents
from unittest.mock import MagicMock
import pytest
from service.document_service import save_document
from exceptions import DuplicateFileException


@pytest.fixture
def get_mock_session():
    return MagicMock()

def test_save_document(get_mock_session):
    get_mock_session.query.return_value.filter.return_value.first.return_value = []
    result = save_document("megha","pdf","abcd", get_mock_session)
    saved_documents = get_mock_session.add.call_args[0][0]
    get_mock_session.refresh.assert_called_once_with(saved_documents)
    assert result == {"message": "Document uploaded successfully"}

def test_save_document_duplicate_file(get_mock_session):
    get_mock_session.query.return_value.filter.return_value.first.return_value = "Megha"
    with pytest.raises(DuplicateFileException):
        save_document("megha","pdf","abcd", get_mock_session)

        



