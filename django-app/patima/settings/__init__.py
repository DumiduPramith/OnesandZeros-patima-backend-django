from dotenv import load_dotenv
from split_settings.tools import include
import os
from pathlib import Path

# load .env file
env_path = Path('') / '.env'

load_dotenv(dotenv_path=env_path)

if os.getenv('DJANGO_ENV') == 'dev':
    dev_env_path = Path('') / '.env.dev'
    load_dotenv(dotenv_path=dev_env_path)
    include('dev.py')
if os.getenv('DJANGO_ENV') == 'prod':
    prod_env_path = Path('') / '.env.prod'
    load_dotenv(dotenv_path=prod_env_path)
    include('prod.py')
