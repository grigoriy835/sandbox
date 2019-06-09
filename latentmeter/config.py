from os.path import join, dirname, isfile
from dotenv import load_dotenv
from os import environ

dotenv_path = join(dirname(__file__), '.env')
if isfile(dotenv_path):
    load_dotenv(dotenv_path)

telegram_config = {
    'token': environ.get('TOKEN', 12345)
}

db_config = {

}
