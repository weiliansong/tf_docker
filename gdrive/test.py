from g_drive import GDrive

GDrive = GDrive()

file_list = GDrive.ls_root()

for f in file_list:
  print('title: {:>40}, id: {}'.format(f['title'], f['id']))

g_folder = GDrive.mkdir('haha')
GDrive.upload(['test/test.txt'], parent_id=g_folder['id'])
