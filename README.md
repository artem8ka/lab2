# Лабораторная работа №2
## Потоковый анализатор файлов
### Для использования утилиты в консоли:
+ Открыть терминал в корень репрозитория
+ Создать виртуальное окружение
```bash
python -m venv .venv
```
+Активировать виртуальное окружение
```bash
.\.venv\Scripts\Activate.ps1
#если отказано, разрешить для текущего окна терминала и повторить попытку
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
+ Установить пакет
```bash
python -m pip install -e .
```
### Команды:
```bash
python -m pytest #запускает тесты
python -m ruff check #проверка ruff
python -m streamstats --help #справка
#анализ логов в файлах INPUT, создает отчет REPORT.json
python -m streamstats analyze INPUT[INPUT ...] --format csv|jsonl --output REPORT.json
#флаг --skip-invalid пропускает невалидные события и записывает предупреждения в лог
python -m streamstats analyze INPUT[INPUT ...] --format csv|jsonl --output REPORT.json --skip-invalid
```