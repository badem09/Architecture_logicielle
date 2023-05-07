import os

config = dict(
DATABASE_URL=os.getenv('TOUDOU_DATABASE_URL', ''),
DEBUG=os.getenv('TOUDOU_DEBUG', 'False') == 'True'
)
