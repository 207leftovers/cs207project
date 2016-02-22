class LazyOperation:
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return LazyOperation(self.function, *args, **kwargs)

    def eval(self):
        newargs = list()
        for i in self.args:
            if isinstance(i, LazyOperation):
                newargs.append(i.eval())
            else:
                newargs.append(i)
        return self.function(*newargs, **self.kwargs)
