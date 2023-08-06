import os
from pathlib import Path
import subprocess as subp
from hashlib import sha224

def exprog(args, cwd=None, env=None):
    env = env if env else os.environ
    cwd = cwd if cwd else os.getcwd()
    return subp.Popen(
        args,
        cwd=cwd,
        env=env,
        stdout=subp.PIPE,
        stderr=subp.PIPE,
        encoding="utf-8",
        universal_newlines=True
    )

def shell(args, cwd=None, env=None, printf=lambda x: print(x, end='')):
    printf(
        "$ {}\n".format(
            ' '.join(args) if not isinstance(args, str) else args
        )
    )
    with exprog(args, cwd=cwd, env=env) as p:
        while p.poll() == None:
            printf(p.stdout.read(1))
        if p.stdout.readable():
            printf(p.stdout.read())
        if p.returncode != 0:
            printf(p.stderr.read())
        return p.returncode


def choose_file(path_templates, name):
    """
    return the first exists path, if not one exists, return None
    ````
    choose_file(["/bin/?", "/usr/local/?"], "sh")
    ````
    """
    for p in map(lambda pt: pt.replace("?", name), path_templates):
        path = Path(p)
        if path.exists():
            return str(path)
    return None

def get_file_hash(path, update, block_size=65536):
    with open(path, 'rb') as f:
        fblk = f.read(block_size)
        while len(fblk) > 0:
            update(fblk)
            fblk = f.read(block_size)

def get_file_hash_sha224(path, block_size=65536):
    obj = sha224()
    get_file_hash(path, obj.update, block_size)
    return obj.hexdigest()

def check_binary(name, PATH=None):
    """
    check if the given name exists in PATHs, if exists, return the first path found, else return None.
    ````
    if check_binary("clang"):
        print("Clang mounted!")

    if not check_binary("some-tool", PATH=".:./tools/"):
        print("Could not found the tool needed for compiling")
    ````
    """
    PATH = PATH if PATH else os.environ.get("PATH", "")
    pathes = map(lambda x: os.path.join(x, "?"), PATH.split(":"))
    return choose_file(pathes, name)

def create_makru(*args):
    """
    create a makru instance to deal with another makru project. this function doesn't have path expanding, so the '.' means CWD, not the folder contains makru config file.
    ````
    projectb = create_makru("-F","./projectb")
    projectb.action("test")
    ````
    """
    from .makru import Makru
    return Makru(args)

def run_makru(*args):
    """
    it looks like run the makru CLI directly.
    """
    makru_instance = create_makru(**args)
    makru_instance.main()
