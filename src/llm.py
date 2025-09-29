import openai
import dotenv
import os
import numpy as np

dotenv.load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def comp(
        user_prompt, 
        system_promt = "You are a helpful assistant that writes content based on the given prompt.",
        temperature=0,
        model="gpt-4.1"):

    completion = client.responses.create(
        model=model,
        input=[
            {
                "role": "developer",
                "content": system_promt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=temperature,
    )

    return completion.output_text

def comp_structure(
        user_prompt, 
        text_format,
        system_promt = "You are a helpful assistant that writes content based on the given prompt.",
        temperature=0,
        model="gpt-5-nano",
):

    completion = client.responses.parse(
        model=model,
        input=[
            {
                "role": "developer",
                "content": system_promt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        # temperature=temperature,
        text_format=text_format,
        reasoning={"effort":"minimal"},
    )

    return completion.output_parsed

def comp_embedding(text):
    response = client.embeddings.create(
    model="text-embedding-3-small",  # or "text-embedding-3-large"
    input=text
)

    # Extract embedding vector
    embedding = response.data[0].embedding

    return embedding

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    v1, v2 = np.array(vec1), np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def compare_texts(text1: str, text2: str):
    emb1 = comp_embedding(text1)
    emb2 = comp_embedding(text2)
    return cosine_similarity(emb1, emb2)