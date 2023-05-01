# PARAMETERS
Param(
    [Parameter(Mandatory = $True)]
    [String] $resourceType
)

# $credentials = "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"
# $repo = "KirtiGhugtyal6/Read-Json"

# FUNCTIONS
# Function to fetch the pipeline id from the json stored on GitHub
function FetchPipelineId {
    param (
        [Parameter(Mandatory = $True)]
        [String] $resourceType
    )

    $pipelineIdJsonRawUrl = "https://raw.githubusercontent.com/KirtiGhugtyal6/Read-Json/main/id.json"
    $pipelineIdJsonFileContent = Invoke-WebRequest -Uri $pipelineIdJsonRawUrl

    $pipelineIdJson = $pipelineIdJsonFileContent | ConvertFrom-Json

    foreach ($resource in $pipelineIdJson.resources) {
        if ($resource.resourceType -eq $resourceType) {
            # Write-Host $resource.pipelineID
            # TriggerPipeline -pipelineId $resource.PipelineID -projectName $resource.project
            return $resource.pipelineID, $resource.project
        }
    }
}


# Function to fetch domain, env, subscriptionId, customerId
function FetchPipelineParametersValue {
    $pipelineParametersJsonRawUrl = "https://raw.githubusercontent.com/shivamgupta-sg/storage-acc-test/main/pipeline_parameters.json"
    $pipelineParametersJsonFileContent = Invoke-WebRequest -Uri $pipelineParametersJsonRawUrl

    $pipelineParametersJson = $pipelineParametersJsonFileContent | ConvertFrom-Json

    return $pipelineParametersJson.domain, $pipelineParametersJson.env, $pipelineParametersJson.subscriptionId, $pipelineParametersJson.customerId    
}


# Function to trigger the Azure DevOps pipeline
function TriggerPipeline {
    param (
        [Parameter(Mandatory = $True)]
        [string] $pipelineId,
        [Parameter(Mandatory = $True)]
        [string] $projectName,
        [Parameter(Mandatory = $True)]
        [String] $domainParameterValue,
        [Parameter(Mandatory = $True)]
        [String] $envParameterValue,
        [Parameter(Mandatory = $True)]
        [String] $subscriptionIdParameterValue,
        [Parameter(Mandatory = $True)]
        [String] $customerIdParameterValue
    )

    $organizationName = "hershal8090gupta" 
    $ado_pat = "nccleljurvhqhz7bftdiodakwladqwg4sfzzw6hnu5kfxj3emoda"
    # Write-Output "Pipeline ID: $pipelineId"
    $base64AuthInfo = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes(":$($ado_pat)"))
    $adoPipelineRunApiUrl = "https://dev.azure.com/$organizationName/$projectName/_apis/pipelines/$pipelineId/runs?api-version=7.0"
    $body = @{
        templateParameters = @{
            domain = $domainParameterValue
            env = $envParameterValue
            subscriptionId = $subscriptionIdParameterValue
            customerId = $customerIdParameterValue
          }
        resources = @{
            repositories = @{
                self = @{
                    refName = "refs/heads/main"
                }
            }
        }
    } | ConvertTo-Json

    Write-Host $body.GetType()

    $response = Invoke-RestMethod -Method Post -Uri $adoPipelineRunApiUrl -Headers @{Authorization = "Basic $base64AuthInfo" } -ContentType "application/json" -Body $body
    Write-Host $response
}


$pipelineId, $projectName = FetchPipelineId -resourceType $resourceType
$domainParameterValue, $envParameterValue, $subscriptionIdParameterValue, $customerIdParameterValue = FetchPipelineParametersValue
TriggerPipeline -pipelineId $pipelineId -projectName $projectName -domainParameterValue $domainParameterValue -envParameterValue $envParameterValue -subscriptionIdParameterValue $subscriptionIdParameterValue -customerIdParameterValue $customerIdParameterValue