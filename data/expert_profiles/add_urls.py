import pandas as pd
import os

def add_urls_to_csv():
    # Get the current directory and construct the path to the CSV
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'expert_profiles_all.csv')
    
    print(f"Looking for CSV file at: {csv_path}")
    
    # Read the CSV file
    try:
        df = pd.read_csv(csv_path)
        print("Successfully loaded CSV file!")
    except FileNotFoundError:
        print(f"Error: Could not find the CSV file at {csv_path}")
        return
    
    # Add 'url' column if it doesn't exist
    if 'url' not in df.columns:
        df['url'] = ''
        print("Added new 'url' column to the dataset")
    
    # Get starting expert name
    print("\nCurrent experts without URLs:")
    missing_urls = df[df['url'].isna() | (df['url'] == '')]['name'].tolist()
    for i, name in enumerate(missing_urls):
        print(f"{i+1}. {name}")
    
    start_name = input("\nEnter the expert name to start from (or press Enter to start from the beginning): ").strip()
    
    # Find starting index
    if start_name:
        if start_name not in df['name'].values:
            print(f"Expert '{start_name}' not found. Starting from the beginning.")
            start_idx = 0
        else:
            start_idx = df[df['name'] == start_name].index[0]
    else:
        start_idx = 0
    
    # Iterate through rows starting from start_idx
    try:
        for idx in range(start_idx, len(df)):
            row = df.iloc[idx]
            
            # Skip if URL already exists
            if pd.notna(row['url']) and row['url'] != '':
                continue
                
            print("\n" + "="*50)
            print(f"Expert {idx+1} of {len(df)}")
            print(f"Name: {row['name']}")
            print(f"Category: {row['category']}")
            print(f"Label: {row['label']}")
            print("Profile preview:", row['profile'][:200] + "...")
            
            # Get URL input
            while True:
                url = input("\nEnter URL (or 'skip' to move to next, 'quit' to save and exit): ").strip()
                if url.lower() == 'quit':
                    raise KeyboardInterrupt
                if url.lower() == 'skip' or url:
                    break
                print("Please enter a URL or 'skip' or 'quit'")
            
            if url.lower() != 'skip':
                df.at[idx, 'url'] = url
                
            # Save after each entry
            df.to_csv(csv_path, index=False)
            print("Progress saved!")
            
    except KeyboardInterrupt:
        print("\nSaving progress...")
        df.to_csv(csv_path, index=False)
        print("Progress saved! You can resume later by entering the last expert's name.")
    
    print("\nProcess completed!")
    remaining = len(df[df['url'].isna() | (df['url'] == '')])
    print(f"Remaining experts without URLs: {remaining}")

if __name__ == "__main__":
    add_urls_to_csv()