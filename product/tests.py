


# {
#     "product" : {
#         "id" : "h3794hfdxjn8m7r",
#         "name" : "Cordless Smart Screw Driver",
#         "brand":"IBELL",
#         "description" : "None",
#         "model_number" : "IBL BS03-06",
#         "stock" : 0
#     }
# }

# # das 
# # nandan@123



import requests

url = "http://127.0.0.1:8000/product/bulk-upload/"
files = {"file": open("/home/das/pro/southlake/tools-ecom-back/IBELL.xlsx", "rb")}

res = requests.post(url, files=files)
print(res.json())