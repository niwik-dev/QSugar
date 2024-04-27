"""
I'm thinking about migrating the `Provider` and `Context` features into the framework,
which is helpful for large project maintenance,
and the concepts are written as follows.

This is the concept stage, if you have any ideas, please contact me.

def ThemeCard(child:QWidget):
    return Provider(
       value=Ref({"dark":True}),
       child=QWidget(
            child=child
       )
    )

value = Ref({})

card = Context(
    value=value,
    child=QWidget(
        style= \
        '''
            background:black;
            color:white;
        ''' if context["dark"] else '''
            background:white;
            color:black;
        '''
    )
)
"""