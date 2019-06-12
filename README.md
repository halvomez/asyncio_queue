# test aiohttp app

#### 1. Установить пакеты
```
pip install -r requirements.txt
```
#### 2. Запустить приложение
```
    python main.py
```
Дополнительно в конфиге можно указать порт для запуска приложения.

#### 3. Описание работы

Реализовано 2 запроса:
<li> /add_task
<li> /get_tasks


add_task добавляет задачу на расчет прогрессии в очередь. Очередь по длине не ограничена.

get_tasks получает отсортированный список задач в очереди на текущий момент.

Сортировка задач идет по времени добавления задачи в очередь, начиная с самой ранней.
Выполняемая задача, которую worker считает в настоящее время, имеет статус 'in_progress' и динамически показывает текущие добавленные элементы прогрессии.
Как только расчет прогрессии завершен, т.е. необходимое количество элементов получено, задача удаляется из очереди, и worker получает следующую.

Количество одновременно запущенных воркеров, которые параллельно ведут расчет отдельных задач,
указывается в конфиге.

