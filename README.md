# Mini-Project-1

## Installation & Running Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/AI-Projects-COMP-472/Mini-Project-1.git
cd Mini-Project-1
```

### 2. Create a Virtual Environment (Recommended)

```sh
# Unix/macOS
python3 -m venv venv
# Activate the virtual environment
source venv/bin/activate
# Deactivate the virtual environment
deactivate

# Windows
python -m venv venv
# Activate the virtual environment
venv\Scripts\activate
# Deactivate the virtual environment
deactivate
```

### 3. Install Dependencies

Make sure you have `pip` upgraded:

```sh
pip install --upgrade pip
```

Then install all required Python packages:

```sh
pip install -r requirements.txt
```

*This will automatically install the core libraries, including Hugging Face transformers, torch, pandas, and more.*

### 4. Prepare the Knowledge Base

Ensure the `data/knowledge_base.csv` file exists and is properly formatted (see sample in this repo).

### 5. Run the Assistant

From the root of the repository, start the terminal chatbot:
***Safer and Preferred***
```sh
python -m assistant.main
```

Or if your entry point is elsewhere, adjust accordingly:

```sh
python assistant/main.py
```

### 6. Usage

- Type your questions at the prompt.
- To exit, type: `quit`

---

#### **Troubleshooting**

- If you see errors about missing packages, double-check that your virtual environment is activated and that all dependencies are installed.
- On first run, Hugging Face may download pre-trained model weights. Ensure your internet connection is active.
- If running on Windows and you see errors running scripts, try using `python` instead of `python3`, and activate your venv as shown above.
- If you ever see ImportError: attempted relative import with no known parent package, it's because you launched with python assistant/main.py instead of the -m module form.

---

### **Dependencies**
See [`requirements.txt`](requirements.txt) for the full list.

---