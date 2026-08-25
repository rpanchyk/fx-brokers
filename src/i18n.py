# -*- coding: utf-8 -*-
"""UI strings for PDF report (uk | en). Broker research notes stay in data/brokers.yaml."""

from __future__ import annotations

from typing import Any


STRINGS: dict[str, dict[str, str]] = {
    "uk": {
        "cover_kicker": "ДОСЛІДЖЕННЯ  ·  РИТЕЙЛ FOREX / CFD",
        "cover_compare": "Порівняння {n} брокерів  ·  період {period}",
        "cover_topics": "Регуляція · рахунки · KYC · платежі · RTS · Україна · платформи · алго",
        "cover_brokers": "БРОКЕРИ В ОГЛЯДІ",
        "cover_src1": "Джерела: офіційні сайти, політики депозитів/виведень, restricted-списки, регуляторні реєстри.",
        "cover_src2": "Умови залежать від країни клієнта та юридичної особи (entity). Не є інвестиційною рекомендацією.",
        "header": "Аналітика форекс-брокерів  ·  {period}",
        "header_right": "Відкриті джерела",
        "footer": "Не є інвестиційною рекомендацією. Умови залежать від юрисдикції та entity.",
        "yes": "Так",
        "no": "Ні",
        "partial": "Частково",
        "sec_method": "1. Методологія",
        "method_body": (
            "Звіт зібрано {as_of} за офіційними сайтами, політиками депозитів/виведень, "
            "restricted-списками та регуляторними реєстрами. Усі бренди працюють через кілька юридичних осіб. "
            "<b>Регуляція, плече, комісії, методи оплати, крипто і навіть доступність для України залежать "
            "від entity, на яку вас онбордять.</b> Перед депозитом читайте клієнтську угоду саме тієї компанії "
            "і перевіряйте ліцензію в реєстрі регулятора."
        ),
        "ua_sub": "Реєстрація з України",
        "ua_body": (
            "Багато брокерів прямо виключають Ukraine у restricted-списку (часто разом із USA/Russia) — "
            "навіть якщо бренд «глобальний». Окремо: Крим і окуповані території майже всюди блокують через "
            "санкції. З боку України діють валютні обмеження НБУ для фізосіб (карткові ліміти, обмежений "
            "SWIFT на іноземні брокерські рахунки) — це не політика брокера, а банківський контур. "
            "Наявність IBAN у брокера не гарантує, що український банк проведе SWIFT-платіж."
        ),
        "legend": (
            "Легенда: <b>Так</b> — підтверджено для основної міжнародної пропозиції; <b>Ні</b> — відсутнє або "
            "країна в restricted; <b>Частково</b> — залежить від entity/країни або лімітів (картка лише на суму депозиту). "
            "Список брокерів і пунктів аналізу задається файлом <b>config.yml</b>."
        ),
        "corpus_note_en": "",
        "sec_findings": "2. Короткі висновки",
        "kpi_brokers": "брокерів у звіті",
        "kpi_ua_yes": "UA — так",
        "kpi_ua_no": "UA — ні",
        "kpi_ua_part": "UA — частково",
        "kpi_raw": "з Raw/ECN у описі",
        "kpi_ct": "з cTrader зараз",
        "th_broker": "Брокер",
        "th_comment": "Коментар",
        "crimea_note": "Крим та окуповані території виключені майже в усіх брокерів через міжнародні санкції.",
        "best_fits": "Найкращі збіги (за увімкненими пунктами)",
        "rec_algo_ct": "<b>Алго + cTrader:</b> {names}. З них для України: {ua_names}.",
        "rec_ua_yes": "<b>Україна так:</b> {names}.",
        "rec_ua_no": "<b>Україна ні:</b> {names}.",
        "rec_ua_part": "<b>Україна частково:</b> {names}.",
        "rec_crypto": "<b>Крипто-депозит (так):</b> {yes}. <b>Ні:</b> {no}. <b>Частково:</b> {partial}.",
        "sec_compare": "3. Зведена таблиця порівняння",
        "sub_identity": "3.1. Сайт, країна, регуляція",
        "th_home": "Головна сторінка",
        "th_country": "Країна / HQ",
        "th_regs": "Регуляції",
        "sub_accounts": "3.2. Рахунки, комісії, свопи",
        "th_accounts": "Рахунки та комісії",
        "th_swaps": "Свопи",
        "accounts_caption": "Комісії — публічні «from». All-in cost міряйте на демо конкретного entity.",
        "sub_kyc": "3.3. KYC",
        "th_kyc": "KYC",
        "kyc_default": "Обов’язковий",
        "sub_pay": "3.4. Депозит, виведення, Return to Source",
        "th_dep_card": "Dep Card",
        "th_dep_iban": "Dep IBAN",
        "th_dep_crypto": "Dep Crypto",
        "th_wd_card": "Wd Card",
        "th_wd_iban": "Wd IBAN",
        "th_wd_crypto": "Wd Crypto",
        "th_rts": "RTS",
        "pay_caption": (
            "Card = Visa/Mastercard. Bank IBAN = міжнародний SWIFT/SEPA з IBAN (не лише локальний BPAY). "
            "RTS є індустріальним AML-правилом: картка майже ніколи не приймає прибуток понад депозит."
        ),
        "th_pay_details": "Деталі платежів / RTS",
        "sub_ukraine_tbl": "3.5. Доступ з України",
        "th_ukraine": "Україна",
        "sub_algo": "3.6. Платформи і алго-трейдинг",
        "th_algo": "Алго",
        "th_mt4": "MT4",
        "th_mt5": "MT5",
        "th_ct": "cTrader",
        "algo_caption": "cTrader у RoboForex закрито 08.2023. У CPT — лише на частині групи. У AMarkets і Admirals на офіційній головній — MT4/MT5.",
        "sec_profiles": "4. Повні профілі брокерів",
        "profiles_intro": (
            "Картка кожного бренду нижче повторює лише пункти, увімкнені в config.yml. "
            "Якщо ви резидент UK / EEA / Австралії, плече і платежі будуть інші, ніж на Seychelles/BVI."
        ),
        "founded": "Засновано",
        "hq": "HQ",
        "site": "Сайт",
        "pay_card": "Card",
        "pay_iban": "Bank IBAN",
        "pay_crypto": "Crypto",
        "sec_advice": "5. Практичні рекомендації",
        "advice_ua": "5.1. Якщо ви в Україні",
        "advice_general": "5.1. Як обирати",
        "advice_avoid": "Не витрачайте час на бренди з <b>Україна — ні</b>: {names}.",
        "advice_shortlist": (
            "Робочий шортліст для алго серед доступних в UA з cTrader: {ct}. "
            "Без cTrader, але з Raw/ECN: {raw}. Offshore / слабший захист: перевіряйте entity."
        ),
        "advice_partial": "Статус «частково» ({names}): обов’язково дропдаун реєстрації й compliance перед депозитом.",
        "advice_test": "Тестуйте мале виведення до робочого капіталу. Картковий депозит обмежить карткове виведення сумою principal.",
        "advice_swift": "SWIFT з українського банку на IBAN брокера може не пройти через ліміти НБУ — плануйте картку / e-wallet / крипто, якщо брокер їх приймає.",
        "advice_rts": "5.2. Return to Source",
        "rts_b1": "Не змішуйте багато методів на одному рахунку.",
        "rts_b2": "Картка рідко приймає прибуток понад депозит — прибуток плануйте на IBAN або той самий e-wallet/крипто.",
        "rts_b3": "Ім’я на картці/IBAN/гаманці = ім’я в KYC.",
        "sec_limits": "6. Обмеження звіту",
        "limits_body": (
            "Restricted-списки змінюються без публічного анонсу. Статуси «частково» означають суперечливі або "
            "entity-залежні джерела. Комісії в оглядах можуть різнитися на $1–4 RT. "
            "Платіжні методи інколи рендеряться динамічно. Звіт не замінює due diligence і не є офертою."
        ),
        "sec_sources": "7. Основні джерела",
        "src_official": "Офіційні сайти зі стовпця «Головна сторінка» (funding, withdrawal, regulation, restricted countries).",
        "src_ua_yes": "Підтвердження доступності UA (серед інших): {names}.",
        "src_ua_no": "Офіційні / оглядові restricted-списки з Ukraine: {names}.",
        "src_extra": "Tickmill / FxPro / Pepperstone deposit-withdrawal і RTS-політики; RoboForex news про припинення cTrader (08.2023).",
        "pipeline": "Пайплайн: змініть brokers/points у config.yml і запустіть python run.py",
        "point_homepage": "Головна сторінка",
        "point_country": "Країна реєстрації",
        "point_regulations": "Регуляції",
        "point_ukraine": "Реєстрація для України",
        "point_algo": "Алго-трейдинг",
        "point_accounts": "Рахунки та комісії",
        "point_swaps": "Свопи",
        "point_kyc": "KYC",
        "point_platforms": "Платформи",
        "point_deposit": "Поповнення",
        "point_withdrawal": "Виведення",
        "point_rts": "Return to Source Rule",
        "none": "—",
        "none_listed": "немає",
    },
    "en": {
        "cover_kicker": "RESEARCH  ·  RETAIL FOREX / CFD",
        "cover_compare": "Comparing {n} brokers  ·  period {period}",
        "cover_topics": "Regulation · accounts · KYC · payments · RTS · Ukraine · platforms · algo",
        "cover_brokers": "BROKERS IN THIS REPORT",
        "cover_src1": "Sources: official websites, deposit/withdrawal policies, restricted-country lists, regulator registers.",
        "cover_src2": "Terms depend on client country and legal entity. Not investment advice.",
        "header": "Forex broker analytics  ·  {period}",
        "header_right": "Open sources",
        "footer": "Not investment advice. Terms depend on jurisdiction and entity.",
        "yes": "Yes",
        "no": "No",
        "partial": "Partial",
        "sec_method": "1. Methodology",
        "method_body": (
            "Compiled {as_of} from official sites, funding/withdrawal policies, restricted-country lists, "
            "and regulator registers. Brands operate via multiple legal entities. "
            "<b>Regulation, leverage, fees, payment methods, crypto and Ukraine availability depend on the "
            "onboarding entity.</b> Read the client agreement for that company and verify the licence."
        ),
        "ua_sub": "Registration from Ukraine",
        "ua_body": (
            "Many brokers list Ukraine on a restricted list (often with USA/Russia), even when the brand looks "
            "“global”. Crimea and occupied territories are blocked almost everywhere due to sanctions. "
            "Separately, NBU wartime FX limits for individuals (card caps, limited SWIFT to foreign brokers) "
            "are bank-side, not broker policy. An IBAN at the broker does not guarantee a Ukrainian bank will send SWIFT."
        ),
        "legend": (
            "Legend: <b>Yes</b> — confirmed for the main international offer; <b>No</b> — absent or country restricted; "
            "<b>Partial</b> — entity/country dependent or capped (card withdrawals often limited to deposited principal). "
            "Brokers and analysis points are controlled by <b>config.yml</b>."
        ),
        "corpus_note_en": (
            "Note: free-text research notes in broker profiles are authored in Ukrainian in data/brokers.yaml; "
            "report chrome, status labels and generated summaries are English when language=en."
        ),
        "sec_findings": "2. Key findings",
        "kpi_brokers": "brokers in report",
        "kpi_ua_yes": "UA — yes",
        "kpi_ua_no": "UA — no",
        "kpi_ua_part": "UA — partial",
        "kpi_raw": "with Raw/ECN in profile",
        "kpi_ct": "with cTrader now",
        "th_broker": "Broker",
        "th_comment": "Comment",
        "crimea_note": "Crimea and occupied territories are excluded by almost all brokers due to sanctions.",
        "best_fits": "Best fits (from enabled points)",
        "rec_algo_ct": "<b>Algo + cTrader:</b> {names}. Of these available in Ukraine: {ua_names}.",
        "rec_ua_yes": "<b>Ukraine yes:</b> {names}.",
        "rec_ua_no": "<b>Ukraine no:</b> {names}.",
        "rec_ua_part": "<b>Ukraine partial:</b> {names}.",
        "rec_crypto": "<b>Crypto deposit (yes):</b> {yes}. <b>No:</b> {no}. <b>Partial:</b> {partial}.",
        "sec_compare": "3. Comparison tables",
        "sub_identity": "3.1. Website, country, regulation",
        "th_home": "Homepage",
        "th_country": "Country / HQ",
        "th_regs": "Regulations",
        "sub_accounts": "3.2. Accounts, commissions, swaps",
        "th_accounts": "Accounts & commissions",
        "th_swaps": "Swaps",
        "accounts_caption": "Commissions are public “from” figures. Measure all-in cost on a demo for your entity.",
        "sub_kyc": "3.3. KYC",
        "th_kyc": "KYC",
        "kyc_default": "Mandatory",
        "sub_pay": "3.4. Deposit, withdrawal, Return to Source",
        "th_dep_card": "Dep Card",
        "th_dep_iban": "Dep IBAN",
        "th_dep_crypto": "Dep Crypto",
        "th_wd_card": "Wd Card",
        "th_wd_iban": "Wd IBAN",
        "th_wd_crypto": "Wd Crypto",
        "th_rts": "RTS",
        "pay_caption": (
            "Card = Visa/Mastercard. Bank IBAN = international SWIFT/SEPA with IBAN (not local BPAY alone). "
            "RTS is standard AML: cards almost never accept profits above deposited principal."
        ),
        "th_pay_details": "Payment / RTS details",
        "sub_ukraine_tbl": "3.5. Ukraine access",
        "th_ukraine": "Ukraine",
        "sub_algo": "3.6. Platforms and algo trading",
        "th_algo": "Algo",
        "th_mt4": "MT4",
        "th_mt5": "MT5",
        "th_ct": "cTrader",
        "algo_caption": "RoboForex discontinued cTrader in Aug 2023. CPT: entity-dependent. AMarkets and Admirals official homepages list MT4/MT5.",
        "sec_profiles": "4. Full broker profiles",
        "profiles_intro": (
            "Each card below includes only points enabled in config.yml. "
            "UK / EEA / Australia residents will see different leverage and payment rails than Seychelles/BVI."
        ),
        "founded": "Founded",
        "hq": "HQ",
        "site": "Website",
        "pay_card": "Card",
        "pay_iban": "Bank IBAN",
        "pay_crypto": "Crypto",
        "sec_advice": "5. Practical recommendations",
        "advice_ua": "5.1. If you are in Ukraine",
        "advice_general": "5.1. How to choose",
        "advice_avoid": "Skip brands with <b>Ukraine — no</b>: {names}.",
        "advice_shortlist": (
            "Algo shortlist among UA-available brokers with cTrader: {ct}. "
            "Raw/ECN without cTrader: {raw}. Treat offshore entities as weaker protection."
        ),
        "advice_partial": "“Partial” status ({names}): always check the registration dropdown and compliance before funding.",
        "advice_test": "Test a small withdrawal before committing capital. Card deposits usually cap card withdrawals at principal.",
        "advice_swift": "SWIFT from a Ukrainian bank to a broker IBAN may fail under NBU limits — plan card / e-wallet / crypto if the broker accepts them.",
        "advice_rts": "5.2. Return to Source",
        "rts_b1": "Avoid mixing many funding methods on one account.",
        "rts_b2": "Cards rarely accept profits above deposit — plan profits to IBAN or the same e-wallet/crypto.",
        "rts_b3": "Card/IBAN/wallet name must match KYC name.",
        "sec_limits": "6. Report limitations",
        "limits_body": (
            "Restricted lists change without public notice. “Partial” means conflicting or entity-dependent sources. "
            "Published commissions may differ by $1–4 RT across reviews. Payment methods can be rendered dynamically. "
            "This report is not due diligence and not an offer."
        ),
        "sec_sources": "7. Main sources",
        "src_official": "Official sites from the Homepage column (funding, withdrawal, regulation, restricted countries).",
        "src_ua_yes": "Ukraine availability references (among others): {names}.",
        "src_ua_no": "Official / review restricted lists including Ukraine: {names}.",
        "src_extra": "Tickmill / FxPro / Pepperstone funding & RTS policies; RoboForex notice on cTrader shutdown (Aug 2023).",
        "pipeline": "Pipeline: edit brokers/points in config.yml and run python run.py",
        "point_homepage": "Homepage",
        "point_country": "Country of registration",
        "point_regulations": "Regulations",
        "point_ukraine": "Ukraine registration",
        "point_algo": "Algo trading",
        "point_accounts": "Accounts & commissions",
        "point_swaps": "Swaps",
        "point_kyc": "KYC",
        "point_platforms": "Platforms",
        "point_deposit": "Deposit",
        "point_withdrawal": "Withdrawal",
        "point_rts": "Return to Source Rule",
        "none": "—",
        "none_listed": "none",
    },
}


class I18n:
    def __init__(self, language: str):
        lang = (language or "uk").lower()
        if lang not in STRINGS:
            lang = "uk"
        self.lang = lang
        self._s = STRINGS[lang]

    def t(self, key: str, **kwargs: Any) -> str:
        if key not in self._s:
            raise ValueError(f"Missing i18n key {key!r} for language={self.lang}")
        text = self._s[key]
        if kwargs:
            return text.format(**kwargs)
        return text

    def status(self, value) -> str:
        if isinstance(value, bool):
            return self.t("yes") if value else self.t("no")
        v = str(value or "").strip().lower()
        if v in ("yes", "так", "true", "1"):
            return self.t("yes")
        if v in ("no", "ні", "false", "0"):
            return self.t("no")
        return self.t("partial")

    def point_title(self, point_id: str, config_label: str | None = None) -> str:
        if self.lang == "en":
            return self._s.get(f"point_{point_id}") or config_label or point_id
        return config_label or point_id
