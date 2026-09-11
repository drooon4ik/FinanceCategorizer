# FinanceCategorizer

Автоматическая категоризация расходов из BNP Paribas GOonline. Результат копируется в буфер обмена для вставки в таблицу.

## Структура

```
finance_categorizer/
├── __init__.py
├── cli.py               # Единая точка входа (флаги -d, -e, -i)
├── crawler.py           # Playwright краулер для скачивания xlsx
├── formatter.py         # Сводная таблица по дням/категориям
├── detail.py            # Детальный просмотр транзакций
├── category_edit.py     # Редактирование категорий
├── ignore_edit.py       # Временное игнорирование транзакций
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
finance -p        # сводная таблица за предыдущий месяц
finance -p 10     # за предыдущий месяц с 10-го числа
```

### Детальный просмотр

```bash
finance -d 15            # все транзакции за 15-е число
finance -d Grocery       # все Grocery за текущий месяц
finance -d 15 Grocery    # Grocery за 15-е
finance -d -p            # все транзакции за предыдущий месяц
finance -d -p Grocery    # Grocery за предыдущий месяц
finance -d -p 15         # транзакции за 15-е предыдущего месяца
```

### Редактирование категорий

```bash
finance -e "keyword" Rest      # добавить keyword в категорию Rest (temp, 2 месяца)
```

### Временное игнорирование транзакций

```bash
finance -i "keyword"           # игнорировать транзакции с keyword (temp, 2 месяца)
finance -i "keyword" 5.00      # игнорировать по keyword + сумме
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
