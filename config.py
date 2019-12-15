import yaml

WEBSERVICE_CONFIG_TICKET = {
    'Name': 'GenericTicketConnectorREST',
    'Config': {
        'SessionCreate': {'RequestMethod': 'POST',
                          'Route': '/Session',
                          'Result': 'SessionID'},
        'TicketCreate': {'RequestMethod': 'POST',
                         'Route': '/Ticket',
                         'Result': 'TicketID'},
        'TicketGet': {'RequestMethod': 'GET',
                      'Route': '/Ticket/:TicketID',
                      'Result': 'Ticket'},
        'TicketGetList': {'RequestMethod': 'GET',
                          'Route': '/TicketList',
                          'Result': 'Ticket'},
        'TicketSearch': {'RequestMethod': 'POST',
                         'Route': '/TicketSearch',
                         'Result': 'TicketID'},
        'TicketUpdate': {'RequestMethod': 'PATCH',
                         'Route': '/Ticket/:TicketID',
                         'Result': 'TicketID'},
        'TicketSearchHistory': {'RequestMethod': 'GET',
                                'Route': '/TicketHistoryGet/:TicketID',
                                'Result': 'Ticket'
                                }
    }
}
with open('./app.conf') as f:
    SETTINGS = yaml.load(f)
DB_STRING = SETTINGS['db']['url']

URL = SETTINGS['otrs']['url']
USERNAME = SETTINGS['otrs']['username']
PASSWORD = SETTINGS['otrs']['password']
HTTPS_VERIFY = SETTINGS['otrs']['verify_ssl']
# Токен для доступа по API к Youtrack
PERM_AUTH_TOKEN = SETTINGS['youtrack']['yt_token']

# URL Youtrack API
BASE_URL = SETTINGS['youtrack']['url']

REQUEST_HEADERS = {
    'Authorization': 'Bearer {token}'.format(token=PERM_AUTH_TOKEN),
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

REQUEST_HEADERS_UPLOAD = {
    'Authorization': 'Bearer {token}'.format(token=PERM_AUTH_TOKEN),
    'Accept': 'application/json'
}

YOUTRACK_PROJECT = SETTINGS['youtrack']['yt_project']
