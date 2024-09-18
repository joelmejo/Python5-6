import json
import jsonschema
import requests

def JsonSerialize(data):
    with open("data_file.json", 'w') as write_file:
        json.dump(data, write_file, indent=4)

def JsonDeserialize(sFile):
    with open(sFile, 'r') as read_file:
        return json.load(read_file)
    
def print_dictionary(dData, sRoot):
    for keys, values in dData.items():
        print()
        if type(dData[keys]) is dict:
            if sRoot != "":
                print("sRoot: " + sRoot + "." + keys)
            else:
                print("sRoot: " + keys)
            print("Dict: " + keys)
            print(type(dData[keys]))
            if sRoot != "":
                print_dictionary(dData[keys], sRoot + "." + keys)
            else:
                print_dictionary(dData[keys], keys)
                
        else:
            print("sRoot: " + sRoot)
            print("Key: " + keys)
            print(values)
            print(type(dData[keys]))


api_url = "https://jsonplaceholder.typicode.com/todos/5"
# api_url = "https://www.corriere.it"
response = requests.get(api_url)
print(response.json())
# print(response.status_code)
# print(response.headers["Content-Type"])
# if(response.status_code==200):
#     if (type(response.json()) is dict):
#         print_dictionary(response.json(), "")





# # sFile = "example_2.json"
# sFile = "example_3.json"
# instance = JsonDeserialize(sFile)
# schema = {
#     "type": "object",
#     "properties": {
#         "name": {"type": "string"},
#         "age": {"type": "number"},
#         "scores": {
#             "type": "array",
#             "items": {"type": "number"},
#         }
#     },
#     "required": ["name"],
#     "additionalProperties": False
# }

# try:
#     jsonschema.validate(instance, schema)
#     print("L'istanza è coerente con lo schema")
# except jsonschema.exceptions.ValidationError:
#     print("L'istanza non è valida")

# print_dictionary(instance, "")


# JsonSerialize(instance)