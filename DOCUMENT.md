<link href='https://fonts.googleapis.com/css?family=Noto Sans' rel='stylesheet'>
<link href="
https://cdn.jsdelivr.net/npm/jetbrains-mono@1.0.6/css/jetbrains-mono.min.css
" rel="stylesheet">

<h1>QSugar Help Document</h1>
<hr/>
<h2>Module Enhance</h2>
<p>

QSugar implements modules for enhancing the `PySide` framework, which can expand original functions without affecting existing functions. There are currently 3 enhancement modes：`Def`、`Bind` and `DSL`。

</p>

<h3>Def Enhance</h3>
<p>

`Def`,the abbreviation of Define, is the most basic enhancement mode.

Using `Def()` to enhance single widget class will return the enhanced proxy class object. To enhance multiple widget classes, please use `Batch(Def)(...)`

```python
from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from QSugar.proxy import Def, Batch

ProxyWidget = Def(QWidget)

Batch(Def)(
    QWidget, QLabel, QPushButton
)
```

Enhanced classes can simplify the setting of properties, and properties with longer names in Qt are replaced by abbreviated names.

For example：`contentsMargins` correspond to `margins`，`maximumWidth` correspond to `max_width` etc.

```python
from PySide6.QtWidgets import QWidget
from QSugar.proxy import Def

Def(QWidget)

widget = QWidget(
    title='windowTitle',
    size=(100, 200),
    margins=(8, 16, 16, 8)
)

```
The setter method of the enhanced class can be called in a streaming manner, and DSL layout can be implemented based on this feature. For developers, you can use the assignment expression `:=` to obtain the handle of each widget to achieve more granular control.

```python
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from QSugar.proxy import Def, Batch

Batch(Def)(
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout
)

widget = (
    QWidget().setLayout(
        QHBoxLayout()
        .addWidget(
            label := QLabel()
            .setText('Fluent API Demo')
        ).addWidget(
            btn := QPushButton()
            .setText('Click Me to Modify Label')
        )
    )
)

btn.clicked.connect(label.setText('Okay!'))
```
The framework also provides the self field to get a handle proxy for widget, which can control the widget in exactly the same way.

```python
from PySide6.QtWidgets import QWidget
from QSugar.proxy import Def
from QSugar.type import Ref

Def(QWidget)

handler = Ref(None)

widget = QWidget(
    self=handler,
)

handler.setWindowTitle('window Title')
```
</p>
<h3>DSL enhance</h3>
<p>

DSL enhancements mainly deal with the nested relationship between `QLayout` and `QWidget`. It fully inherits all the features enhanced by `Def`.

```python
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from QSugar.proxy import DSL, Batch

Batch(DSL)(
    QWidget,
    QLabel,
    QHBoxLayout
)

widget = QWidget(
    child=QHBoxLayout(
        children=[
            QLabel(text='Row1'),
            QLabel(text='Row2'),
            QLabel(text='Row3'),
        ]
    )
)
```
Enhanced classes can use the properties of `child` and `children`  to implement flexible layout DSL and quickly build interface UI from code. The nesting of `QWidget` and `QBoxLayout` is very unintuitive, so the framework encapsulates `Row`, `Column`, `RowCol`, and `ColRow` to assist the layout.

```python
from PySide6.QtWidgets import QWidget, QLabel
from QSugar.proxy import DSL, Batch
from QSugar.component import Row

Batch(DSL)(
    QWidget,
)

widget = QWidget(
    child=Row(
        children=[
            QLabel(text='Row1'),
            QLabel(text='Row2'),
            QLabel(text='Row3')
        ]
    )
)
```
What comes to mind? Paired with the `generator`, you can achieve flexible layout and easily implement list rendering.

```python
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel
from QSugar.proxy import DSL, Batch
from QSugar.component import RowCol

Batch(DSL)(
    QWidget,
    QLabel,
)

widget = QWidget(
    child=RowCol(
        alignment=Qt.AlignmentFlag.AlignCenter,
        children=[
            QLabel(
                text=f'<{tag}>{index + 1}. {name}</{tag}>'
            )
            for index, (name, tag) in enumerate(
                [
                    ('John', 'h1'), ('Tom', 'h2'), ('Alice', 'h3')
                ]
            )
        ]
    )
)
```
You can refer to the example `test_render.py` to try more flexible DSL usage.
</p>

<h3> Bind Enhance</h3>
<p>

`Bind` enhancement is the prerequisite for using reactive programming and is a very critical step. It also has all the features enhanced by `Def`.

```python
from PySide6.QtWidgets import QPushButton, QLabel
from QSugar.proxy import Bind, Batch
from QSugar.type import Ref, Computed

Batch(Bind)(
    QPushButton,
    QLabel
)

labelText = Ref('0')
label = QLabel(text=labelText)

btnValue = Ref(0)
btnText = Computed(globals())


@btnText.get
def getBtnText():
    return str(btnText.value)


btn = QPushButton()
btn.setText(btnText)
```
If enhancement is not performed, the setter method of the widget can only take effect on the initial usage, and cannot take effect on reference types such as Ref and Computed. For specific details, see <a href="">Reactive Programming</a>.
</p>

<h2>Reactive Programming</h2>

> If you have studied the Vue framework, you can refer to this [document](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)

<p>

The `Ref` type is used to wrap properties so that widgets can identify and handle them reactively.

The `DeepRef` type can wrap complex type properties so that all its sub-properties are proxied.

```python
from QSugar.type import Ref, DeepRef
from PySide6.QtGui import QColor

text = Ref('a')


class Model:
    def __init__(self):
        self.color = QColor(255, 100, 100)
        self.text = 'Something'


model = DeepRef(Model())
```

To obtain a reference to a `Ref`/`DeepRef` object, you can call the `getValue` method or directly access the value property，
when calling the `setValue` method and setting the value property to change its reference, the `valueChanged` signal will be triggered.

```python
from QSugar.type import Ref

text = Ref('a')
print(text.value)  # 'a'
print(text.getValue())  # 'a'

text.valueChanged.connect(lambda value: print(value))

text.value = 'b'  # trigger signal
text.setValue('c')  #trigger signal

```
The `Ref`/`DeepRef` type implements syntactic sugar for assigning and obtaining references, and can also obtain methods and properties of proxy objects.

```python
from QSugar.type import Ref

text = Ref('a')
text << 'b'  # equivalent to text.setValue('b')

print(*text)  # equivalent to print(text.getValue())

from PySide6.QtWidgets import QWidget

widget = Ref(QWidget())
widget.setWindowTitle('title')  # Methods of proxy objects to be called directly

```
Combined with `Bind` enhancement, the binding of data and widgets can be realized, and the logic and interface can be bridged through data.

```python
from QSugar.type import Ref
from QSugar.proxy import Batch,Bind
from PySide6.QtWidgets import QLabel

Batch(Bind)(
    QLabel
)

text = Ref('Old Text')

QLabel(
    text=text,
)

text << 'New Text'
```

In many cases, there are differences between the data required by  the widget and defined property objects.

For example, in a counter, the property that needs to be changed in the logic is number, but `QLabel` needs to render a string. In this case, computed properties can be used to solve the problem.

Because reflection is needed to obtain global variables, `globals()` is required to obtain the global context when constructing calculated properties. And use the get decorator to define the getter method.

```python
from QSugar.type import Ref,Computed

count = Ref(0)
text = Computed(globals())

@text.get
def getText():
    return str(count.value)
```
It will automatically collect all dependencies of the `Ref`/`DeepRef` type in the getter method,
once the dependency changes, its `valueChanged` signal is automatically triggered.

```python
from QSugar.type import Ref,Computed

valueA = Ref(0)
valueB = Ref(1)
sum = Computed(globals())

@sum.get
def getText():
    return valueA.value+valueB.value

sum.valueChanged.connect(lambda value:print(value))

valueA << 2 # trigger signal
valueB << 3 # trigger signal
```

Combined with Bind enhancement, it can meet more data binding situations. For details, see `test_computed.py`.
</p>

<h2>
    DSL Syntax
</h2>

<p>
    QSugar supports multiple DSL syntaxes for layout, which are independent of data binding. Developers can choose one of the DSL syntaxes to quickly layout.
</p>

<h3>
    __init__ Method Property
</h3>

<p>

This is native support for `PySide`, based on the property setting/slot function binding method derived from the Qt metatype system.

And after DSL enhancement, layout can be carried out flexibly and quickly.

```python
import sys

from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QVBoxLayout

from QSugar.proxy import Batch, DSL, Bind
from QSugar.type import Ref, DeepRef

Batch(Bind)(
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)

Batch(DSL)(
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

app = QApplication(sys.argv)

textProp = Ref('Text')

btn = DeepRef(None)

widget = QWidget(
    title='Prop DSL Test',
    size=(300, 300),
    child=QHBoxLayout(
        children=[
            QPushButton(
                text=textProp
            ),
            QVBoxLayout(
                children=[
                    QPushButton(
                        text=textProp
                    ),
                    QPushButton(
                        text=textProp
                    )
                ]
            ),
            QPushButton(
                text='Button A',
                clicked=lambda : textProp << ''
            ),
            QPushButton(
                text='Button B',
                clicked=lambda: textProp << 'Text'
            )
        ]
    )
)

widget.show()
app.exec()


```
You can obtain the handle of each widget through `self` or assignment expression `:=`
</p>

<h3>
    Fluent API
</h3>

<p>
The fluent API is a classic DSL design, but its disadvantage is that it is not intuitive.

```python
import sys

from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QVBoxLayout

from QSugar.proxy import Batch, Bind
from QSugar.type import Ref

Batch(Bind)(
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
)

textProp = Ref('Text')

app = QApplication(sys.argv)

widget = \
    (
        QWidget()
        .setWindowTitle('Fluent DSL Test')
        .setFixedSize(300, 300)
        .setLayout(
            QHBoxLayout()
            .addWidget(
                btn := QPushButton()
                .setText(textProp)
            )
            .addLayout(
                QVBoxLayout()
                .addWidget(
                    QPushButton()
                    .setText(textProp)
                )
                .addWidget(
                    QPushButton()
                    .setText(textProp)
                )
            )
            .addWidget(
                btnA := QPushButton()
                .setText('Button A')
            )
            .addWidget(
                btnB := QPushButton()
                .setText('Button B')
            )
        )
    )

btnA.clicked.connect(
    lambda: textProp << ''
)

btnB.clicked.connect(
    lambda: textProp << 'Text'
)

widget.show()
app.exec()
```
You can obtain the handle of each widget through `self` or walrus expression `:=`.
</p>

<h3>
    qtml Parse
</h3>

<p>
    xml is used as the carrier for layout, and embedded in scripts  for flexible control.

</p>

> It is still in the experimental stage, and this feature should be used with caution.
