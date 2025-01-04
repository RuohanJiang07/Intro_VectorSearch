import os
import tiktoken
import pandas as pd

# 🛠️ Setup file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(current_dir, 'expert_profiles_all.csv')
output_file_path = os.path.join(current_dir, 'chunked_expert_profiles.csv')

# 📝 Load your data
try:
    df = pd.read_csv(input_file_path)
    print(f"✅ Loaded data from '{input_file_path}'")
except FileNotFoundError:
    raise FileNotFoundError(f"❌ The file '{input_file_path}' was not found. Please check the path.")

# 🎯 Initialize the OpenAI tokenizer
try:
    tokenizer = tiktoken.get_encoding("cl100k_base")  # Common tokenizer for OpenAI embeddings
    print("✅ Tokenizer initialized successfully.")
except Exception as e:
    raise RuntimeError(f"❌ Error initializing tokenizer: {e}")

# 📚 Function to chunk text
def chunk_text(text, max_tokens=100, overlap=10):
    """
    Splits text into smaller chunks with a specified maximum number of tokens,
    ensuring a small overlap between chunks.
    
    Args:
        text (str): The input text to chunk.
        max_tokens (int): Maximum tokens per chunk (smaller for finer granularity).
        overlap (int): Number of overlapping tokens between chunks.
    
    Returns:
        List of text chunks.
    """
    if not text.strip():
        return []  # Handle empty or whitespace-only text
    
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens - overlap):
        chunk = tokens[i:i + max_tokens]
        chunks.append(tokenizer.decode(chunk))
    return chunks

# 🧠 Apply chunking to the 'profile' column
if 'profile' not in df.columns:
    raise KeyError("❌ The column 'profile' does not exist in the input CSV file.")

df['profile'] = df['profile'].fillna('')  # Ensure no NaN values
df['Profile_Chunks'] = df['profile'].apply(lambda x: chunk_text(str(x)))

# 🔄 Flatten the chunks into a new DataFrame
chunked_profiles = []
for index, row in df.iterrows():
    for chunk in row['Profile_Chunks']:
        chunked_profiles.append({
            'Name': row['name'] if 'name' in row else "N/A",
            'Category': row['category'] if 'category' in row else "N/A",
            'Label': row['label'] if 'label' in row else "N/A",
            'Profile_Chunk': chunk
        })

# 💾 Save the chunked data to a new CSV file
chunked_df = pd.DataFrame(chunked_profiles)
try:
    chunked_df.to_csv(output_file_path, index=False)
    print(f"🎉 Chunking complete! Saved as '{output_file_path}'")
except Exception as e:
    raise RuntimeError(f"❌ Error saving chunked data: {e}")
