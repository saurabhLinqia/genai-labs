# import boto3
import json, time
# import sagemaker
from sagemaker.session import Session
from sagemaker.predictor import Predictor



class SagemakerLlama2TextGenModel():
    
    def __init__(self, endpoint_name, sagemaker_session: Session, max_retries=3):
        # print("SagemakerEmbeddingsModel.__init__ fired")
        self.model_predictor = Predictor(endpoint_name = endpoint_name, sagemaker_session = sagemaker_session)
        self.max_retries = max_retries
        self.retry_time = 1
        

    # Llama Supported Parameters

    # max_new_tokens: 
    #   Model generates text until the output length (excluding the input context length) reaches max_new_tokens. If specified, 
    #   it must be a positive integer.

    # temperature: 
    #   Controls the randomness in the output. Higher temperature results in output sequence with low-probability words 
    #   and lower temperature results in output sequence with high-probability words. If temperature -> 0, it results in 
    #   greedy decoding. If specified, it must be a positive float.

    # top_p: 
    #   In each step of text generation, sample from the smallest possible set of words with cumulative probability top_p. If 
    #   specified, it must be a float between 0 and 1.
    # 
    # return_full_text: 
    #   If True, input text will be part of the output generated text. If specified, it must be boolean. The default 
    #   value for it is False.

    # You may specify any subset of the parameters mentioned above while invoking an endpoint.

    # Methods to query the model and parse the output 
    def query_endpoint(self, prompt):    
        # query the model
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 64, 
                "top_p": 0.9, 
                "temperature": 0.6,
                "return_full_text": False,
            }
        }

        print("encoding payload")
        encoded_payload = json.dumps(payload).encode("utf-8")
        tries = 0
        while tries < self.max_retries:
            try: 
                tries += 1
                query_response = self.model_predictor.predict(
                    encoded_payload,
                    {
                        "ContentType": "application/json",
                        "Accept": "application/json",
                        "CustomAttributes": "accept_eula=true" # for Meta models
                    },
                )
                # result = self.parse_text_response(query_response)
                # print("\n") # reset the print cursor from the inference loop
                response = json.loads(query_response)
                # return response
                # return response[0]['generated_text']
                return response[0]['generation']
            
            except Exception as e:
                print("error calling the model")
                print(str(e))
                print("retrying in {} seconds".format(self.retry_time))
                time.sleep(self.retry_time)
                continue


    def query_chat_endpoint(self, instruction, context, question):    
        # query the model
        params = {
            "max_new_tokens": 64, 
            "top_p": 0.9, 
            "temperature": 0.6,
            "return_full_text": False,
        }
        prompt = [[
            {"role": "system", "content": instruction },
            {"role": "user", "content": question },
        ]]
                
        payload = {
            "inputs": prompt ,
            "parameters": params
        }

        print("encoding payload")
        encoded_payload = json.dumps(payload).encode("utf-8")
        tries = 0
        while tries < self.max_retries:
            try: 
                tries += 1
                query_response = self.model_predictor.predict( 
                    encoded_payload,
                    {
                        # "ContentType": "application/json",
                        # "Accept": "application/json",
                        "CustomAttributes": "accept_eula=true" # for Meta models
                    },
                )
                
                # result = self.parse_text_response(query_response)
                # print("\n") # reset the print cursor from the inference loop
                # response = json.loads(query_response)
                # return response
                # return response[0]['generated_text']
                # return response[0]['generation']
                return query_response
            
            except Exception as e:
                print("error calling the model")
                print(str(e))
                print("retrying in {} seconds".format(self.retry_time))
                time.sleep(self.retry_time)
                continue

