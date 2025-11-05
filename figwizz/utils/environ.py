"""
Environment variable loading + checking functions
"""

import os

__all__ = [
    'load_env_variables',
]

# Environment Variable Checking Functions ----------------------------------------

def search_for_env_file(env_file='auto', max_parents=3, abspath=False):
    env_file_opts = ['env', 'env.local', 'env.development', 'env.production']
    
    if env_file != 'auto' or env_file is not None:
        env_file_opts = [env_file]
    
    env_filepath = None
    
    for i in range(max_parents):
        for file_opt in env_file_opts:
            relative_path = os.path.join(os.getcwd(), *['..']*i, file_opt)
            if os.path.exists(relative_path):
                env_filepath = relative_path
                break
    
    if env_filepath is not None:
        print(f"Found .env file at {env_filepath}")
        if abspath:
            env_filepath = os.path.abspath(env_filepath)
            
    return env_filepath # return the path to the env file
    
def load_env_variables(env_file='auto', update_environ=True, **kwargs):
    if not os.path.exists(env_file):
        env_file = search_for_env_file(env_file, **kwargs)
        if env_file is None:
            raise FileNotFoundError(f"No .env file found in the current or parent directories.")
    
    if env_file is not None:
       # update the environment variables with the values from the env file
       env_vars = {}
       with open(env_file, 'r') as file:
           for line in file:
               if line.startswith('#'):
                   continue
               key, value = line.strip().split('=')
               env_vars[key] = value
               
       if not update_environ:
            return env_vars
       else: # update the global env
            os.environ.update(env_vars)
            return None