import requests
import config

response = requests.get(
    f"{config.BASE_URL}/wp-json/wp/v2/categories",
    auth=(config.USER, config.PASSWORD)
)

if response.status_code == 200:
    categories = response.json()
    print("\n# Copy this into CATEGORY_MAP in publish_gem.py:")
    print("CATEGORY_MAP = {")
    for cat in sorted(categories, key=lambda x: x['name']):
        print(f"    '{cat['name']}': {cat['id']},")
    print("}")
    print(f"\nFound {len(categories)} categories total.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
