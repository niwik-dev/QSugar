class StyleSheet(dict):
    def __init__(self, *args, **kwargs):
        self.stylesheet = dict()
        for arg in args:
            if isinstance(arg, dict):
                self.stylesheet.update(arg)
        if kwargs:
            self.stylesheet.update(kwargs)
        super().__init__(self.stylesheet)

    def toString(self):
        props = []
        for key, value in self.stylesheet.items():
            key = key.replace('_', '-')
            if isinstance(value, tuple):
                value = ' '.join(value)
            props.append(':'.join((key, value))+';')
        res = '\n'.join(props)
        return res
