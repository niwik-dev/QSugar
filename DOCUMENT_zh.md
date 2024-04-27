<link href='https://fonts.googleapis.com/css?family=Noto Sans' rel='stylesheet'>
<link href="
https://cdn.jsdelivr.net/npm/jetbrains-mono@1.0.6/css/jetbrains-mono.min.css
" rel="stylesheet">

<h1>QSugar 帮助文档</h1>

<h2>组件增强</h2>
<p>

QSugar实现了用于增强PySide框架的组件，可以在<strong>不影响现有功能</strong>的情况下拓展原有功能。目前存在3种增强模式：`Def`、`Bind`和`DSL`。

</p>

<h3>Def增强</h3>
<p>

`Def`，即Define的缩写，是最基础的增强模式。

使用`Def()`对单个控件类进行增强，会返回被增强的代理类对象。而对多个控件类进行增强请使用`Batch(Def)(...)`

```python
from PySide6.QtWidgets import QWidget, QLabel, QPushButton
from QSugar.proxy import Def, Batch

ProxyWidget = Def(QWidget)

Batch(Def)(
    QWidget, QLabel, QPushButton
)
```

增强类可以简化属性的设置，对Qt中名称较长的属性由简略名称代替。

例如：`contentsMargins`对应`margins`，`maximumWidth`对应`max_width`等等。

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
增强类的setter方法可以流式调用，可以依据这个特性实现DSL布局。对开发者来说，可以使用海象表达式`:=`来获取各个控件的句柄，实现粒度更精细的控制。

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
框架也提供了`self`字段来获取控件的句柄代理，可以以完全相同的方式控制控件。

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
<h3>DSL增强</h3>
<p>

DSL增强主要应对于`QLayout`和`QWidget`之间的嵌套关系。它完全继承`Def`增强的所有特性。

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

增强类可以使用`child`和`children`属性实现灵活的布局DSL，快速地从代码构建界面UI。`QWidget`和`QBoxLayout`的嵌套是很不直观的，因此框架封装了`Row`,`Column`以及`RowCol`,`ColRow`来辅助布局。

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
想到什么？和生成器搭配可以实现灵活布局，轻松实现列表渲染。

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
可以参考例子`test_render.py`，尝试更多灵活的DSL用法。
</p>

<h3> Bind增强</h3>
<p>

`Bind`增强是使用响应式编程的前提，是非常关键的步骤。同样具备`Def`增强的所有特性。

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

如果不进行增强，那么控件的setter方法仅能对初始用法生效，无法对`Ref`,`Computed`等引用类型生效，具体的细节见<a href="">响应式编程</a>。
</p>

<h2>响应式编程</h2>

> 如果你学习过Vue框架，可以参考这篇[文档](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)

<p>

`Ref`类型用来包装属性，使得控件可以识别并且响应式处理。

`DeepRef`类型可以包装复杂类型的属性，使得其子属性均被代理。

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

获取`Ref`/`DeepRef`对象的引用可以调用`getValue`方法或者直接访问`value`属性，
调用`setValue`方法和设置`value`属性改变其引用时，会触发`valueChanged`信号

```python
from QSugar.type import Ref

text = Ref('a')
print(text.value)  # 'a'
print(text.getValue())  # 'a'

text.valueChanged.connect(lambda value: print(value))

text.value = 'b'  # 触发信号
text.setValue('c')  # 触发信号
```
`Ref`/`DeepRef`类型实现了赋值和获取引用的语法糖，同时可以获取代理对象的方法和属性。

```python
from QSugar.type import Ref

text = Ref('a')
text << 'b'  # 相当于text.setValue('b')

print(*text)  # 相当于print(text.getValue())

from PySide6.QtWidgets import QWidget

widget = Ref(QWidget())
widget.setWindowTitle('title')  # 可以直接调用代理对象的方法
```
结合`Bind`增强，可以实现数据与控件的绑定，通过数据桥接逻辑和界面。

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

很多时候，控件需要的数据与定义的属性对象存在着差异。

比如，在计数器中，逻辑中需要变化的属性是数字，但是`QLabel`需要呈现的是字符串，这种情形下可以使用计算属性来解决问题。

因为需要反射获取全局变量，构造计算属性时需要`globals()`获取全局上下文。并且使用get装饰器来定义getter方法。

```python
from QSugar.type import Ref,Computed

count = Ref(0)
text = Computed(globals())

@text.get
def getText():
    return str(count.value)
```
它会自动收集getter方法中的`Ref`/`DeepRef`类型的所有依赖，
一旦依赖发生变化就会自动触发其`valueChanged`信号。

```python
from QSugar.type import Ref,Computed

valueA = Ref(0)
valueB = Ref(1)
sum = Computed(globals())

@sum.get
def getText():
    return valueA.value+valueB.value

sum.valueChanged.connect(lambda value:print(value))

valueA << 2 # 触发信号
valueB << 3 # 触发信号
```

结合`Bind`增强可以满足更多数据绑定的情形，详情见 `test_computed.py`。
</p>

<h2>
    DSL语法
</h2>

<p>
    QSugar支持多种DSL语法进行布局，它们与数据绑定是独立的。开发者可以自行选择其中一种DSL语法，快速进行布局。
</p>

<h3>
    __init__方法属性
</h3>

<p>
这是PySide原生支持，基于Qt元类型系统衍生的属性设置/槽函数绑定方式。

并且进行DSL增强以后，可以灵活且快速地进行布局。

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
可以通过`self`或者海象表达式`:=`获取各控件的句柄。
</p>

<h3>
    Fluent API
</h3>

<p>
流式API是经典的DSL设计，缺点就是直观性不强。

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
可以通过`self`或者海象表达式`:=`获取各控件的句柄。
</p>

<h3>
    qtml解析
</h3>

<p>
    xml为载体进行布局，并且嵌入脚本进行灵活控制。
</p>

> 暂时不提供文档，目前还在实验期
