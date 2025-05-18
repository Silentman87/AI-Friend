#############################################################################
#                      AI-Friend | Ai-powered health &                      #
#                          emotional support chatbot                        #
#                                                                           #
#                                                                           #             
#                                                                           #
#                    ------For Research Purpose------                       #
#############################################################################


from datasets import load_dataset
import pandas as pd

# Load the DailyDialog dataset
dataset = load_dataset("daily_dialog")

# Convert to DataFrame and save as CSV
for split in dataset.keys():
    df = pd.DataFrame(dataset[split])
    df.to_csv(f"daily_dialog_{split}.csv", index=False, encoding="utf-8")
    print(f"Saved {split} dataset as daily_dialog_{split}.csv")

print("Download completed!")




# Load the dataset
ds = load_dataset("Amod/mental_health_counseling_conversations")

# Convert the dataset to a DataFrame (assuming 'train' split)
df = pd.DataFrame(ds['train'])

# Save to CSV file
csv_filename = "mental_health_counseling.csv"
df.to_csv(csv_filename, index=False)

print(f"Dataset saved successfully as {csv_filename}!")




ds = load_dataset("samhog/psychology-10k")

# Convert the dataset to a DataFrame (assuming 'train' split)
df = pd.DataFrame(ds['train'])

# Save to CSV file
csv_filename = "psychology-10k.csv"
df.to_csv(csv_filename, index=False)

print(f"Dataset saved successfully as {csv_filename}!")



ds = load_dataset("asuender/motivational-quotes", "quotes_extended")

# Convert the dataset to a DataFrame (assuming 'train' split)
df = pd.DataFrame(ds['train'])

# Save to CSV file
csv_filename = "motivational-quotes.csv"
df.to_csv(csv_filename, index=False)

print(f"Dataset saved successfully as {csv_filename}!")



ds = load_dataset("facebook/empathetic_dialogues")

# Convert the dataset to a DataFrame (assuming 'train' split)
df = pd.DataFrame(ds['train'])

# Save to CSV file
csv_filename = "empathetic.csv"
df.to_csv(csv_filename, index=False)

print(f"Dataset saved successfully as {csv_filename}!")

df = pd.read_csv('C:/Users/HP/AIFriend/empathetic.csv')
df.sample(10)