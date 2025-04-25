import requests
import fitz
from io import BytesIO

tenant_id = ""
client_id = ""
client_secret = ""

token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "https://graph.microsoft.com/.default"
}
token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
token_resp = requests.post(token_url, data=token_data, headers=token_headers)
token_json = token_resp.json()

if "access_token" not in token_json:
    print("❌ Token fetch failed:", token_json)
    exit()

access_token = token_json["access_token"]
print("✅ Token retrieved successfully.")

headers = {"Authorization": f"Bearer {access_token}"}

site_url = "https://graph.microsoft.com/v1.0/sites/ninebitc-my.sharepoint.com:/personal/khushi_ojha_ninebit_in:/"
site_resp = requests.get(site_url, headers=headers)

#print(site_resp.json())

site_data = site_resp.json()

if "id" not in site_data:
    print("❌ Failed to get site ID:", site_data)
    exit()
sites = site_data.get('value', [])
print("drive ************************************************* id",sites)
site_id = site_data["id"]
print("📌 Site ID:", site_id)

drive_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive"
drive_resp = requests.get(drive_url, headers=headers)
drive_data = drive_resp.json()

if "id" not in drive_data:
    print("❌ Failed to get drive ID:", drive_data)
    exit()
drives = drive_data.get('value', [])
print("drive ************************************************* id",len(drives))
drive_id = drive_data["id"]
print("📌 Drive ID:", drive_id)


url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
resp = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
data = resp.json()
#print("**************************", resp.json())

# for item in data.get("value", []):
#     item_type = "📁 Folder" if "folder" in item else "📄 File"
#     print(f"{item_type}: {item['name']}")


# url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
# resp = requests.get(url, headers=headers)
# items = resp.json().get("value", [])

# connectors_folder = None
# for item in items:
#     if item["name"].lower() == "connector" and "folder" in item:
#         connectors_folder = item
#         break

# if connectors_folder:
#     print(f"📁 Found folder - ID: {connectors_folder['id']}")
    
#     folder_id = connectors_folder["id"]
#     children_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_id}/children"
#     resp = requests.get(children_url, headers=headers)
#     items = resp.json().get("value", [])

#     pdf_files = [item for item in items if item["name"].lower().endswith(".pdf")]
#     if not pdf_files:
#         print("❗ No PDF files found in this folder.")
#     else:
#         print(f"📁 Found {len(pdf_files)} PDF files.")
# else:
#     print("❌ Folder not found.")

# for pdf in pdf_files:
#     pdf_name = pdf["name"]
#     pdf_id = pdf["id"]

#     print(f"\n📄 Downloading: {pdf_name}")

#     # Download the file content
#     download_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{pdf_id}/content"
#     download_resp = requests.get(download_url, headers=headers)

#     if download_resp.status_code != 200:
#         print(f"❌ Failed to download {pdf_name}: {download_resp.status_code}")
#         continue

#     # Read PDF from bytes
#     pdf_bytes = BytesIO(download_resp.content)
#     doc = fitz.open(stream=pdf_bytes, filetype="pdf")

#     print(f"📜 Extracted text from {pdf_name}:")
#     for page in doc:
#         text = page.get_text()
#         print(text)

search_name = "Aditi Jain.pdf"  # Partial or full name
search_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/search(q='{search_name}')"

resp = requests.get(search_url, headers=headers)
results = resp.json().get("value", [])

for file in results:
    if file["name"].lower().endswith(".pdf"):
        print(f"📄 Found PDF: {file['name']} (ID: {file['id']})")


