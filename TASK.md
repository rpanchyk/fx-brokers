Виконай аналітику форекс брокерів.

Основні пункти для аналізу:
- Головна сторінка (URL)
- Країна реєстрації
- Регуляції брокера (FCA, CySEC і тд)
- Типи рахунків (акаунтів) та їх комісії (Standard, Raw і тд)
- Свопи
- Потреба KYC
- Варіанти поповнення рахунку (deposit): Card (Visa/Mastercard), Bank transfer (IBAN), Crypto
- Варіанти зняття коштів з рахунку (withdrawal): Card (Visa/Mastercard), Bank transfer (IBAN), Crypto
- Наявність правила "Return to Source Rule" (виведення коштів на той же рахунок, з якого було виконано поповнення)
- Чи дозволена реєстрація для України? (багато брокерів мають це обмеження!)
- Підтримка MetaTrader 4, MetaTrader 5, cTrader
- Чи підходить для алго-трейдингу?

Список форекс брокерів:
- icmarkets
- gomarkets
- avatrade
- cptmarkets
- dooprime
- fxcm
- startrader
- tickmill
- tradenation
- vantagemarkets
- forex4you
- roboforex
- a-markets
- admiralmarkets
- fxpro
- pepperstone
- blackbull
- eightcap
- fpmarkets
- fusionmarkets

Потрібна повна аналітика по кожному брокеру зі списку.
Окремо створи зведену таблицю порівняння.
Збережи всі python-скрипти, за допомогою яких виконувалась робота.
Цей проект має бути повторюваним в майбутньому (повторюваний пайплайн).

Налаштування (config.yml):
- Можна змінювати пункти для аналізу (points)
- Можна змінювати список брокерів (brokers)
- output: filename_pattern, orientation, paper_size, language, title
- Дата зрізу = день запуску пайплайна (не фіксується в config.yml)

Результатом має бути PDF-файл "FxBrokers_YYYY-MM.pdf" з усією зібраною інформацією.
