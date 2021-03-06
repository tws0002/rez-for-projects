name = "pip"
version = "19.0.3"
environ = {
    "PYTHONPATH": [
        "{root}/python",
    ],
}

requires = [
    "python>=2.7,<4",
]

private_build_requires = [
    "rezutils-1",
]

build_command = "python -m rezutils {root}"


def commands():
    global env
    global this
    global system
    global expandvars

    for key, value in this.environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].prepend(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
