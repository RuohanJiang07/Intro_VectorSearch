import os
import pandas as pd
import openai
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
embedded_profiles_path = os.path.join(project_root, 'data', 'embedded_expert_profiles.csv')
expert_profiles_path = os.path.join(project_root, 'data', 'expert_profiles_all.csv')

os.environ['OPENAI_API_KEY'] = 'put-api-key-here'
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("❌ OPENAI_API_KEY environment variable not set. Please set it before running the script.")

try:
    df = pd.read_csv(embedded_profiles_path)
    print(f"✅ Loaded embedded data from '{embedded_profiles_path}'")

    expert_df = pd.read_csv(expert_profiles_path)
    print(f"✅ Loaded expert profiles from '{expert_profiles_path}'")

    name_to_url = dict(zip(expert_df['name'], expert_df['url']))
except FileNotFoundError as e:
    raise FileNotFoundError(f"❌ File not found: {str(e)}")

df['Embedding'] = df['Embedding'].apply(json.loads)

def get_query_embedding(query, model="text-embedding-3-small"):
    try:
        response = openai.embeddings.create(
            model=model,
            input=query
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        return None

def fetch_full_profile(expert_name):
    """
    Fetch the full profile of an expert by their name.
    """
    try:
        expert_row = expert_df.loc[expert_df['name'] == expert_name].iloc[0]
        return expert_row['profile'], expert_row['label']
    except IndexError:
        print(f"⚠️ Full profile not found for expert: {expert_name}")
        return "", ""


def generate_explanation(name, label, profile, query, model="gpt-4"):
    """Generate an AI explanation for why the expert matches the query."""
    prompt = f"""
    You are an assistant tasked with explaining why an expert matches a user's query. 
    The user's query is: "{query}"
    The expert's name is: "{name}"
    The expert's label is: "{label}"
    The expert's profile is: "{profile}"

    Provide a concise explanation (2-3 sentences) of why this expert matches the query.
    Start directly into the main explanation, which means you don't have to say 'Someone is a suitable match for the user's query on something because'. Don't waste your words.
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI assistant that explains search results."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error generating explanation: {e}")
        return "An explanation could not be generated for this expert."

def schematic_search(query, top_n=6):
    print("Generating query embedding...")
    query_embedding = get_query_embedding(query)
    if not query_embedding:
        print("❌ Failed to generate query embedding.")
        return pd.DataFrame()

    query_embedding = np.array(query_embedding).reshape(1, -1)
    profile_embeddings = np.vstack(df['Embedding'].values)

    print("🔍 Calculating cosine similarity...")
    similarities = cosine_similarity(query_embedding, profile_embeddings)[0]

    df['Similarity'] = similarities

    sorted_df = df.sort_values(by='Similarity', ascending=False)

    combined_results = {}
    unique_experts = 0
    index = 0

    while unique_experts < top_n and index < len(sorted_df):
        row = sorted_df.iloc[index]
        name = row['Name']

        if name not in combined_results:
            expert_info = expert_df[expert_df['name'] == name].iloc[0]
            full_profile = expert_info['profile']
            label = expert_info['label']

            explanation = generate_explanation(name, label, full_profile, query)

            combined_results[name] = {
                'Name': name,
                'Category': row['Category'],
                'Label': label,
                'Explanation': explanation,
                'Similarity': row['Similarity'],
                'url': name_to_url.get(name, '')
            }
            unique_experts += 1
        else:
            print(f"⚠️ Duplicate expert '{name}' found. Skipping duplicate profile snippet.")

        index += 1

    unique_results = sorted(combined_results.values(), key=lambda x: x['Similarity'], reverse=True)[:top_n]

    return pd.DataFrame(unique_results)

if __name__ == "__main__":
    user_query = input("🔎 Enter your query: ")
    results = schematic_search(user_query)

    if not results.empty:
        print("\n🎯 Top Matching Results:")
        for i, row in results.iterrows():
            print(f"\n➡️ Name: {row['Name']}")
            print(f"   Category: {row['Category']}")
            print(f"   Label: {row['Label']}")
            print(f"   URL: {row['url']}")
            print(f"   Match Score: {row['Similarity']:.4f}")
            print(f"   Profile Snippet: {row['Profile_Chunk']}")
    else:
        print("⚠️ No results found.")