import requests
from github import Github

github = Github('shivamgupta-sg', "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")
user = github.get_user()
repository = user.get_repo('storage-acc-test')


user = "shivamgupta-sg"
repo = "storage-acc-test"

url = f"https://api.github.com/repos/{user}/{repo}/git/trees/main?recursive=1"
r = requests.get(url)
res = r.json()
# print (res)

yml_substring = ".yml"
yaml_substring = ".yaml"

substring = "."
for file in res["tree"]:
    # print(file["path"])
    if yml_substring in file["path"] or yaml_substring in file["path"]:
        # print (file["path"])
        yml_files_list = []
        yml_files_list.append(file["path"])
        # print(yml_files_list)
        for yml_file in yml_files_list:
            if "/" in yml_file:
                # print (yml_file)
                parameter_yml_files_list = []
                parameter_yml_files_list.append(yml_file)
                print(parameter_yml_files_list)
                
                parameters = []
                for parameter_yml_file in parameter_yml_files_list:
                    parameter_yml_file_raw_url = "https://raw.githubusercontent.com/shivamgupta-sg/storage-acc-test/main/environments/us/dev/central-us/test.yml"
                    file_content = repository.get_contents(parameter_yml_file)
                    print(file_content)
                    print(file_content.decoded_content.decode())
                    print(file_content.decoded_content.decode().split('\n'))
                    value_list = file_content.decoded_content.decode().split('\n')
                    # with open(parameter_yml_file, 'r') as f:
                    #     print(f.read())
                    for value in value_list:
                        print(value)
                        value.split(":")