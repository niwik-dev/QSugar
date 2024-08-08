<link href='https://fonts.googleapis.com/css?family=Noto Sans' rel='stylesheet'>
<link href="
https://cdn.jsdelivr.net/npm/jetbrains-mono@1.0.6/css/jetbrains-mono.min.css
" rel="stylesheet">

<h1 style="text-align: center;">QSugar🌱</h1>

<div style="text-align:center; letter-spacing: 0.05em;">
    响应式 PySide框架，简单且友好
</div>

<h2>
    语言🌐
</h2>

[简体中文](README_zh.md) &nbsp;[English](README.md)

<h2>
    安装🛠️
</h2>

```bash
   pip install QSugar
```

<h2>
    说明🗂️
</h2>

<h3> 介绍 </h3>

<p>
    QSugar是一个用于高效构建和响应界面的PySide框架，本身借鉴学习了Vue等优秀框架的理念。QtQuick技术的发展，证实Qt元类型系统赋予了Qt在声明式UI上的无限潜力。QSugar在此基础上而构思和大胆尝试。
</p>

<p>
    如果你不了解Vue框架的理念，可以阅读下述文档。
</p>

> [Vue框架](https://vuejs.org/guide)

<h2>
    快速上手🖐️
</h2>

<span>这是一个计数器的例子，你可以从中了解，它与传统开发模式的区别。<span>

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
QSugar使用装饰器增强QtWidgets的现有类，使用 Batch(DSL)(...) 进行注册。与此同时，借助于Ref和Computed类来包装属性和计算属性，详情见<a>响应式编程</a>。

QSugar使用DSL语法和响应式对象，来迅速构建UI界面。请注意！QSugar支持<strong>不止一种</strong>DSL语法，它与响应式编程是独立设计的。<br/>

如果你不打算DSL语法，响应式编程是可以适用的。例如：
</p>

```python
import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from QSugar.type import Ref

btnText = Ref('Click Me!')

app = QApplication(sys.argv)
widget = QPushButton()
widget.setText(btnText)
widget.show()

# 修改按钮的文本内容
btnText << 'Modified'

app.exec()
```
<p>
    尽可能降低对PySide框架的侵入性，是QSugar框架设计的准则之一。正如其名，如果把传统开发模式比作咖啡，QSugar就像方糖一样，需要的功能则加，不需要则搁置。
</p>

<p>
    支持的布局DSL语法包括：
    <ul>
        <li>
            __init__方法属性
        </li>
        <li>Fluent API</li>
    </ul>
</p>

<h2>
    帮助文档📘
</h2>

<p>

目前只有md文档，见[Github文档](DOCUMENT_zh.md)

</p>

<h2>
    问题解答❓
</h2>

<p>
Q:为什么不兼容PyQt？

A:QSugar目前只支持PySide，由于PyQt的绑定和PySide的差异性很大，存在着这样的问题：

(1) PyQt对象属性虽然可以在__init__方法里设置，但是不会触发相应的setter方法。虽然可以通过反射解决，但是由于设置属性/绑定信号是UI构建的高频操作，频繁反射获取setter方法会导致严重的性能问题。（经测试经常出现页面卡顿）

(2) PyQt使用的sip绑定，缺乏shiboken对于Python中间层支持，导致很多特性无法使用。例如使用装饰器代理方法/类的时候，部分方法会出现莫名的异常（疑似内存释放和函数寻址问题）。
</p>

<h2>
    支持项目👍
</h2>

<p>
如果你觉得项目有价值，请给项目点个Star⭐，谢谢你啦！

如果你给下水道的鼠鼠买一杯热可可，

我会非常感谢你，并且在搬砖之余与你分享技术细节。
</p>

<h2>
    联系方式 📧
</h2>

<p>
gmail邮箱： niwik.dev@gmail.com
</p>
