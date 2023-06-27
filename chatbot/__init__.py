"""chatbot module
You can implement your chatbot module here.

You will have considerable freedom when implementing this. The code below is
only meant to only be one possible starter. Feel free to redo this in a way
you think is fit.
"""
import sys
sys.path.append("..")
from keys import NEWS_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID, WOLFRAM_ALPHA_APPID, WEATHER_API_KEY
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.agents import Tool


TEMPLATE = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

TOOLS:
------
- Wikipedia
- Math
- Python REPL
- Wolfram Alpha
- Terminal
- News API
- OpenWeatherMap API
- UW CSE Lookup


To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When using the CSE Lookup tool, respond with the first result you receive from the tool. Do not use Google Search or Wikipedia to answer questions about the CSE course catalog.

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
{ai_prefix}: [your response here]
```

SUFFIX = Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}"""

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectordb = Chroma(persist_directory='rtdocs-vectordb',
                  embedding_function=embeddings)

# IMPORTANT
# search_type "mmr" or "similarity", where mmr aims for both relevance and diversity
# k is the number of results to return, the more results we return the better the extraction between vectors, but we take a hit to performance especially when using map_reduce chain_type
retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 12}) 

# IMPORTANT
# map_reduce passes the inital prompt to each vector chunk that the retriever retrieves. it then aggregates the responses from each chunk and passes those back to itself to generate a final response
# there are other chain_types, but map_reduce is the most accurate for our use case, please see final report for more details
qa_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0),
                                       chain_type="map_reduce",
                                       retriever=retriever,
                                       return_source_documents=False) #if you set to true, you will need to change the Tool to use qa.predict instead and parse the args 

class Chatbot:
    def __init__(self, template=TEMPLATE, qa_chain=qa_chain):
        self.template = template
        self.prompt = PromptTemplate(
            input_variables=["tool_names", "ai_prefix",
                             "chat_history", "agent_scratchpad", "input"],
            template=self.template)
        self.memory = ConversationBufferMemory()
        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0,
            model_name='gpt-3.5-turbo')
        self.tools = load_tools([
            'wikipedia',
            'llm-math',
            'python_repl',
            'wolfram-alpha',
            'terminal',
            'news-api',
            'openweathermap-api'
        ],
            llm=self.llm,
            news_api_key=NEWS_API_KEY,
            openweathermap_api_key=WEATHER_API_KEY,
            wolfram_alpha_appid=WOLFRAM_ALPHA_APPID,
            google_cse_id=GOOGLE_CSE_ID,
            google_api_key=GOOGLE_API_KEY)
        # load_tools() is not compatible with custom tools
        self.tools = self.tools + [Tool(
                name="UW CSE Lookup",
                func=qa_chain.run,
                description=("use this tool when you need to answer questions "
                             "about the UW CSE course catalog "
                             "or CSE courses in general "
                             "input should be a fully formed question"),
                return_direct=True # add return_direct=True if you want to return the Tool response rather than the agent response
            )]
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            prompt=self.prompt)

    def respond(self, user_prompt):
        return self.agent.run(input=user_prompt)
