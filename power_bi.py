import requests
import msal
from creds import username, password
# creds file just contains the following:
# username = 'your email e.g. sunny.sharma@datalytyx.com'
# password = 'your password e.g. Notachancethisworks!'


def request_access_token():
    app_id = 'Application_Client_ID_goes_here'
    tenant_id = 'Directory_Tenant_ID_goes_here'

    authority_url = 'https://login.microsoftonline.com/' + tenant_id
    scopes = ['https://analysis.windows.net/powerbi/api/.default']

    # Step 1. Generate Power BI Access Token
    client = msal.PublicClientApplication(app_id, authority=authority_url)
    token_response = client.acquire_token_by_username_password(
        username=username, password=password, scopes=scopes)
    if not 'access_token' in token_response:
        raise Exception(token_response['error_description'])

    access_id = token_response.get('access_token')
    return access_id


access_id = request_access_token()

dataset_id = 'Dataset_ID_goes_here'
endpoint = f'https://api.powerbi.com/v1.0/myorg/datasets/{dataset_id}/refreshes'
headers = {
    'Authorization': f'Bearer ' + access_id
}

response = requests.post(endpoint, headers=headers)
if response.status_code == 202:
    print(f'Dataset {dataset_id} refreshed')
else:
    print(f'Dataset {dataset_id} NOT refreshed')
    print(response.reason)
    print(response.json())
