from datetime import datetime
import sys
import os
from sqlalchemy.orm.exc import NoResultFound

from helpers.models import session
from helpers.models import Ticket, Article, Attachment

from yt import (
    youtrack_create_issue,
    youtrack_create_issuecomment,
    youtrack_create_issueattachment
)


def get_otrs_tickets_id(otrs_client, ticket=None):
    tickets = []
    if ticket:
        tickets.append(ticket)
        return tickets

    # filter only escalation and new
    tickets = otrs_client.ticket_search(
        StateIDs=[1, 4, 6],
        QueueIDs=[13]
    )
    tickets.extend(otrs_client.ticket_search(
        TicketEscalationTimeOlderDate=datetime.now(),
        StateType='new',
    ))
    return tickets


def add_in_db_ticket(ticket_id, otrs_ticket, ticket_history):
    # Проверяем есть ли этот тикет в нашей локальной базе данных
    try:
        # Update the ticket in local database
        local_ticket = session.query(Ticket).filter_by(otrs_id=str(ticket_id)).one()
    except NoResultFound:
        # create a new ticket in local database
        local_ticket = Ticket(
            title=otrs_ticket.field_get("Title"),
            otrs_ticket_number=otrs_ticket.field_get("TicketNumber"),
            otrs_id=str(ticket_id),
            date_create=otrs_ticket.field_get("Created"),
            date_update=otrs_ticket.field_get("Changed"),
            is_closed=False,
            #  записываем id предпоследней очереди в бд
            queueid=ticket_history[-2]['QueueID'],
            stateid=ticket_history[-2]['StateID']
        )
        session.add(local_ticket)
        session.commit()
        # Отправляем новый тикет в youtrack
        youtrack_create_issue(local_ticket)
    return local_ticket


def add_in_db_article(article, local_ticket):
    # Проверяем есть ли этот Article в нашей локальной базе данных
    try:
        # Update the Article in local database
        local_article = session.query(Article).filter_by(otrs_id=str(article.get('ArticleID'))).one()
    except NoResultFound:
        # create a new Article in local database
        local_article = Article(
            ticket_id=local_ticket.id,
            otrs_from=article.get('From'),
            title=article.get('Subject'),
            body=article.get('Body'),
            otrs_id=article.get('ArticleID'))
        session.add(local_article)
        session.commit()

        # Отправляем OtrsArticle как комментарий к задаче в youtrack
        youtrack_create_issuecomment(local_article)
    return local_article


def check_attachments(article, local_article, ticket_number):
    try:
        for file in article['Attachment']:
            # Проверяем есть ли этот файл в нашей локальной базе данных
            try:
                # Update the Attachment in local database
                local_attachment = session.query(Attachment).filter_by(
                    article_id=local_article.id,
                    filename=file.get('Filename')
                ).one()
            except NoResultFound:
                # create a new Attachment in local database
                local_attachment = Attachment(
                    article_id=local_article.id,
                    filename=file.get('Filename'),
                    filepath=os.path.join(ticket_number, 'files', file.get('Filename')))
                session.add(local_attachment)
                session.commit()

                # Отправляем прикрепление в youtrack
                content = file['Content']
                youtrack_create_issueattachment(local_attachment, content)
    except KeyError:
        pass


def create_or_update_otrs_tickets(otrs_client, tickets):
    for ticket_id in tickets:
        # получаем историю по данному тикету
        ticket_history = otrs_client.get_history(ticket_id)
        otrs_ticket = otrs_client.ticket_get_by_id(ticket_id, articles=True, attachments=True, dynamic_fields=True)
        data = otrs_ticket.to_dct()
        if len(data) < 1:
            msg = 'No valid json data found'
            print('error ', msg)
            sys.exit(1)
        ticket_number = data['Ticket']['TicketNumber']
        ticket_data = data['Ticket']
        local_ticket = add_in_db_ticket(ticket_id, otrs_ticket, ticket_history)

        # Перебираем все Article
        for article in ticket_data['Article']:
            local_article = add_in_db_article(article, local_ticket)
            # Обрабатываем прикрепленные файлы
            check_attachments(article, local_article, ticket_number)
