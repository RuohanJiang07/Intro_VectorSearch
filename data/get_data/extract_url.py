import re
import json
import os

# File paths (assumes same folder as this script)
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 'careerbusiness.html')
output_file = os.path.join(current_dir, 'careerbusiness_experts_urls.json')

# Regular expression to match expert URLs
pattern = r'https://intro\.co/([^?]+)\?source=intro'

# Read the HTML file and extract URLs
with open(input_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Find all matches using regex
urls = re.findall(pattern, html_content)

# Format URLs properly
expert_urls = [f'https://intro.co/{name}?source=intro' for name in urls]

# Save the URLs to a JSON file
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(expert_urls, json_file, indent=4)

print(f"✅ Extracted {len(expert_urls)} URLs and saved them to '{output_file}'")
