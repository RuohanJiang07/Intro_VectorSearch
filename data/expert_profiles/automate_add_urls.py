import pandas as pd
import json
import os

def generate_url_from_name(name):
    """Generate the expected URL format from a name"""
    try:
        # Split name and capitalize each part
        name_parts = name.strip().split()
        # Join parts without spaces
        formatted_name = ''.join(part.capitalize() for part in name_parts)
        return f"https://intro.co/{formatted_name}?source=intro"
    except Exception as e:
        print(f"Error formatting name '{name}': {e}")
        return None

def match_urls_from_json():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define file paths
    csv_path = os.path.join(current_dir, 'expert_profiles_all.csv')
    json_path = os.path.join(current_dir, 'expert_urls.json')
    
    # Load the CSV file
    try:
        df = pd.read_csv(csv_path)
        print("Successfully loaded CSV file!")
        print(f"Total experts in CSV: {len(df)}")
    except FileNotFoundError:
        print(f"Error: Could not find the CSV file at {csv_path}")
        return
    
    # Load the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            url_data = json.load(f)
        print("Successfully loaded JSON file!")
        
        # Create a set of all URLs from all categories
        all_urls = set()
        for category in url_data.keys():
            all_urls.update(url_data[category])
        print(f"Total URLs in JSON: {len(all_urls)}")
    except FileNotFoundError:
        print(f"Error: Could not find the JSON file at {json_path}")
        return
    
    # Add 'url' column if it doesn't exist
    if 'url' not in df.columns:
        df['url'] = ''
        print("Added new 'url' column to the dataset")
    
    # Counter for matches
    matches = 0
    skipped = 0
    
    # Process each row without a URL
    for idx, row in df[df['url'].isna() | (df['url'] == '')].iterrows():
        name = row['name']
        expected_url = generate_url_from_name(name)
        
        if expected_url and expected_url in all_urls:
            df.at[idx, 'url'] = expected_url
            matches += 1
            print(f"✓ Match found for {name}: {expected_url}")
        else:
            if expected_url:
                print(f"× No match found for {name} (looking for: {expected_url})")
            skipped += 1
    
    # Save the updated CSV
    df.to_csv(csv_path, index=False)
    
    # Print summary
    print("\nProcess completed!")
    print(f"URLs matched: {matches}")
    print(f"Experts skipped: {skipped}")
    print(f"Total processed: {matches + skipped}")

if __name__ == "__main__":
    match_urls_from_json()