# Автоматиизированное управление бекапами. 
- Выгрузка в хранилище файлов в сети и на внешний FTP сервер.
- Чистка старых бекапов с требуемым разрежением.

Для работы требуется создать в корне проекта файл `.env` со значениями переменных окружения.

Пример заполнения в файле `.env.example`

## config.py
DATABASE_DIRS - настройка списка баз и имен папок. 
  'mssql' - имя папки базы на сервере СУБД, где создаются бекапы.
  'storage' - имя папки базы в хранилище файлов
  'ftp' - имя папки базы на сервере FTP
BACKUPS_AGE_SETTINGS_STORAGE - настройка плотности бекапов в хранилище файлов для автоматической чистки старых. Каждый элемент списка описывает период глубины хранения и плотность бекапов.
BACKUPS_AGE_SETTINGS_MSSQL - настройка плотности бекапов на локальном диске СУДБ для автоматической чистки старых. Каждый элемент списка описывает период глубины хранения и плотность бекапов.
BACKUPS_COUNT_PER_DAY - количество бекапов в день для каждоый базы, для ежедневного контроля.

**Заполнение данных учетных записей ftp `FTP_READER` и `FTP_FULL_READER` не обязательны.**

## backup_manager.py
**Скрипт для запуска переноса и чистки бекапов.**

**Использование:**<br>
`backup_manager.py [-h] [-d dd.mm.yyyy] [--only_transport] [--only_cleaning]`<br>

*   -h, --help        Показать опции и использование
*   -d dd.mm.yyyy     Дата бекапов для обработки. Если не указано, то текущая дата
*   --only_transport  Выполнить только перенос бекапов
*   --only_cleaning   Выполнить только чистку бекапов


## evening_announce.py
**Скрипт для вечернего оповещения, чтобы знать что задание создания бекапов выполнено**

## backups_checker.py
**Проверка количества бекапов в хранилище или ftp. Для дополнительного контроля.**

**Использование:**<br>
`backups_checker.py [-h] [-d dd.mm.yyyy] storage_type`
*   storage_type   Местоположение для проверки "storage" или "ftp"
*   -h, --help     Показать опции и использование
*   -d dd.mm.yyyy  Дата бекапов для проверки. Если не указано, то текущая дата
