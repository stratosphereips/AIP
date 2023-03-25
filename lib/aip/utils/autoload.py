
models = []

def register(cls):
    models.append(cls)
    return cls
