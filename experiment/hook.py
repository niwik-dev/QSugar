"""
I'm thinking about migrating `React Hooks` into the framework, and the concepts are written as follows.
This is the concept stage, if you have any ideas, please contact me.

def Counter():
    setCount,count = useState(0)
    return QWidget(
        child:Row(
            children=[
                QLabel(
                    text=f"You have clicked {count} Times"
                ),
                QPushButton(
                    text="Plus One",
                    clicked=lambda: setCount(count+1)
                ),
                QPushButton(
                    text="Clear",
                    clicked=lambda: setCount(0)
                )
            ]
        )
    )
"""