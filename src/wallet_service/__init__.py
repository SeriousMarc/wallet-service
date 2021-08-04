import os

SECRET = os.getenv('SECRET', b'')

# TODO
#   1. change ID to UUID
#   2. transaction wrapper around wallet operations as Deco or DI
#   3. logger
