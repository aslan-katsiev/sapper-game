# Sapper

![](['')

### What is Sapper
[Sapper](https://minesweeper.online/ru/) - компьютерная игра-головоломка,
в которой необходимо найти все мины на игровом поле,
используя числовые подсказки.

### Gameplay
В начале игры отображается игровое поле с закрытыми клетками.
Табло показывает общее количество непомеченных мин и время игры.
Когда игрок делает первый клик по одной из клеток, открывается несколько пустых клеток и клеток с числами.
Число на клетке обозначает количество мин вокруг неё, то есть в области 3×3 с центром в этой клетке.
Используя подсказки, игрок определяет точное местонахождение мин, помечая их флажком и открывая клетки без мин.
Для победы необходимо открыть все клетки без мин.
В случае, если игрок открывает клетку с миной, игра заканчивается поражением.

### Purpose of Buttons
- LMB - Открыть клетку
- RMB - Поставить флажок

### About the Project
Проект создан в учебных целях для Yandex Lyceum

#### Installation
pip install -r requirements.txt

#### Autor:
Aslan Dzeytov, young it-developer, 14 y.o.
#### Связаться можно с помощью почты:
katsiev.001@mail.ru