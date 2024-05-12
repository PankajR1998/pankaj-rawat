from flask import Flask, request, jsonify
from flask import render_template,jsonify
from rag import RAG
import requests
import time
import json
app = Flask(__name__)

rag = RAG()
# texts = ["""Generative artificial intelligence (generative AI, GenAI,[1] or GAI) is artificial intelligence capable of generating text, images, videos, or other data using generative models,[2] often in response to prompts.[3][4] Generative AI models learn the patterns and structure of their input training data and then generate new data that has similar characteristics.[5][6]

# Improvements in transformer-based deep neural networks, particularly large language models (LLMs), enabled an AI boom of generative AI systems in the early 2020s. These include chatbots such as ChatGPT, Copilot, Gemini and LLaMA, text-to-image artificial intelligence image generation systems such as Stable Diffusion, Midjourney and DALL-E, and text-to-video AI generators such as Sora.[7][8][9][10] Companies such as OpenAI, Anthropic, Microsoft, Google, and Baidu as well as numerous smaller firms have developed generative AI models.[3][11][12]

# Generative AI has uses across a wide range of industries, including software development, healthcare, finance, entertainment, customer service,[13] sales and marketing,[14] art, writing,[15] fashion,[16] and product design.[17] However, concerns have been raised about the potential misuse of generative AI such as cybercrime, the use of fake news or deepfakes to deceive or manipulate people, and the mass replacement of human jobs."""]

def context_gen():
    url = "https://public-api.wordpress.com/rest/v1/sites/175179695/posts/"
    reponse = requests.get(url=url)
    if reponse.status_code==200:
        data = reponse.json()['posts']
    posts = [f"post id:{post['ID']}, site_id:{post['site_ID']}, title:{post['title']}, content:{post['content']}" for post in data]
    return posts

messages = []
def setup_rag_pipeline(context: list):
    rag.load_env_variables()
    docs = rag.preprocessing(context=context)
    retriever = rag.vector_conversion_retrieval(documents=docs)
    rag_chain = rag.rag_chaining(retriever=retriever)
    # print(rag.result(chain=rag_chain,query=query))
    return rag_chain

@app.route('/',methods=['GET'])
def temp():
    note_message ={'sender': "Note","content":"Please refer the 'https://public-api.wordpress.com/rest/v1/sites/175179695/posts/' api."}
    return render_template('index.html',messages=note_message)

@app.route('/send', methods=['POST'])
def get_rag_reponse():
    start = time.time()
    user_input = request.json.get('user_input')
    print("input:",user_input)
    context = context_gen()
    print("content generated....")
    rag.load_env_variables()
    docs = rag.preprocessing(context=context)
    retriever = rag.vector_conversion_retrieval(documents=docs)
    rag_chain = rag.rag_chaining(retriever=retriever)
    rag_response = rag.result(chain=rag_chain,query=user_input)
    print("result Genaration is complete...")
    if user_input:
        messages.append({'sender': 'User', 'content': user_input})
        end_response = {'sender': 'Bot', 'content': rag_response}
        messages.append(end_response)
    print(end_response)
    print("**********Total time taken : ",time.time()-start)
    return jsonify(end_response)


if __name__=="__main__":
    # ragchain=setup_rag_pipeline(context=context_gen())
    app.run()
    # print(context_gen())
    # query = "tell me the post id of Six on Saturday:  Opportunities for Change title"
    

    # print(rag.result(ragchain,query=query))
