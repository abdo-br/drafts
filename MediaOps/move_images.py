# %%
import os, time, datetime
import shutil



# %%

def get_year(file, ):

    return str(datetime.datetime.fromtimestamp(os.path.getmtime(file)).year)


source_folder = 'F:/Phone backup/DCIM/Camera/'
destination_folder = 'F:/Phone backup/DCIM/'

for file_name in os.listdir(source_folder):

    source_path = os.path.join(source_folder, file_name)

    if os.path.isfile(source_path):

        creation_year = get_year(source_path)
        destination_path = os.path.join(destination_folder+creation_year, file_name)

        try:
            shutil.move(source_path, destination_path)
            print(f'Moved: {file_name}')
        finally:
            pass


# %%
