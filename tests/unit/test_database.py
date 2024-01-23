import unittest
from unittest.mock import patch, MagicMock
from src.database.database import WeaviatePDFManager

class TestWeaviatePDFManager(unittest.TestCase):

    @patch('src.database.database.weaviate.Client')
    def test_create_schema(self, mock_weaviate_client):
        manager = WeaviatePDFManager('weaviate_url', 'weaviate_api_key', 'openai_api_key')
        class_name = 'TestSchemaClass'

        manager.create_schema(class_name)

        # Assert that the create_class method is called on the mock_weaviate_client
        mock_weaviate_client.return_value.schema.create_class.assert_called_once_with({
            "class": class_name,
            "vectorizer": "text2vec-openai",
            "properties": [
                {
                    "name": "text",
                    "dataType": ["text"],
                },
            ],
            "moduleConfig": {
                "generative-openai": {},
                "text2vec-openai": {"model": "ada", "modelVersion": "002", "type": "text"},
            },
        })

    @patch('src.database.database.weaviate.Client')
    def test_query_data(self, mock_weaviate_client):
        manager = WeaviatePDFManager('weaviate_url', 'weaviate_api_key', 'openai_api_key')
        class_name = 'TestQueryClass'
        query_text = 'query_text'
        limit = 5

        manager.query_data(class_name, query_text, limit)

        # Assert that the get method is called on the query
        mock_weaviate_client.return_value.query.get.assert_called_once_with(class_name, ["text"])

if __name__ == '__main__':
    unittest.main()
