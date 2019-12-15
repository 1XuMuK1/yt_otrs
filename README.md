# yt_otrs
Integration YouTrack with OTRS v6

# Задача интеграции Youtrack + OTRS

Есть две системы, у каждой из которых есть свой API

# Youtrack - система ведения задач для разработчиков:
- тикеты
- комментарии

https://www.jetbrains.com/help/youtrack/standalone/youtrack-rest-api-reference.html
https://devopshq.github.io/youtrack/

# OTRS - система тикетов для второй линии поддержки
- Очереди тикетов
- Тикеты
- комментарии ( Article )

https://doc.otrs.com/doc/api/otrs/6.0/Perl/
https://pypi.org/project/PyOTRS/

## Необходимо:
- чтобы эскалированные новые тикеты OTRS попадали как задачи в Youtrack в определенный проект
- Комментарии/файлы сделанные в Youtrack попадали в OTRS в соотв задачи
- Комментарии/файлы сделанные в OTRS попадали в Youtrack в соотв задачи


## Команда для запуска
(otrs-youtrack-env) > $ alembic upgrade head (миграции моделей бд)

(otrs-youtrack-env) > $ python auto_run.py

Если не указывать Ticket ID, то будут использоваться эскалированные новые тикеты и тикеты, которые есть сохраненные и не закрытые в локальной базе данных.

