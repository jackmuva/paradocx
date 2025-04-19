import os
from dotenv import load_dotenv
from pinecone import Pinecone
from pinecone.openapi_support import PineconeApiException
from langchain_openai.chat_models import ChatOpenAI
from llmlingua import PromptCompressor

load_dotenv()

def get_pinecone_indices(pc):
    try:
        dense = pc.Index(str(os.getenv('PINECONE_DENSE_INDEX')))
        sparse = pc.Index(str(os.getenv('PINECONE_SPARSE_INDEX')))
    except PineconeApiException:
        if not pc.has_index(str(os.getenv('PINECONE_DENSE_INDEX'))):
            pc.create_index_for_model(
                name=str(os.getenv('PINECONE_DENSE_INDEX')),
                cloud="aws",
                region="us-east-1",
                embed={ # pyright: ignore
                    "model":"multilingual-e5-large",
                    "field_map":{"text": "chunk_text"}
                }
            )
        dense = pc.Index(str(os.getenv('PINECONE_DENSE_INDEX')))

        if not pc.has_index(str(os.getenv('PINECONE_SPARSE_INDEX'))):
            pc.create_index_for_model(
                name=str(os.getenv('PINECONE_SPARSE_INDEX')),
                cloud="aws",
                region="us-east-1",
                embed={ # pyright: ignore
                    "model":"pinecone-sparse-english-v0",
                    "field_map":{"text": "chunk_text"}
                }
            )
        sparse = pc.Index(str(os.getenv('PINECONE_SPARSE_INDEX')))

    return dense, sparse 



def vector_search(index, query: str,top_k: int = 5, rerank:bool=False):
    if rerank:
        query_response = index.search_records(
            namespace=str(os.getenv('PINECONE_NAMESPACE')),
            query={
                "inputs": {"text": query},
                "top_k": top_k
            },
            rerank={
                "model": "cohere-rerank-3.5",
                    "rank_fields": ["text"]
            }
        )
    else:
        query_response = index.search_records(
            namespace=str(os.getenv('PINECONE_NAMESPACE')),
            query={
                "inputs": {"text": query},
                "top_k": top_k
            }
        )
    return query_response 

def merge_chunks(dense_matches, sparse_matches):
    deduped_hits = {hit['_id']: hit for hit in dense_matches['result']['hits'] + sparse_matches['result']['hits']}.values()
    return sorted(deduped_hits, key=lambda x: x['_score'], reverse=True)

def compress_prompt(llm_lingua, prompt:str, target_token=500):
    compressed_prompt = llm_lingua.compress_prompt(
        prompt, instruction="", question="", target_token=target_token
    )
    print(f"""savings: {compressed_prompt['saving']} | origin_tokens: {compressed_prompt['origin_tokens']} | compressed_tokens: {compressed_prompt['compressed_tokens']}""")
    return compressed_prompt['compressed_prompt']

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
llm_lingua = PromptCompressor(model_name="openai-community/gpt2", device_map="cpu")

def run_rag(prompt: str, search_method:str="dense", top_k:int=5, rerank:bool=False, summarization:bool=False, target_token=500):
    dense_index, sparse_index = get_pinecone_indices(pc)

    llm = ChatOpenAI(model="o4-mini-2025-04-16") 
    messages = [
        (
            "system",
            '''You are a helpful assistant that helps people search the useparagon (Paragon) docs. 
                Only use provided information retrieved as context. If context is irrelevant to the 
                prompt, do not use it. Do not hallucinate.''',
        ),
    ]
    
    if search_method == 'dense':
        response = vector_search(dense_index, prompt, top_k, rerank)
        context_text=[doc['fields']['text'] for doc in response.result['hits']]
        text_answer = " ".join(context_text)
    elif search_method == 'sparse':
        response = vector_search(sparse_index, prompt, top_k, rerank)
        context_text=[doc['fields']['text'] for doc in response.result['hits']]
        text_answer = " ".join(context_text)
    else:
        query_response = vector_search(dense_index, prompt, top_k, rerank)
        sparse_response = vector_search(sparse_index, prompt, top_k, rerank)
        response = {"result": {"hits": merge_chunks(query_response, sparse_response)}}
        context_text=[doc['fields']['text'] for doc in response['result']['hits']]
        text_answer = " ".join(context_text)

    if summarization:
        compressed_prompt=compress_prompt(llm_lingua, prompt, target_token)
        messages.append(("human", compressed_prompt))
    else:
        messages.append(("human", prompt))
     
    context = [doc['fields'] for doc in response['result']['hits']]
    instruction = "Using the provided information, give me a better and summarized answer"
       
    added_prompt = f"{text_answer} {instruction}"
    messages.append(("assistant", added_prompt))
    better_answer = llm.invoke(messages)
    return better_answer, context 
