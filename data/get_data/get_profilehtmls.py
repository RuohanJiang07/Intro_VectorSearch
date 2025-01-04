import os
import requests
import json

# Define the current folder as the base directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the JSON file from the same folder as the script
json_file_path = os.path.join(CURRENT_DIR, 'expert_urls.json')
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Create a base folder for the downloads in the same directory
BASE_DIR = os.path.join(CURRENT_DIR, 'expert_html_files')
os.makedirs(BASE_DIR, exist_ok=True)

# Loop through each category and download the HTML content
for category, urls in data.items():
    # Create a folder for each category
    category_dir = os.path.join(BASE_DIR, category.replace('&', 'and').replace(' ', '_'))
    os.makedirs(category_dir, exist_ok=True)
    
    print(f"📂 Downloading HTML files for category: {category}")
    for index, url in enumerate(urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"{index + 1}.html"
                filepath = os.path.join(category_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as html_file:
                    html_file.write(response.text)
                print(f"✅ Saved: {filepath}")
            else:
                print(f"❌ Failed to download {url} - Status Code: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error downloading {url}: {e}")

print("\n🎉 Download complete!")
