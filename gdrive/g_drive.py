import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GDrive(object):

  def __init__(self):
    self.authenticated = False
    self.folder_mime_type = 'application/vnd.google-apps.folder'

  def authenticate(self):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile('credentials.json')

    if gauth.credentials is None:
      gauth.CommandLineAuth()

    elif gauth.access_token_expired:
      gauth.Refresh()

    else:
      gauth.Authorize()

    gauth.SaveCredentialsFile('credentials.json')

    self.gauth = gauth
    self.drive = GoogleDrive(self.gauth)
    self.authenticated = True

  def ls_root(self):
    if not self.authenticated:
      self.authenticate()

    file_list = self.drive.ListFile(
                        {'q': "'root' in parents and trashed=false"}).GetList()

    return file_list

  # TODO Implement this
  def folder_exists(self, folder_name):
    raise Exception('Not yet implemented')

  def mkdir(self, folder_name, parent_id='root'):
    if not self.authenticated:
      self.authenticate()

    if parent_id == 'root':
      g_folder = self.drive.CreateFile({'title': folder_name,
                                        'mimeType': self.folder_mime_type})

    else:
      g_folder = self.drive.CreateFile({'title': folder_name,
                                        'parents': [{'id': parent_id}],
                                        'mimeType': self.folder_mime_type})

    g_folder.Upload()
    print('Folder {} created successfully!'.format(folder_name))

    return g_folder

  def upload(self, fnames, parent_id='root'):
    if not self.authenticated:
      self.authenticate()

    for fname in fnames:
      if not os.path.exists(fname):
        print('File {} does not exist, skipping...'.format(fname))

      if parent_id == 'root':
        g_file = self.drive.CreateFile({'title':fname.strip().split('/')[-1]})
      else:
        g_file = self.drive.CreateFile({'title':fname.strip().split('/')[-1],
                                        'parents': [{
                                            'kind': 'drive#childList',
                                            'id': parent_id}
                                        ]})

      g_file.SetContentFile(fname)
      g_file.Upload()

      print('title: %s, mimeType: %s' % (g_file['title'], g_file['mimeType']))

  def download(self, fname, fid):
    if not self.authenticated:
      self.authenticated()

    if not os.path.exists('/tmp/gdrive'):
      os.mkdir('/tmp/gdrive')

    g_file = drive.CreateFile({'id': fid})
    g_file.GetContentFile('/tmp/gdrive/' + fname)
