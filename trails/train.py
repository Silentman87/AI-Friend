import torch
from datasets import load_dataset, Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, TrainingArguments, Trainer, DataCollatorForSeq2Seq
from peft import LoraConfig, get_peft_model
import pandas as pd
import numpy as np


# Load dataset (replace with your dataset)
dataset = load_dataset('csv', data_files="dataset\merged_dataset.csv")

dataset = dataset["train"].train_test_split(test_size=0.2)


# Load tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Tokenization function
def preprocess_function(examples):
    inputs = examples["input_text"]
    targets = examples["target_text"]
    
    # Tokenize inputs and targets
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=512, truncation=True, padding="max_length").input_ids
    
    # T5 requires shifting decoder input IDs
    model_inputs["labels"] = labels
    model_inputs["decoder_input_ids"] = tokenizer(inputs, max_length=512, truncation=True, padding="max_length").input_ids
    
    return model_inputs

# Apply tokenization
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Convert dataset to PyTorch tensors
def format_dataset(example):
    return {
        "input_ids": torch.tensor(example["input_ids"], dtype=torch.long),
        "attention_mask": torch.tensor(example["attention_mask"], dtype=torch.long),
        "labels": torch.tensor(example["labels"], dtype=torch.long),
        "decoder_input_ids": torch.tensor(example["decoder_input_ids"], dtype=torch.long)
    }

tokenized_datasets = tokenized_datasets.map(format_dataset)

# Load model
base_model = T5ForConditionalGeneration.from_pretrained("t5-small")

# LoRA configuration
lora_config = LoraConfig(
    r=8, lora_alpha=16, target_modules=["q", "v"], lora_dropout=0.05, bias="none"
)

# Apply LoRA to the model
model = get_peft_model(base_model, lora_config)

# Training arguments
training_args = TrainingArguments(
    output_dir="./t5_lora_finetuned",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=2,  # Adjust based on your GPU
    per_device_eval_batch_size=2,
    learning_rate=3e-4,
    weight_decay=0.01,
    num_train_epochs=3,  # Adjust as needed
    save_total_limit=2,
    fp16=torch.cuda.is_available(),
    push_to_hub=False
)

# Data collator for sequence-to-sequence models
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Train the model
trainer.train()

# Save the LoRA adapter
model.save_pretrained("./t5_lora_adapter")
print("Training complete! Model saved.")


# Define local path where you extracted the model
local_model_path = r"C:\Users\HP\AIFriend\t5_spiritual_guru"

# Load model and tokenizer
tokenizer = T5Tokenizer.from_pretrained(local_model_path)
model = T5ForConditionalGeneration.from_pretrained(local_model_path)

model.eval()


def generate_response(input_text, max_length=100):
    # Tokenize input
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    
    # Generate output
    output_ids = model.generate(input_ids, max_length=max_length)
    
    # Decode and return response
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)



# Example 1: Spiritual Guidance
input_text = "What does the Bhagavad Gita say about inner peace?"
response = generate_response(input_text)
print("Model Response:", response)

# Example 2: Emotional Support
input_text = "Provide a motivational quote about forgiveness"
response = generate_response(input_text)
print("Model Response:", response)

# Example 3: Wellness Suggestion
input_text = "How can I improve my mental well-being?"
response = generate_response(input_text)
print("Model Response:", response)




device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_response(input_text, max_length=150):
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

    output_ids = model.generate(
        input_ids,
        max_length=max_length,
        do_sample=True,  # Enables randomness
        top_k=50,        # Consider top 50 words instead of just the best
        top_p=0.9,       # Uses nucleus sampling (top 90% probability mass)
        temperature=0.8,  # Introduces more variety (0.8 - 1.2 recommended)
        repetition_penalty=1.8,  # Reduces repetitive phrases
        num_return_sequences=1  # Generates a single response
    )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# Test Case
input_text = "i used to scare for darkness"
response = generate_response(input_text)
print("Model Response:", response)





def calculate_perplexity(model, tokenizer, test_texts):
    model.eval()
    total_ppl = []
    
    for text in test_texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)  # Ensure correct device
        with torch.no_grad():
            outputs = model(**inputs, labels=inputs["input_ids"])
            loss = outputs.loss
            ppl = torch.exp(loss).item()
            total_ppl.append(ppl)

    avg_ppl = np.mean(total_ppl)
    print(f"Perplexity Score: {avg_ppl:.2f}")  # Lower is better
    return avg_ppl

# Example Test Sentences
test_sentences = [
    "How can I stay motivated during tough times?",
    "I feel really down today. What should I do?",
    "Can you give me some wellness tips?"
]

calculate_perplexity(model, tokenizer, test_sentences)





from nltk.translate.bleu_score import sentence_bleu,SmoothingFunction,corpus_bleu

def evaluate_bleu_score(model, tokenizer, test_data):
    scores = []
    for input_text, expected_output in test_data:
        response = generate_response(input_text)  # Your model's response function
        reference = [expected_output.split()]  # Tokenized expected output
        candidate = response.split()  # Tokenized generated response
        print(response)
        score = sentence_bleu(reference, candidate)  # Compute BLEU score
        scores.append(score)
    
    avg_bleu = np.mean(scores)
    print(f"BLEU Score: {avg_bleu:.2f}")  # Closer to 1 is better
    return avg_bleu

# Example Test Data
test_data = [
    ("How can I stay motivated?", "Stay focused on your goals and keep pushing forward."),
    ("I feel anxious today.", "Try deep breathing and a short walk to calm your mind.")
]

evaluate_bleu_score(model, tokenizer, test_data)


reference_texts = "Stay focused on your goals and keep pushing forward."
generated_texts = "I'll leave you motivated once a week."

smoothing = SmoothingFunction().method1  # Method1 helps in low-overlap cases
bleu_score = corpus_bleu(reference_texts, generated_texts, smoothing_function=smoothing)
print("BLEU Score:", bleu_score)


from rouge_score import rouge_scorer
scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
scores = [scorer.score(ref, gen) for ref, gen in zip(reference_texts, generated_texts)]
print("ROUGE-L Score:", scores)