import sys
import pathlib
import os
from terminy import parse_param

if __name__=="__main__":
    params = {'command': {'short':'c'
            , 'has_parameter':True
            , 'mandatory':True
            , 'description':'Command to be executed.'}
        , 'app': {'short':'a'
            , 'has_parameter':True
            , 'mandatory':True
            , 'description':'Application name.'}}
    parsed_params = parse_param(sys.argv, params)
    command = parsed_params['command']['value']
    app = parsed_params['app']['value']
    print(parsed_params)
    if command=='create':
        try:
            path = pathlib.Path().resolve()
            file_path = pathlib.Path(__file__).parent.resolve()
            print(str(path))
            fullpath = os.path.join(path, app)
            if os.path.isdir(fullpath):
                raise Exception("Aplicação já existe.")
            os.makedirs(fullpath)
            for subdir in ['controller', 'model', 'view']:
                os.makedirs(os.path.join(fullpath, subdir))
            with open(os.path.join(fullpath, 'main.py'), 'w') as fp:
                pass
        except Exception as e:
            raise Exception(str(e))
    else:
        raise Exception("Unrecognized command: {}".format(command))
