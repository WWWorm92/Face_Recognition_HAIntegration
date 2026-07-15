# Face Recognition Bridge for HACS

Этот репозиторий содержит только Home Assistant интеграцию `face_recognition_bridge`.

## Установка

1. Добавь репозиторий в HACS как `Integration`.
2. Установи `Face Recognition Bridge`.
3. Перезапусти Home Assistant.
4. Добавь интеграцию через `Settings -> Devices & Services`.

## Настройка

При добавлении интеграции укажи:

- `base_url` - адрес backend API;
- `api_token` - токен backend, если он включен;
- `scan_interval` - интервал опроса.

## Что делает интеграция

- читает `latest_event` из backend API;
- создает сенсоры с последним человеком, камерой и score;
- шлет события в Home Assistant:
  - `face_recognition_match`
  - `face_recognition_unknown`

## Backend

Backend вынесен в отдельный проект и должен жить отдельно от HACS-репозитория.
