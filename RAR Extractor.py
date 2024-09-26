import requests
from bs4 import BeautifulSoup
import re

def extract_rar_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.find_all('a', href=True)
        
        rar_links = [link['href'] for link in links if link['href'].lower().endswith('.rar')]
        
        rar_links = [requests.compat.urljoin(url, link) for link in rar_links]
        
        return rar_links
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    input_file = 'websites.txt'
    output_file = 'rar_download_links.txt'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            websites = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        print("Error: Unable to read the input file with UTF-8 encoding. Trying with 'utf-8-sig' encoding...")
        try:
            with open(input_file, 'r', encoding='utf-8-sig') as f:
                websites = [line.strip() for line in f if line.strip()]
        except UnicodeDecodeError:
            print("Error: Unable to read the input file. Please ensure it's saved in UTF-8 encoding.")
            return
    
    all_rar_links = []
    
    for website in websites:
        print(f"Processing: {website}")
        rar_links = extract_rar_links(website)
        all_rar_links.extend(rar_links)
    
    unique_rar_links = list(dict.fromkeys(all_rar_links))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in unique_rar_links:
            f.write(f"{link}\n")
    
    print(f"RAR download links have been saved to {output_file}")

if __name__ == "__main__":
    main()
