import os, tempfile, urllib.request

try:
    from urllib import FancyURLopener
except ImportError:
    from urllib.request import FancyURLopener


PLUGINS = ['repository.jakubicek222.and.jd',
           'https://github.com/Jakubicek222/plugin.video.jd.stream',

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
class MyOpener(FancyURLopener):
    version = UA
urlretrieve = MyOpener().retrieve

def delete_all_files(folder,skip):
    print('processing '+folder)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        #print(file_path)
        if not file_path in skip:
            try:
                if os.path.isfile(file_path):
                    print('unlinking '+file_path)
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    delete_all_files(file_path,skip)
                    print('removing '+file_path)
                    os.rmdir(file_path)
            except Exception as e:
                print(e)
        else:
            print('skipping '+file_path)

delete_all_files('repository',[])
externals = []
for ext in EXTERNAL:
    tmpf = tempfile.NamedTemporaryFile()
    tempname = tmpf.name + '_' + ext['name'] + '.zip'
    tmpf.close
    print("Downloading "+ext['url'])
    urlretrieve(ext['url'],tempname) 
    externals.append(tempname)

os.system("python create_repository.py --no-parallel --datadir repository " + " ".join(PLUGINS) + " " + " ".join(externals))

for tempname in externals:
    os.unlink(tempname)
