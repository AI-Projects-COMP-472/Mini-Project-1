# COMP 472 Mini Project 1: Student Support AI Assistant

This project is an AI-powered student support assistant for COMP 472. It answers student questions from a CSV knowledge base, detects sentiment, recommends escalation for strongly negative messages, and uses sentence embeddings with semantic search to retrieve the closest answer.

## Features

- Loads a `data/knowledge_base.csv` file with `question,answer` columns
- Uses `pandas` for CSV loading
- Uses `sentence-transformers` to generate sentence embeddings
- Uses `scikit-learn` cosine similarity for semantic search
- Uses Hugging Face `transformers` sentiment analysis
- Displays sentiment label and confidence score for every message
- Recommends human escalation for strongly negative messages
- Maintains basic conversation history and session statistics
- Class-based structure that can be reused later in a GUI

## Project structure

```text
comp472_student_support_ai/
├── assistant/
│   ├── __init__.py
│   ├── config.py
│   ├── escalation.py
│   ├── knowledge_base.py
│   ├── models.py
│   ├── semantic_search.py
│   ├── sentiment.py
│   └── support_assistant.py
├── tests/
│   ├── test_conversation.py
│   ├── test_knowledge_base.py
│   ├── test_semantic_search.py
│   └── test_sentiment.py
├── gui/
│   └── app.py
├── data/
│   └── knowledge_base.csv
├── main.py
├── short_reflection.txt
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup in VS Code

Open the project folder in VS Code, then run these commands in the terminal.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The first run may take longer because Hugging Face models need to download.

## How it works

### Embeddings

An embedding is a numerical representation of text. The sentence-transformer model converts every knowledge base question into a vector. Similar questions should have similar vectors.

### Semantic search

When the user asks a question, the program converts that question into an embedding too. It compares the user question embedding against all stored question embeddings using cosine similarity. The closest stored question is selected, and the matching answer is returned.

### Sentiment analysis

The program uses a Hugging Face sentiment-analysis pipeline to classify each user message as positive, neutral, or negative. If the user message is negative with confidence above the escalation threshold, the assistant recommends contacting a human advisor.

## Optional GUI

The project also includes a simple Tkinter GUI for demo purposes. It uses the same assistant classes as the command-line version.

Run it from the project folder:

```bash
python gui/app.py
```

The first launch may take a moment while the embedding and sentiment models load.

## Example run

```text
Loading Student Support AI...
Welcome to Student Support AI
Type 'quit' to exit.

You: I cannot access my account and this is terrible
Sentiment: NEGATIVE (0.99)
Recommended escalation: Contact human advisor.
Match confidence: 0.73
Answer: Visit the IT Service Desk portal and select the password reset option. Follow the instructions sent to your registered email.

You: Where is the registrar office?
Sentiment: NEUTRAL (0.91)
Match confidence: 0.94
Answer: The registrar office is located in the main administration building. You can also contact the office through the student service centre.
```

## Test questions

Try these:

```text
How do I reset my password?
Where is the registrar office?
I am extremely frustrated with tuition payment.
How do I access Moodle?
How do I drop a class?
Where is my exam schedule?
```

## Running the basic test

```bash
python -m pytest
```

The included tests check the CSV structure and the assistant components. They use fake model objects for component tests, so they do not download AI models during testing.

## Demo explanation

During the demo, be ready to explain:

1. The CSV is loaded using pandas.
2. Stored questions are converted into embeddings using SentenceTransformer.
3. The user's message is converted into another embedding.
4. Cosine similarity finds the closest question.
5. Transformers pipeline detects sentiment.
6. Strongly negative messages trigger human escalation.
7. The conversation loop continues until the user types `quit`.
