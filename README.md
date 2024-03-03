# Retrieval Augmented Generation
Retrieval-augmented generation (RAG) is a natural language processing (NLP) approach that combines elements of both retrieval and generation models to improve the performance of various language tasks. In the context of information retrieval, RAG models aim to effectively retrieve relevant information from a large dataset or knowledge base and then generate a response based on that retrieved information.

This project uses the Langchain RetrievalQA, OpenAI GPT-3.5 Turbo, and ChromaDB to build a RAG application over the course catalog for the University of Washington Computer Science and Engineering. The catalog is converted to embeddings and the vectors are saved to disk, where they can be loaded and queried against. 

Running this project requries the use of an OpenAI API key. 


# How to use this repository

Below are file descriptions for the new/significant files in alphabetical order to guide you on the layout of this repository.

## `chatbot/__init__.py`
This Python script contains the fully defined version of the chatbot with all tooling incorportated. It returns chat responses to `api.py`. 

## `FINAL_DEMO.ipynb`
This notebook is used for the video recording demonstration. [Link to video here](https://youtu.be/7VOPEAVuTtM)

## `FINAL_REPORT.pdf`
This contains an explanation of the concepts used in Langchain and an evaluation of the overall approach.

## `rtdocs-create.ipynb`
This notebook is used to download the UW Course Catalog, parse it, and save its embeddings to a vector database on disk.

## `rtdocs-query.ipynb`
This notebook is used to load the vector database from disk and query against it. It also includes a bunch of sample queries for the UW CSE Lookup Tool.
