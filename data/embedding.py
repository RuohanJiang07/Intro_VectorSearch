import openai
import pandas as pd
import os
import json

# 🛡️ Set OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# If the API key isn't set in the environment, manually add it here (not recommended)
if not openai.api_key:
    openai.api_key = 'api-key-here'

# 📊 File Paths
input_csv = os.path.join(os.path.dirname(__file__), 'chunked_expert_profiles.csv')
output_csv = os.path.join(os.path.dirname(__file__), 'embedded_expert_profiles_with_labels.csv')

# 📈 OpenAI Embedding Model (Latest Version)
EMBEDDING_MODEL = "text-embedding-3-small"

def get_openai_embedding(text):
    """
    Fetch embedding for a given text using OpenAI's API.
    
    Args:
        text (str): The input text to embed.
    
    Returns:
        list: Embedding vector or None if an error occurs.
    """
    try:
        response = openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
            encoding_format="float"
        )
        return response.data[0].embedding
    except openai.OpenAIError as e:
        print(f"❌ Error generating embedding: {e}")
        return None

# 🚀 Load CSV Data
df = pd.read_csv(input_csv)

# Ensure the expected columns exist
required_columns = ['Name', 'Category', 'Label', 'Profile_Chunk']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"❌ CSV file must contain the following columns: {required_columns}")

# Add new columns for embeddings
df['Profile_Embedding'] = None
df['Label_Embedding'] = None

# ⚙️ Generate Embeddings for Profile Chunks and Labels
for index, row in df.iterrows():
    # Embed Profile Chunk
    profile_text = row['Profile_Chunk']
    if pd.isna(profile_text) or profile_text.strip() == '':
        print(f"⚠️ Skipping empty profile chunk at index {index}")
    else:
        print(f"📝 Generating embedding for profile chunk at index {index}, Name: {row['Name']}")
        profile_embedding = get_openai_embedding(profile_text)
        if profile_embedding is not None:
            df.at[index, 'Profile_Embedding'] = json.dumps(profile_embedding)  # Store embedding as JSON string
    
    # Embed Label
    label_text = row['Label']
    if pd.isna(label_text) or label_text.strip() == '':
        print(f"⚠️ Skipping empty label at index {index}")
    else:
        print(f"🏷️ Generating embedding for label at index {index}, Label: {row['Label']}")
        label_embedding = get_openai_embedding(label_text)
        if label_embedding is not None:
            df.at[index, 'Label_Embedding'] = json.dumps(label_embedding)  # Store embedding as JSON string

# 💾 Save the Updated DataFrame to a New CSV
df.to_csv(output_csv, index=False)
print(f"\n✅ Embeddings for Profile Chunks and Labels have been added and saved to '{output_csv}'")
