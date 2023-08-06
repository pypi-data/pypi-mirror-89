
__title__ = 'mbuslite'
__version__ = '0.0.1'
__description__ = 'A small, in-process message bus implementation.'
__author__ = 'Francis Ferrell'
__author_email__ = 'francisferrell@gmail.com'
__copyright__ = f'Copyright 2020 {__author__}'
__url__ = 'https://gitlab.com/francisferrell/mbuslite'
__license__ = 'MIT'



from .bus import MessageBus
from .service import Service

Bus = MessageBus()

