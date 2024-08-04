# Anixart Playlist Extractor

Собирает плейлист для [VLC](videolan.org/vlc/index.ru.html).

## Зачем:
1. Так проще смотреть с ПК (ПК клиента то нет (вроде)). Нет необходимости в эмуляторах.
2. Так можно получить ссылки на видео заблокированного в регионе релиза. Без ВПН и прочих шаманств. Почти `:)`

## Установка:
```
git clone https://github.com/Greateapot/anixart-playlist-extractor.git
cd anixart-playlist-extractor
python3 -m pip install -e .
```

## Использование:

> [!TIP]
> Авторизация не требуется.

### Сборка плейлиста
```
axapex extract -rid RELEASE_ID -tid TYPE_ID -q QUALITY -o "path/to/output/dir"
```
1.  `RELEASE_ID` - идентификатор релиза. Его можно получить через кнопку "поделиться" справа от кнопки "смотреть" на странице релиза. Последнее число в ссылке - тот самый `RELEASE_ID`.
    Пример:
    ```
    Рекомендую посмотреть: «Магическая битва 0. Фильм»
    https://anixart.tv/release/18093
    ```

    18093 <-- `RELEASE_ID`
2.  `TYPE_ID` - идентификатор озвучки/субтитров. Его можно узнать с помощью команды `list-types` (Подробнее ниже).
3.  `QUALITY` - Качество видео. Доступно 3 варианта: 360, 480 и 720. По умолчанию стоит 720. 1080 нет т.к. я ни разу не видел такого качества на Kodik.
4. `"path/to/output/dir"` - Путь, куда будет сохранен плейлист, в формате `xspf`.

> [!IMPORTANT]  
> Плейлист работает ограниченное кол-во часов (я не знаю сколько). По истечении срока необходимо сгенерировать новый.


### Получение идентификатора озвучки
```
axapex list-types -rid RELEASE_ID -pm PAGES_MAX
```
1.  `RELEASE_ID` - аналогично. Опционально, если не указать `RELEASE_ID`, будет выведен список всех доступных озвучек и их идентификаторы.
2.  `PAGES_MAX` (Работает только с указанным `RELEASE_ID`) - максимальное кол-во страниц, которые надо обработать, чтобы получить точный список озвучек релиза. Используется в случае, если релиз недоступен в регионе. По умолчанию - 2 (более чем достаточно).