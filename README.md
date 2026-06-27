# FinanceCategorizer

Автоматическая категоризация расходов из BNP Paribas GOonline. Результат копируется в буфер обмена для вставки в таблицу.

## Структура

```
finance_categorizer/
├── __init__.py
├── crawler.py           # Playwright краулер для скачивания xlsx
├── formatter.py         # Сводная таблица по дням/категориям
├── detail.py            # Детальный просмотр транзакций
├── category_edit.py     # Редактирование категорий
└── categories.py        # Категории и фильтры
```

## Установка

```bash
pip install -r requirements.txt
playwright install chromium
```

Заполнить `.env`:
```
BANK_LOGIN=your_login
BANK_PASSWORD=your_password
```

## Использование

```bash
finance           # скачать xlsx (кеш 3ч) + сводная таблица
finance 15        # с 15-го числа
finance -f        # принудительно перекачать xlsx
```

### Детальный просмотр

```bash
financed 15            # все транзакции за 15-е число
financed Grocery       # все Grocery за текущий месяц
financed 15 Grocery    # Grocery за 15-е
```

### Редактирование категорий

```bash
financee "keyword" Rest      # добавить keyword в категорию Rest
```

### Только скачать xlsx

```bash
financec            # скачать (с кешем 3ч)
financec -f         # принудительно
financec --debug    # с видимым браузером
```

## Категории

Настраиваются в `finance_categorizer/categories.py`:

- **Grocery** — продукты (Lidl, Kaufland, Biedronka...)
- **Car&Fuel** — топливо, парковка, такси (Orlen, Bolt...)
- **Rest** — рестораны, хобби, развлечения (McDonald's, Zalipianki...)
- **Development** — обучение (Noblewings, экзамены...)
- **Clothes** — одежда (Peek & Cloppenburg, Reserved)
- **Gift** — подарки
- **Other** — всё остальное

## Фильтры

- `EXCLUDE_KEYWORDS` — исключить по описанию (налоги, подписки)
- `EXCLUDE_KEYWORD_AMOUNT` — исключить по описанию + сумме
- `EXCLUDE_AMOUNTS` — исключить по точной сумме
- `EXCLUDE_ACCOUNTS` — исключить переводы на эти счета
