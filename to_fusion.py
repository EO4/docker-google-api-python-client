import sys
import httplib2
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.http import MediaFileUpload

KEY_FILE='/.config/gclib/sa_key.json'
FT_SCOPE = 'https://www.googleapis.com/auth/fusiontables'
DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'
READ_PERMISSION={'type': 'anyone','role': 'reader'}
FT_ROOT="https://www.google.com/fusiontables/DataSource?docid="


""" upload csv to fusion table

  Args:
    table_name<str>: name of fusion table
    file_path<str>: path/to/file.csv
    return_response<bool>:
      * if true return response from googleapiclient along with the fusion-table id
      * otherwise return the fusion-table id
    read_all<bool>:
      * if true update the permissions of the fusion-table to Public-Read.

"""
def csv_to_ft(table_name,file_path,return_response=False,read_all=True):
  fusiontable = _create_service()
  request=fusiontable.table().importTable(name=table_name,media_body=_file_media(file_path))
  try:
    # create table
    create_table_response=request.execute()
    ft_id=create_table_response.get("tableId")
    # set permission (optional)
    if ft_id and read_all: set_permissions(ft_id)
    # return response
    if return_response: return ft_id, create_table_response
    else: return ft_id
  except Exception as e:
    print "\n\ncsv_to_ft: ERROR {}, {}:\n\t{}\n".format(file_path,table_name,e)
    if return_response:
      return None, e
    else:
      return None


""" set_permissions for fusion table

  Args:
    ft_id<str>: fusion-table id
    permission<dict>: fusion table permissions. defaults to Public-Read.

"""
def set_permissions(ft_id,permission=READ_PERMISSION):
  try:
    drive = _create_service('drive')
    drive.permissions().insert(fileId=ft_id,body=permission).execute()
    return True
  except Exception as e:
    print "\n\nset_permissions: ERROR {}, {}:\n\t{}\n".format(ft_id,permission,e)
    return False


#
# HELPERS
#
def _create_service(service='fusiontables',version='v2'):
  credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, [FT_SCOPE,DRIVE_SCOPE])
  http = httplib2.Http()
  credentials.authorize(http)
  return discovery.build(service, version, http=http)

def _file_media(file_path):
return MediaFileUpload(file_path,mimetype='application/octet-stream')
