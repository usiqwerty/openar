# Интерфейс пользователя

В графическом интерфейсе есть два типа элементов - виджеты и приложения

Стоит понимать разницу между разными элементами интерфейса
## Виджеты
Небольшие окна с информацией, не перехватывают фокус
Виджеты нужны для отображения информации и, возможно, для простого вида ввода (например виджет-кнопка)
## Приложения
В отличие от виджетов, приложения:
 - имеют элементы управления окном 
 - могут работать в отдельном потоке
 - ~~приложения могут обрабатывать получение и потерю фокуса~~ (пока не реализовано)
 

## Создание элементов интерфейса
Для работы с графическим интерфейсом используется пакет gui

Чтобы создать виджет или приложение нужно объявить свой класс, унаследованный от `gui.abstract.widget.Widget`

Класс должен реализовывать метод `render`, который рисует сам элемент.
Также при необходимости можно реализовать обработчики событий (например ~~`on_click`~~, ~~`on_start`~~).