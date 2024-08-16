# Добавление элементов управления
Когда у нас есть рабочее окно приложения, в него хочется
что-нибудь добавить, например, текст.

За элементы интерфейса приложения отвечает поле `elements` класса приложения.
В нём хранятся все отображаемые элементы приложения.

Допустим, мы хотим добавить текст. Для этого нужно создать объект элемента:
```python
from gui.elements.text import Text

label = Text("Hello, world!")
```
Этот объект можно настраивать: менять позицию, размер и многое другое.
В случае с текстовым элементом, можно, например, поменять шрифт.

Когда всё готово, нужно добавить элемент в `elements`:
```python
from gui.abstract.app import Application
from gui.elements.text import Text


class App(Application):
    def on_start(self):
        self.elements.append(Text("Hello, world!"))

```
Если запустить приложение, мы увидим окно с нашей надписью.

Узнать полный список элементов управления и их параметры можно в [справочнике](../reference/controls.md)