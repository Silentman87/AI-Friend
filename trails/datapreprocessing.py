#############################################################################
#                      AI-Friend | Ai-powered health &                      #
#                          emotional support chatbot                        #
#                                                                           #
#                                                                           #             
#                                                                           #
#                    ------For Research Purpose------                       #
#############################################################################



import pandas as pd
import re
import spacy
from nltk.tokenize import word_tokenize
import ast
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string


import nltk
nltk.download('punkt_tab')  # For tokenization
nltk.download('stopwords')  # For stop words
nltk.download('wordnet')  # For lemmatization
nltk.download('omw-1.4')  # For wordnet support

# Initialize tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))



# Load English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("mental_health_counseling.csv")

df.info()

# Function to clean and lemmatize text
def preprocess_text(text):
    text = text.lower().strip()  # Lowercase & trim spaces
    text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Lemmatization
    doc = nlp(" ".join(tokens))
    lemmatized_text = " ".join([token.lemma_ for token in doc])

    return lemmatized_text

# Apply preprocessing

df["Context"] = df["Context"].apply(preprocess_text)
df["Response"] = df["Response"].apply(preprocess_text)

# Save preprocessed data
df.to_csv("final_preprocessed_mental_health_data.csv", index=False)

print("✅ Preprocessing complete! Cleaned dataset saved as 'final_preprocessed_mental_health_data.csv'")



df = pd.read_csv("daily_dialog_train.csv")
df.head()

# Define act and emotion label mappings
act_label = {
    0: "__dummy__",  
    1: "inform",
    2: "question",
    3: "directive",
    4: "commissive",
}

emotion_label = {
    0: "no emotion",
    1: "anger",
    2: "disgust",
    3: "fear",
    4: "happiness",
    5: "sadness",
    6: "surprise",
}

# Create a new dataframe to store the processed data
processed_data = []

for index, row in df.iterrows():
    # Convert text representation of lists to actual lists
    dialogues = ast.literal_eval(row["dialog"])
    acts = ast.literal_eval(row["act"])
    emotions = ast.literal_eval(row["emotion"])

    # Ensure all lists have the same length
    assert len(dialogues) == len(acts) == len(emotions), f"Mismatch at index {index}"

    # Expand rows
    for i in range(len(dialogues)):
        processed_data.append({
            "utterance": dialogues[i].strip(),
            "act": act_label[acts[i]],
            "emotion": emotion_label[emotions[i]] 
        })

# Convert processed data into a new dataframe
df_processed = pd.DataFrame(processed_data)

# Save to a new CSV file
df_processed.to_csv("processed_daily_dialogue.csv", index=False)

print("✅ Preprocessing completed! File saved as 'processed_daily_dialogue.csv'.")


# Function to clean text
def clean_text(text):
    text = text.lower().strip()  # Lowercase
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"\d+", "", text)  # Remove numbers
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    words = word_tokenize(text)  # Tokenize words
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]  # Lemmatization & stopword removal
    return " ".join(words)

df_processed["utterance"] = df_processed["utterance"].apply(clean_text)

df_processed.head()

df_processed.to_csv("final_dailydialogue.csv", index = False)



df = pd.read_csv("empathetic.csv") 

def clean_text(text):
    if isinstance(text, float):  # Handle NaN values
        return ""
    text = text.replace("_comma_", ",")  # Replace _comma_ with actual comma
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

# Clean text columns
df["context"] = df["context"].apply(clean_text)
df["prompt"] = df["prompt"].apply(clean_text)
df["utterance"] = df["utterance"].apply(clean_text)


#Create input-output pairs for T5

def format_input(row):
    return f"Context: {row['context']} Prompt: {row['prompt']}"

df["input_text"] = df.apply(format_input, axis=1)
df["target_text"] = df["utterance"]

# Drop unnecessary columns
df = df[["input_text", "target_text"]]

# Save preprocessed data
df.to_csv("preprocessed_empathetic.csv", index=False)
print("Preprocessing complete. Data saved!")



df = pd.read_csv("motivational-quotes.csv")

# Clean quotes by removing unnecessary symbols
df["quote"] = df["quote"].str.replace(r'“|”', '', regex=True).str.strip()
# Standardize author names
df["author"] = df["author"].str.strip()


# Prepare input-output pairs for T5
df["input_text"] = df["prompt"]
df["target_text"] = df["quote"]

# Save cleaned dataset
df[["input_text", "target_text"]].to_csv("cleaned_motivational_quotes.csv", index=False)

print("Preprocessing complete. Cleaned data saved!")



df = pd.read_csv("psychology-10k.csv")

# Remove duplicate entries (if any)
df = df.drop_duplicates()
# Clean input and output text
df["input"] = df["input"].str.strip().str.replace(r'"', '', regex=True)
df["output"] = df["output"].str.strip().str.replace(r'"', '', regex=True)

# Prepare for T5 fine-tuning
df.rename(columns={"input": "input_text", "output": "target_text"}, inplace=True)

# Save cleaned dataset
df[["input_text", "target_text"]].to_csv("cleaned_psychological_dataset.csv", index=False)

print("Preprocessing complete! Ready for T5 training.")



# Load the DailyDialogue dataset
df = pd.read_csv("raw_data\daily_dialog_train.csv")  # Update with actual file path

# Lists to store processed data
inputs = []
responses = []

# Iterate through each row and process dialogues
for _, row in df.iterrows():
    try:
        # Convert dialog string to list
        dialog = ast.literal_eval(row["dialog"])  # Convert string representation to list
        
        # Create input-response pairs
        for i in range(len(dialog) - 1):
            inputs.append(dialog[i].strip())
            responses.append(dialog[i + 1].strip())
    except Exception as e:
        print(f"Error processing row: {e}")

# Create a new DataFrame with input-response pairs
cleaned_df = pd.DataFrame({"input": inputs, "response": responses})

# Save as CSV
cleaned_df.to_csv("dailydialogue_cleaned.csv", index=False)

print("Preprocessing complete. CSV saved as 'dailydialogue_cleaned.csv'")
