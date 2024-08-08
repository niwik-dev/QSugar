<link href='https://fonts.googleapis.com/css?family=Noto Sans' rel='stylesheet'>
<link href="
https://cdn.jsdelivr.net/npm/jetbrains-mono@1.0.6/css/jetbrains-mono.min.css
" rel="stylesheet">

<h1 style="text-align: center;">QSugar🌱</h1>

<div style="text-align:center; letter-spacing: 0.05em;">
    Reactive PySide framework,simple and friendly
</div>

<h2>
    Language🌐
</h2>

[简体中文](README_zh.md) &nbsp;[English](README.md)
<h2>
    Install🛠️
</h2>

```bash
   pip install QSugar
```

<h2>
    Explain🗂️
</h2>

<h3> Introduce </h3>

<p>
    QSugar is a PySide framework for efficiently building and reactive interfaces.  It learns from the concepts of excellent frameworks mainly Vue. The development of QtQuick technology confirms that the Qt metatype system gives Qt unlimited potential for declarative UI. QSugar was conceived and boldly attempted on this basis.
</p>

<p>
    If you don’t understand the concept of Vue framework, you can read the following documents
</p>

> [Vue Document](https://vuejs.org/guide)

<h2>
    Get Started Quickly🖐️
</h2>

<span>This is an example of a counter. You can understand how it differs from the traditional development model.<span>

```python
import sys

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel

from QSugar import Batch, DSL, Ref, Computed, Bind, Row, Column

Batch(DSL)(QWidget, QPushButton)
Batch(Bind)(QLabel)

count = Ref(1)
countText = Computed(globals())


@countText
def getTip():
    return f'The number is {count.value}.'


app = QApplication(sys.argv)

widget = QWidget(
    child=Row(
        children=[
            QLabel(
                alignment=Qt.AlignmentFlag.AlignCenter,
                text=countText
            ),
            Column(
                children=[
                    QPushButton(
                        text='+1',
                        clicked=lambda: count << count.value + 1
                    ),
                    QPushButton(
                        text='-1',
                        clicked=lambda: count << count.value - 1
                    )
                ]
            )
        ]
    )
)
widget.show()

app.exec()
```
<p>

QSugar enhances existing classes of QtWidgets with decorators, register with `Batch(DSL)(...)` . At the same time, properties are packaged and calculated with the help of `Ref` and `Computed` classes. For details, see <a> reactive programming</a>.

QSugar uses DSL syntax and responsive objects to quickly build UI interfaces. Please note! QSugar supports more than one </strong> DSL syntax and is designed independently of reactive programming. <br/>

If you don't care about DSL syntax, reactive programming is applicable. For example:
</p>

```python
import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from QSugar import Ref

btnText = Ref('Click Me!')

app = QApplication(sys.argv)
widget = QPushButton()
widget.setText(btnText)
widget.show()

# Modify the text content of the button
btnText << 'Modified'

app.exec()
```
<p>
    Minimizing the intrusion of the PySide framework as much as possible is one of the principles of QSugar framework design. As its name suggests, if the traditional development model is compared to coffee, QSugar is like a sugar cube. The functions you need are added and the functions you don’t need are shelved.
</p>

<p>
    Supported layout DSL syntax includes：
    <ul>
        <li>
            __init__method and property
        </li>
        <li>Fluent API</li>
        <li>qtml file parsing (in experiment)</li>
        <li>with statement (not in practice)</li>
    </ul>
</p>

<p>

The project plans to develop the `dsl-cli` command line tool in the future to facilitate conversion between different DSL syntaxes and reduce the compatibility burden. For a detailed introduction, see <a>DSL Syntax</a>.

</p>

<h2>
    Help Document📘
</h2>

<p>

Currently there is only md file, see [GitHub Document](DOCUMENT.md).

</p>

<h2>
    FAQ❓
</h2>

<p>
Q:Why is the old project deleted？

A:The widget enhancement idea of QSugar's old design is Mixin injection. Python has general support for Mixin features, and its behaviors that do not meet expectations often occur. For example, the DSL enhancement in old design is implemented by inheriting BaseDSLMixin. Method proxies (especially events) of subclasses of enhanced classes often fail, causing a lot of problems in development, so this project is rewritten from scratch with decorators.

Q: Why is it not compatible with PyQt?

A: QSugar currently only supports PySide. Since the binding of PyQt is very different from PySide, there are such problems：

(1) Although PyQt object property can be set in the __init__ method, the corresponding setter method will not be triggered. Although it can be solved through reflection, since setting property/binding signals is a high-frequency operation in UI construction, the method of frequent reflection to obtain the setter will cause serious performance problems. (After testing, page jam often occur)

(2) The sip binding used by PyQt lacks shiboken support for the middle layer of Python , resulting in many features unavailable. For example, when using a decorator proxy method/class, inexplicable exceptions will occur in some methods (suspected memory release and function addressing issues).
</p>

<h2>
    Support Project👍
</h2>

<p>
If you think the project is valuable, please give the project a Star⭐, thank you!

If you buy a cup of hot cocoa for the sewer rat 

I'll thank you very much and share the technical details with you while I'm at it.
</p>

<h2>
    Contact style 📧
</h2>

<p>
gmail mailbox： niwik.dev@gmail.com
</p>
