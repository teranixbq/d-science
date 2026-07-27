import urllib.request
import datetime
import os
import json

def fetch_latest_hf_data():
    url = "https://huggingface.co/api/trending?type=model"
    today = datetime.datetime.now(datetime.timezone.utc)
    
    os.makedirs('data', exist_ok=True)
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            raw_data = json.loads(content)
            
            trending_list = raw_data.get('recentlyTrending', [])
            
            processed_data = []
            
            for item in trending_list[:5]: 
                repo_data = item.get('repoData', {})
                
                full_id = repo_data.get('id', '')
                
                pipeline_tag = repo_data.get('pipeline_tag', '')
                if pipeline_tag:
                    pipeline_tag = ' '.join(word.capitalize() for word in pipeline_tag.split('-'))

                last_updated = repo_data.get('lastModified', '')
                try:
                    dt = datetime.datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)
                    days_ago = (today - dt).days
                    updated_text = f"Updated {days_ago} days ago" if days_ago > 0 else "Updated today"
                except:
                    updated_text = "Updated recently"
                
                try:
                    downloads = int(repo_data.get('downloads', 0))
                    if downloads >= 1000000:
                        download_text = f"{downloads/1000000:.1f}M"
                    elif downloads >= 1000:
                        download_text = f"{downloads/1000:.1f}k"
                    elif downloads == 0:
                        download_text = "0"
                    else:
                        download_text = str(downloads)
                except:
                    download_text = "0"
                    
                processed_data.append({
                    "id": full_id,
                    "pipeline_tag": pipeline_tag,
                    "updated_text": updated_text,
                    "download_text": download_text
                })

            with open('data/huggingface.json', 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2)
                
            print(f"Successfully fetched and processed Hugging Face trending data.")
            return
            
    except Exception as e:
        print(f"Failed to fetch Hugging Face data: {e}")

if __name__ == "__main__":
    fetch_latest_hf_data()
