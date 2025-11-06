# MAX University Bot — MVP

## Описание
Прототип чат-бота и мини-приложения для мессенджера MAX, решающего задачу цифровизации взаимодействия студентов и вуза:
- Быстрый доступ к расписанию и оценкам,
- Запрос официальных документов (справки, выписки),
- Открытие IT/административных тикетов.

## Файлы в проекте
- `app.py` — Flask приложение (вебхук + мини-приложение).
- `Dockerfile` — контейнеризация.
- `requirements.txt` — зависимости.
- `presentation.pptx` — презентация проекта.
- `.env.example` — пример переменных окружения.

## Переменные окружения
Создайте файл `.env` или задайте переменные при запуске:
- `MAX_TOKEN` — секретный токен для верификации вебхуков (например, от MAX).
- `PORT` — порт приложения (по умолчанию 8080).

## Запуск локально (без Docker)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export MAX_TOKEN="your-max-token"
python app.py
# приложение будет доступно на http://localhost:8080
```

## Сборка и запуск в Docker
Сборка образа:
```bash
docker build -t max-unibot:latest .
```

Запуск контейнера (локально, пример):
```bash
docker run -e MAX_TOKEN="your-max-token" -p 8080:8080 max-unibot:latest
```

## Как протестировать webhook (пример локально)
Используйте `curl`:
```bash
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -H "X-MAX-TOKEN: demo-token" \
  -d '{"user_id":"u1","text":"start"}'
```

Пример получения расписания (после авторизации id):
```bash
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -H "X-MAX-TOKEN: demo-token" \
  -d '{"user_id":"u1","text":"id 12345"}'
```

## Как интегрировать с MAX messenger
1. Зарегистрируйте webhook URL в кабинете разработчика MAX (например `https://yourdomain.com/webhook`).
2. Установите `MAX_TOKEN` и настройте верификацию подписи/поля, который использует MAX.
3. Для мини-приложения используйте `/mini` как страницу, которую можно открыть из интерфейса бота.

## Ограничения MVP
- Демонстрационная in-memory база данных. В продакшене — интеграция с SIS (Student Information System).
- Нет аутентификации через OAuth — используется простая проверка ID (для MVP).
- Логика команд минимальна для быстрого прототипирования.
