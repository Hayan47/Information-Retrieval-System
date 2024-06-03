# Information Retrieval System

This is an information retrieval system built with Python Django using a Service Oriented Architecture. It uses PostgreSQL as the database backend and Tailwind CSS for styling.

## Project Structure

The project is structured as follows:

- `IR` contains the main Django project. This directory includes settings, URLs, and other configurations for the entire project. It serves as the central hub for managing the information retrieval system.

- `ir_controller` contains the service responsible for controlling the main project and connecting to the remaining services. It handles communication between different components of the system and ensures smooth operation of the information retrieval system.

Additional directories represent individual services within the system. Each service is responsible for specific functionality and communicates with other services via APIs using Django REST Framework.

services are designed to be modular and communicate with each other via RESTful APIs, allowing for scalability, flexibility, and easy integration of new features or services.

## Features

- Service Oriented Architecture
- PostgreSQL database
- Tailwind CSS for styling
- Word Embedding using Word2Vec
- BM25 Ranking
- LDA Model for Topic Detection

## Techniques Used

### Word Embedding using Word2Vec

Word2Vec is a popular technique for generating word embeddings, which are dense vector representations of words in a high-dimensional space. These embeddings capture semantic similarities between words based on their context in a large corpus of text. In this project, Word2Vec was used to convert words into fixed-length vectors, which were then used as features for various tasks such as semantic similarity, information retrieval, and natural language processing.

### BM25 Ranking

BM25 (Best Matching 25) is a ranking function used for information retrieval. It is an improved version of the TF-IDF (Term Frequency-Inverse Document Frequency) weighting scheme that takes into account the length of the document and the average length of documents in the corpus. BM25 assigns higher weights to terms that appear infrequently in the corpus and have high discriminative power for a given query. In this project, BM25 was used to rank documents based on their relevance to user queries in the information retrieval system.

### LDA Model for Topic Detection

Latent Dirichlet Allocation (LDA) is a generative probabilistic model used for topic modeling in text corpora. It represents documents as mixtures of topics, where each topic is characterized by a distribution over words. LDA is used to discover the underlying topics in a collection of documents and assign each document a distribution over these topics. In this project, LDA was used for topic detection to categorize documents into different topics and facilitate better organization and retrieval of information.

## Requirements

- Python 3.x
- PostgreSQL
- Node.js and npm (for Tailwind CSS)

## Installation

### Clone the Repository

```sh
git clone https://github.com/Hayan47/Information-Retrieval-System
cd yourproject
```

### Set Up Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```sh
pip install -r requirements.txt
```
### Create Database

install PostgreSQL from [this link](https://www.postgresql.org/download/). After installing PostgreSQL, create a database called `mydatabase`, user `postgres`, password `admin` on port `5432`.

### Apply Migrations

```sh
python manage.py migrate
```

### Run the Server

```sh
python manage.py runserver
```
## Testing the Project

### Download Dataset

First, download the dataset, queries, and qrels from the following links and place them in the `IR/static/datasets` directory:

- antique: [Dataset Link](#https://drive.google.com/file/d/1-AIadRgLg7R90Ux3mMlgEkZC4frVQNvZ/view?usp=drive_link), [Queries Link](#https://drive.google.com/file/d/1YioflSePeYxASSh8ymBnegfYWU17Fpj1/view?usp=drive_link), [Qrels Link](#https://drive.google.com/file/d/112DCVc-HTgaNEXDwA2M9lnkYoW6Q18pF/view?usp=drive_link)

- lotte science: [Dataset Link](#https://drive.google.com/file/d/1-0FKzfZJ2GDwupJFLzVNzftwLunGP8OQ/view?usp=drive_link), [Queries Link](#https://drive.google.com/file/d/1KQS2Mf9Adp8nRrGL1ybezpcRlc3PFaaJ/view?usp=drive_link), [Qrels Link](#https://drive.google.com/file/d/1jFiRbouy5rIJ8DJfpSoFxdgljNjrXG6a/view?usp=drive_link)

Ensure that the directory structure looks like this:

```
IR/
└── static/
└── datasets/
    ├── {dataset_name}.tsv
    ├── {dataset_name}_queries.csv
    └── {dataset_name}_qrels.csv
```
### Contributing

Feel free to submit issues, fork the repository and send pull requests!
