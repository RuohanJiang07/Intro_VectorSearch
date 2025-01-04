import json
import os

# File paths (assumes same folder as this script)
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 'careerbusiness_experts_urls.json')
output_file = os.path.join(current_dir, 'unique_careerbusiness_expert_urls.json')

# Read the JSON file with URLs
with open(input_file, 'r', encoding='utf-8') as file:
    urls = json.load(file)

# Remove duplicates using set and preserve order
unique_urls = list(dict.fromkeys(urls))

# Save unique URLs to a new JSON file
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(unique_urls, json_file, indent=4)

print(f"✅ Removed duplicates. {len(unique_urls)} unique URLs saved to '{output_file}'")
