import urllib.request
import datetime
import os
import csv
import json

def fetch_latest_kaggle_data():
    base_url = "https://raw.githubusercontent.com/teranixbq/KaggleTrending/main/data/trending_{}.csv"
    today = datetime.datetime.now(datetime.timezone.utc)
    
    os.makedirs('data', exist_ok=True)
    
    for i in range(14):
        date_str = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        url = base_url.format(date_str)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8')
                
                reader = csv.DictReader(content.splitlines())
                data = list(reader)[:5]
                
                for row in data:
                    row['owner'] = row['ref'].split('/')[0]
                    
                    last_updated = row.get('lastUpdated', '')
                    try:
                        dt = datetime.datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)
                        days_ago = (today - dt).days
                        row['updated_text'] = f"Updated {days_ago} days ago" if days_ago > 0 else "Updated today"
                    except:
                        row['updated_text'] = "Updated recently"
                    
                    try:
                        downloads = int(row.get('downloadCount', 0))
                        if downloads >= 1000000:
                            row['download_text'] = f"{downloads/1000000:.2f}M"
                        elif downloads >= 1000:
                            row['download_text'] = f"{downloads/1000:.1f}k"
                        else:
                            row['download_text'] = str(downloads)
                    except:
                        row['download_text'] = "0"

                with open('data/kaggle.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                    
                print(f"Successfully fetched and processed Kaggle data for {date_str}")
                return
        except Exception as e:
            continue
            
    print("Failed to fetch Kaggle data from the last 14 days.")

if __name__ == "__main__":
    fetch_latest_kaggle_data()
