# import boto3
import json, time
# import sagemaker
from sagemaker.session import Session
from sagemaker.predictor import Predictor



class SagemakerEmbeddingsModel():
    
    def __init__(self, endpoint_name, sagemaker_session: Session, max_retries=3):
        # print("SagemakerEmbeddingsModel.__init__ fired")
        self.model_predictor = Predictor(endpoint_name = endpoint_name, sagemaker_session = sagemaker_session)
        self.max_retries = max_retries
        self.retry_time = 1
        
    # all-minilm-l6-v2 and gpt-j-6b return embeddings with an extra array wrapper[] around the embedding result
    # vector space for all-minilm-l6-v2 is 384 
    # vector space for gpt-j is 4096
    def parse_response(self, query_response):
        """Parse response and return the embedding."""
        model_predictions = json.loads(query_response)
        # print('model response:', model_predictions)
        embeddings = model_predictions["embedding"]
        # print(f'got embeddings: {len(embeddings)}', end='\r')
        # print(f'first embedding length: {len(embeddings[0])}', end='\r')
        return embeddings[0]

    
    # Methods to query the model and parse the output 
    def query_endpoint(self, text):    
        """Query the model predictor."""
        encoded_text = text.encode("utf-8")
        tries = 0
        while tries < self.max_retries:
            try: 
                tries += 1
                query_response = self.model_predictor.predict(
                    encoded_text,
                    {
                        "ContentType": "application/x-text",
                        "Accept": "application/json",
                    },
                )
                result = self.parse_response(query_response)
                return result
            except:
                print("error calling the model")
                print(str(e))
                print("retrying in {} seconds".format(self.retry_time))
                time.sleep(self.retry_time)
                continue
            



