import os
import re
import csv

# Base directory for the downloaded HTML files
BASE_DIR = "/Users/lesliejiang/Desktop/intro_co/data/get_data/expert_html_files"
OUTPUT_CSV = "expert_profiles_all.csv"

# Regex patterns for extracting data
name_pattern = r"<title>Intro - Book with (.*?)</title>"
label_pattern = r'</div><p class="font-sofia tracking-tight leading-5 text-\[17px\] text-\[#807F7F\]">(.*?)</p><div class="rating'
profile_pattern = r'<p class="font-sofia text-\[17px\] font-light leading-6 tracking-\[-0.25px\] text-charcoal whitespace-pre-wrap pt-2 uncropped">(.*?)</p></div></div></div><div class="'

# List to store all extracted expert data
expert_data = []

# Process each category folder
for category in os.listdir(BASE_DIR):
    category_path = os.path.join(BASE_DIR, category)
    if os.path.isdir(category_path):
        print(f"📂 Processing category: {category}")
        for filename in os.listdir(category_path):
            if filename.endswith(".html"):
                file_path = os.path.join(category_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        
                        # Extract data using regex patterns
                        name_match = re.search(name_pattern, content)
                        name = name_match.group(1) if name_match else "N/A"
                        
                        label_match = re.search(label_pattern, content)
                        label = label_match.group(1) if label_match else "N/A"
                        
                        profile_match = re.search(profile_pattern, content, re.S)
                        profile = profile_match.group(1).strip() if profile_match else "N/A"
                        
                        # Append extracted data to the list
                        expert_data.append({
                            "category": category,
                            "name": name,
                            "label": label,
                            "profile": profile
                        })
                        
                        print(f"✅ Extracted data from {filename}")
                
                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")

# Save the extracted data to a CSV file
try:
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['category', 'name', 'label', 'profile']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for expert in expert_data:
            writer.writerow(expert)
    
    print(f"\n🎉 Data successfully saved to {OUTPUT_CSV}")
except Exception as e:
    print(f"❌ Error saving CSV file: {e}")
