#############################################################################
#                      AI-Friend | Ai-powered health &                      #
#                          emotional support chatbot                        #
#                                                                           #
#                                                                           #             
#                                                                           #
#                    ------For Research Purpose------                       #
#############################################################################


#############################################################################
#  Importing library
#
#############################################################################


from transformers import T5ForConditionalGeneration, T5Tokenizer, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import Dataset, load_dataset
from peft import LoraConfig, get_peft_model
import pandas as pd
import nltk
nltk.download('averaged_perceptron_tagger_eng')

# 1. Load your local CSV file
csv_path = r"C:\Users\HP\AIFriend\dataset\dailydialogue_cleaned.csv"  # Replace with your actual path
df = pd.read_csv(csv_path)

# Convert to Hugging Face Dataset format
dataset = Dataset.from_pandas(df)

# 2. Load Model and Tokenizer
model_name = r"C:\Users\HP\AIFriend\t5_spiritual_guru"  # or your existing fine-tuned model
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# 3. Preprocess Data (adjust column names as needed)
def preprocess_function(examples):
    inputs = ["empathetic response: " + text for text in examples["input"]]  # Replace "input_text"
    targets = examples["response"]  # Replace "target_text"
    
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length").input_ids
    model_inputs["labels"] = labels
    return model_inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# 4. Configure LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q", "v"],
    lora_dropout=0.05,
    bias="none",
    task_type="SEQ_2_SEQ_LM"
)
model = get_peft_model(model, lora_config)

# 5. Training Setup
training_args = Seq2SeqTrainingArguments(
    output_dir="./t5_dailydialogue_lora",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    learning_rate=3e-4,
    fp16=True,
    save_strategy="epoch",
    logging_steps=100,
    predict_with_generate=True,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
)

# 6. Start Training
trainer.train()

# 7. Save Model
model.save_pretrained("./t5_dailydialogue_lora")




import torch
import nlpaug.augmenter.word as naw
from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
from peft import LoraConfig, get_peft_model


def augment_text(text, n=3):
    """Performs text augmentation using paraphrasing."""
    aug = naw.SynonymAug(aug_src='wordnet')  # Synonym-based augmentation
    augmented_texts = [aug.augment(text)[0] for _ in range(n)]  # Extract first element
    return list(set(augmented_texts))  # Remove duplicates


# Load dataset (Replace 'your_dataset.csv' with actual path)
dataset = load_dataset("csv", data_files="dataset\dailydialogue_cleaned.csv")


augmented_data = []
for item in dataset["train"]:  # Assuming single split
    context = item["input"]
    response = item["response"]
    new_contexts = augment_text(context, n=2)
    new_responses = augment_text(response, n=2)
    
    # Add original and augmented data
    augmented_data.append({"input": context, "response": response})
    for ctx, res in zip(new_contexts, new_responses):
        augmented_data.append({"input": ctx, "response": res})

# Convert back to Hugging Face Dataset
dataset = dataset["train"].from_list(augmented_data)

tokenizer = T5Tokenizer.from_pretrained("t5_spiritual_guru")

def preprocess(example):
    """Tokenize input context and response."""
    inputs = tokenizer(example["input"], padding="max_length", truncation=True, max_length=128)
    targets = tokenizer(example["response"], padding="max_length", truncation=True, max_length=128)
    inputs["labels"] = targets["input_ids"]
    return inputs

dataset = dataset.map(preprocess, batched=True)


# -------------------- 🔹 LoRA Configuration -------------------- #
lora_config = LoraConfig(
    r=32,  # Higher rank for better learning
    lora_alpha=64,  # Larger scaling factor
    lora_dropout=0.1,  # Prevent overfitting
    target_modules=["q", "v"],  # Fine-tuning attention layers
)


# Load model with LoRA
model = T5ForConditionalGeneration.from_pretrained("t5_spiritual_guru")
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()



training_args = Seq2SeqTrainingArguments(
    output_dir="./t5_dailydialogue_lora",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    save_strategy="epoch",
    logging_steps=100,
    predict_with_generate=True,
    report_to="none"
)


trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer
)


# 6. Start Training
trainer.train()