import traceback
import json
from pyotrs import Client as OtrsClient
import argparse


from otrs import (
    get_otrs_tickets_id, create_or_update_otrs_tickets)
from yt import create_or_update_youtrack_issues
from helpers.exceptions import OtrsAuthException
from helpers.models import session, Ticket
from config import WEBSERVICE_CONFIG_TICKET, URL, USERNAME, PASSWORD, HTTPS_VERIFY


class Client(OtrsClient):
    def get_history(self, ticket_id):
        self.operation = "TicketSearchHistory"
        payload = {
            "SessionID": self.session_id_store.value,
            "TicketID": "{0}".format(ticket_id),
        }
        self._result_type = self.ws_config[self.operation]["Result"]
        response = self._send_request(payload, ticket_id)
        res_json = json.loads(response.text)
        try:
            return res_json['TicketHistory'][0]['History']
        except KeyError as e:
            msg = 'пустой ответ от api TicketHistoryOtrs KeyError: {}'.format(e)
            print('error', msg)


def args_parse():
    parser = argparse.ArgumentParser()
    # Добавляем поддержку обработки тикета по TicketID
    parser.add_argument('-t', '--ticket', help='Ticket ID as seen in URL (TicketID=99641 = 99641)', type=str,
                        required=0)
    args = parser.parse_args()
    return args.ticket


def run(url, username, password, ticket=None):
    try:
        # Подключение к otrs
        otrs_client = Client(
            url,
            username,
            password,
            https_verify=HTTPS_VERIFY,
            webservice_config_ticket=WEBSERVICE_CONFIG_TICKET
        )
        try:
            otrs_client.session_restore_or_set_up_new()
        except (OtrsAuthException, Exception) as e:
            msg = '{}'.format(e)
            print('error', msg)
        # Получаем тикеты для синхронизации из otrs
        tickets = get_otrs_tickets_id(otrs_client, ticket)
        # Получаем тикеты для синхронизации из локальной базы данных
        other_tickets = [r.otrs_id for r in session.query(Ticket.otrs_id).filter_by(is_closed=False)]

        tickets_all = set(tickets + other_tickets)
        create_or_update_otrs_tickets(otrs_client, tickets_all)
        create_or_update_youtrack_issues(otrs_client, tickets_all)
    except Exception as e:
        traceback.print_exc()
        msg = 'ошибка автоматического запуска: {}'.format(e)
        print('error', msg, 'auto_run')


if __name__ == '__main__':
    ticket = args_parse()
    run(URL, USERNAME, PASSWORD, ticket)
