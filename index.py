import os
import re
import fitz
from langchain.text_splitter import SpacyTextSplitter
import uuid

class Index:
    """
    Index class for managing document indexing.
    """
    def __init__(self, cfg, conn, embeddings):
        """
        Initialize the Index class.

        Args:
            cfg (dict): Configuration dictionary.
            conn: Connection to the database.
            embeddings: Embeddings object.
        """
        
        self.cfg = cfg
        self.conn = conn
        self.embeddings = embeddings
        self.text_splitter = SpacyTextSplitter(chunk_size=self.cfg['chunk_size'], chunk_overlap=self.cfg['chunk_overlap'])

    def get_chunks(self, doc):
        """
        Split the text of a document into chunks.

        Args:
            doc: PDF document object.

        Returns:
            dict: Dictionary containing page number as key and list of text chunks as value.
        """

        file_dict = {}
        i = 0
        for page in doc:
            text = page.get_text()
            text = text.strip()
            text = text.replace("\n", " ")
            text = re.sub(r'[ ]+', ' ', text)
            text = re.sub(r'[^a-zA-Z0-9&\-+/\\*]', ' ', text)
            chunks = self.text_splitter.split_text(text)
            file_dict[f"page_{i}"] = chunks
            i += 1
        return file_dict
    
    def create_table(self):
        """
        Create a table in the database for storing document chunks.
        """

        cur = self.conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {self.cfg['table']}")
        cur.execute(f'''CREATE TABLE {self.cfg['table']} (
                        chunk_id VARCHAR NOT NULL,
                        title VARCHAR NOT NULL,
                        content VARCHAR NOT NULL,
                        embeddings VECTOR(768) NOT NULL
                    )''')
        self.conn.commit()
        print(f"Table {self.cfg['table']} created successfully")
    
    def insert_file(self, file_dir, file_name):
        """
        Insert document chunks into the database from a single file.

        Args:
            file_dir (str): Directory containing the file.
            file_name (str): Name of the file.
        """

        file_path = os.path.join(file_dir, file_name)
        doc = fitz.open(file_path)
        file_dict = self.get_chunks(doc)

        cur = self.conn.cursor()
        for page, chunks in file_dict.items():
            for chunk in chunks:
                emb = list(self.embeddings.embed_query(chunk))
                cur.execute(f"INSERT INTO {self.cfg['table']} (chunk_id, title, content, embeddings) VALUES (%s, %s, %s, %s)", (str(uuid.uuid4()), file_name + page, chunk, emb))
        self.conn.commit()
        print(f"File {file_name} inserted successfully")
    
    def insert_dir(self, file_dir):
        """
        Insert document chunks into the database from all files in a directory.

        Args:
            file_dir (str): Directory containing the files.
        """

        for file_name in os.listdir(file_dir):
            if os.path.isfile(os.path.join(file_dir, file_name)):
                self.insert_file(file_dir, file_name)
