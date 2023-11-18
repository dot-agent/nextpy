"""Firebase Realtime Database Loader."""

from typing import Dict, List, Optional

from openams.rag.document_loaders.basereader import BaseReader
from openams.schema import DocumentNode


class FirebaseRealtimeDatabaseReader(BaseReader):
    """Firebase Realtime Database reader.

    Retrieves data from Firebase Realtime Database and converts it into the DocumentNode used by LlamaIndex.

    Args:
        database_url (str): Firebase Realtime Database URL.
        service_account_key_path (Optional[str]): Path to the service account key file.

    """

    def __init__(
        self,
        database_url: str,
        service_account_key_path: Optional[str] = None,
    ) -> None:
        """Initialize with parameters."""

        self.database_url = database_url

        try:
            import firebase_admin
            from firebase_admin import credentials
        except ImportError:
            raise ImportError("`firebase_admin` package not found, please run `pip install firebase-admin`")
        
        if not firebase_admin._apps:
            if service_account_key_path:
                cred = credentials.Certificate(service_account_key_path)
                firebase_admin.initialize_app(
                    cred, options={"databaseURL": database_url}
                )
            else:
                firebase_admin.initialize_app(
                    options={"databaseURL": database_url}
                )
        

    def load_data(self, path: str, field: Optional[str] = None) -> List[DocumentNode]:
        """Load data from Firebase Realtime Database and convert it into documents.

        Args:
            path (str): Path to the data in the Firebase Realtime Database.
            field (str, Optional): Key to pick data from

        Returns:
            List[DocumentNode]: A list of documents.

        """

        try:
            from firebase_admin import db
        except ImportError:
            raise ImportError("`firebase_admin` package not found, please run `pip install firebase-admin`")
        
        ref = db.reference(path)
        data = ref.get()

        documents = []

        if isinstance(data, Dict):
            for key in data:
                entry = data[key]
                metadata = {
                    "document_id": key,
                    "databaseURL": self.database_url,
                    "path": path,
                    "field": field 
                }
                if type(entry) is Dict and field in entry:
                  text = entry[field]
                else:
                  text = str(entry)
                
                DocumentNode = DocumentNode(text=text, extra_info=metadata)
                documents.append(DocumentNode)
        elif isinstance(data, str):
            documents.append(DocumentNode(text=data))

        return documents