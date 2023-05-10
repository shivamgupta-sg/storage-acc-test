#!/usr/bin/env python3
import requests
import base64
import requests
import os
import shutil
import yaml
import urllib3
from zipfile import ZipFile


#############
# FUNCTIONS #
#############

# Get GitHub Repo as Zip
def get_github_repo(owner: str, repo: str, ref: str, token: str, outfile: str = 'repo.zip') -> str:
    http = urllib3.PoolManager()

    url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{ref}"

    r = http.request(
        'GET',
        url=url,
        preload_content=False,
        headers={'Authorization': "Bearer " + token}
    )

    with open(outfile, 'wb') as out:
        while True:
            data = r.read(64)
            if not data:
                break
            out.write(data)
    r.release_conn()

    return outfile


# Extract zip file
def extract_zip_file(file: str) -> int:
    with ZipFile(file, 'r') as zObject:
        # Extracting all the members of the zip into a specific location.
        zObject.extractall(path="repo")
    return 0


# Get the subfolders name
def get_subfolders_name(dirname: str) -> list:
    subdirs_list = [os.path.join(dirname, o) for o in os.listdir(
        dirname) if os.path.isdir(os.path.join(dirname, o))]
    # print('From Function: ')
    # print(subdirs_list)
    return subdirs_list


# Get File Content from the file present on given file path
def get_file_content(file: str) -> dict:
    with open(file, "r") as yaml_file:
        # print(type(yaml.safe_load(naas_yaml)))
        return yaml.safe_load(yaml_file)


# Get the pipeline id for the resource
def get_pipeline_id(resource: str, subdir: str) -> str:
    pipeline_id_yaml_file_content = get_file_content(
        file=f"repo/{subdir}/Code/yml/Pipeline_id.yml")

    for pipeline_data in pipeline_id_yaml_file_content["resources"]:
        if pipeline_data["resourceType"] == resource:
            # print(pipeline_data["pipelineID"])
            return pipeline_data['pipelineID']


# build headers for pipeline api call
def build_headers_for_ado_with_authorization(ado_pat_token: str, content_type: str = 'application/json') -> dict:
    headers = {
        "Authorization": "Basic " + base64.b64encode(f":{ado_pat_token}".encode("ascii")).decode("ascii"),
        "Content-Type": content_type
    }
    return headers


# trigger pipeline
def trigger_pipeline(pipeline_id: str, organization_name: str, project_name: str, pipeline_parameters:dict={}) -> int:
    api_url = f"https://dev.azure.com/{organization_name}/{project_name}/_apis/pipelines/{pipeline_id}/runs?api-version=7.0"
    ado_pat = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    # print(pipeline_parameters)
    
    if pipeline_parameters:
        template_parameters = {}
        template_parameters['kubernetes_version']= pipeline_parameters['kubernetes-version']
        template_parameters['autoscaling_enabled'] = pipeline_parameters['autoscaling-enabled']
        template_parameters['node_count']=pipeline_parameters['node-pool']['node-count']
        template_parameters['node_pool_type']=pipeline_parameters['node-pool']['type']
        template_parameters['node_pool_vm_size']=pipeline_parameters['node-pool']['vm']['size']
        template_parameters['node_pool_vm_disk_size']=pipeline_parameters['node-pool']['vm']['os-disk-size-gb']
        
        # print(template_parameters)
    
    # kubernetes_version = component['config']['kubernetes-version']
    # print(f'Kubernetes version: {kubernetes_version}')

    # autoscaling_enabled = component['config']['autoscaling-enabled']
    # print(f'Node count: {autoscaling_enabled}')

    # node_count = component['config']['node-pool']['node-count']
    # print(f'Node count: {node_count}')
    
    # node_pool_type = component['config']['node-pool']['type']
    # print(f'Node pool type: {node_pool_type}')

    # node_pool_vm_size = component['config']['node-pool']['vm']['size']
    # print(f'Node pool type: {node_pool_vm_size}')
    
    # node_pool_vm_disk_size = component['config']['node-pool']['vm']['os-disk-size-gb']
    # print(f'Node pool type: {node_pool_vm_disk_size}')
    
    body_data = {
        'templateParameters': template_parameters,
        "definition": {
            "id": pipeline_id
        }
    }
    
    print(body_data)

    # response = requests.post(api_url, headers=build_headers_for_ado_with_authorization(
    #     ado_pat_token=ado_pat), json=body_data)

    # if response.status_code == 200:
    #     print("triggered successfully!")
    #     return 0
    # else:
    #     print(f"failed{response.status_code}")
    #     return response.status_code


# Remove the directory (recursive or non recursive)
def remove_directory(dirname: str, recursive: bool) -> int:
    if recursive:
        shutil.rmtree(dirname)
        return 0
    else:
        os.rmdir(dirname)
        return 0


# Remove the file
def remove_file(filename: str) -> int:
    os.remove(filename)
    return 0


#################
# MAIN FUNCTION #
#################

def main():
    # download the Github Repository as a zip file
    zipfile_name = get_github_repo(owner="duck-creek", repo="DCOD.Next.EMS",
                                   ref="master", token="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    # extract the zip file (github repository)
    extract_zip_file(file=zipfile_name)

    subdir_list = get_subfolders_name(dirname='repo')

    # print(subdir_list)
    # subdir = None

    try:
        # pass
        if len(subdir_list) == 1:
            subdir = subdir_list[0].split('\\')
        # print(subdir)

        # get compute.yml file content
        compute_yaml_file_content = get_file_content(
            file=f"repo/{subdir[-1]}/environments/us/dev/central-us/compute.yml")
        # print(compute_yaml_file_content)

        # print(compute_yaml_file_content['components'])

        for component in compute_yaml_file_content['components']:
            if component['type'] == 'aks':
                aks_config = component['config']
                # kubernetes_version = component['config']['kubernetes-version']
                # print(f'Kubernetes version: {kubernetes_version}')

                # autoscaling_enabled = component['config']['autoscaling-enabled']
                # print(f'Node count: {autoscaling_enabled}')

                # node_count = component['config']['node-pool']['node-count']
                # print(f'Node count: {node_count}')
                
                # node_pool_type = component['config']['node-pool']['type']
                # print(f'Node pool type: {node_pool_type}')

                # node_pool_vm_size = component['config']['node-pool']['vm']['size']
                # print(f'Node pool type: {node_pool_vm_size}')
                
                # node_pool_vm_disk_size = component['config']['node-pool']['vm']['os-disk-size-gb']
                # print(f'Node pool type: {node_pool_vm_disk_size}')

    #     # get the pipeline id from the pipelineId.yml
    #     pipelineId = get_pipeline_id(resource='aks', subdir=subdir[-1])
    #     print('')
    #     print(f'Resource: aks')
    #     print(f'Pipeline Id: {pipelineId}')

    #     # for resource in component_yaml_file_content['resources']:
    #     #     print(resource['properties']['resourceType']==resource)
    #     # print(resource['properties'])

        organization = 'hershal8090gupta'
        project = 'projectname'
        pipeline_id = '2'

        # trigger the pipeline
        trigger_pipeline(pipeline_id=pipeline_id,
                        organization_name=organization, project_name=project, pipeline_parameters = aks_config)

    finally:
        # clean up the workspace
        remove_directory(dirname='repo', recursive=True)
        remove_file(filename='repo.zip')


#########################
# calling main function #
#########################
if __name__ == '__main__':
    main()
