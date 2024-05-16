from langchain.schema import Document
import pandas as pd
from typing import List

class Retriever:
    """
    Retriever class to retrieve documents from the database.
    """
    def __init__(self, cfg: dict, conn, embeddings):
        """
        Initialize the Retriever class.

        Args:
            cfg (dict): Configuration dictionary.
            conn: Connection to the database.
            embeddings: Embeddings object.
        """
        
        self.cfg = cfg
        self.conn = conn
        self.embeddings = embeddings

    def df_to_docs(self, df: pd.DataFrame) -> List[Document]:
        """
        Convert the dataframe to a list of Document objects.

        Args:
            df (pd.DataFrame): Dataframe of retrieved documents.

        Returns:
            List[Document]: List of Document objects.
        """

        docs = [
            Document(
                page_content=row['content'],
                metadata={
                    'score': row['score'],
                    'title': row['title'],
                    'chunk_id': row['chunk_id']
                }
            )
            for _, row in df.iterrows()
        ]
        return docs

    def similarity_search(self, query: str, k: int = 3) -> pd.DataFrame:
        """
        Perform similarity search using the embeddings.

        Args:
            query (str): Query string.
            k (int): Number of documents to retrieve.

        Returns:
            pd.DataFrame: Dataframe of retrieved documents.
        """

        sim_search_query = f'''
        SELECT chunk_id, title, content, embeddings, 1 - (embeddings <-> %s::vector) AS score
        FROM {self.cfg['table']}
        ORDER BY score DESC
        LIMIT %s
        '''

        emb = list(self.embeddings.embed_query(query))
        cur = self.conn.cursor()

        try:
            cur.execute(sim_search_query, (emb, k))
            rows = cur.fetchall()
        except Exception as e:
            cur.close()
            raise e

        cur.close()
        df = pd.DataFrame(rows, columns=['chunk_id', 'title', 'content', 'embeddings', 'score'])
        return df

    def retrieve_docs(self, query: str, k: int = 3) -> List[Document]:
        """
        Retrieve documents based on the query.

        Args:
            query (str): Query string.
            k (int): Number of documents to retrieve.

        Returns:
            List[Document]: List of Document objects.
        """

        df = self.similarity_search(query, k)
        docs = self.df_to_docs(df)
        return docs
