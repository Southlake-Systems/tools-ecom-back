import requests

url = "http://127.0.0.1:8000/product/bulk-upload/"
files = {"file": open("/home/das/pro/southlake/tools-ecom-back/sheets/productsheet.xlsx", "rb")}



res = requests.post(url, files=files)
print(res.json())