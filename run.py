import debugpy
import bakachon as baka
import gc
import os
import threading

from typing import Optional
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PCI = os.environ.get("picture_images")
BCF = os.environ.get("bakachon_folder")


# Use SublimeDebugger, debugpy lib.
def debug_wait_for_attach(listen_to):
    scoop: Optional[str] = os.path.expanduser(
        '~/scoop/apps/python/current/python.exe')
    pyenv: Optional[str] = os.path.expanduser('~/.pyenv/shims/python')
    anyenv: Optional[str] = os.path.expanduser(
        '~/.anyenv/envs/pyenv/shims/python')

    # Use Scoop.
    if os.path.exists(os.path.expanduser(scoop)):
        debugpy.configure(python=str(scoop))
        debugpy.listen(listen_to)
        debugpy.wait_for_client()
    # Use Pyenv.
    elif os.path.exists(pyenv):
        debugpy.configure(python=str(pyenv))
        debugpy.listen(listen_to)
        debugpy.wait_for_client()
    # Use Anyenv.
    elif os.path.exists(anyenv):
        debugpy.configure(python=str(anyenv))
        debugpy.listen(listen_to)
        debugpy.wait_for_client()


# face class
class Face(threading.Thread):

    # use thread
    def __init__(self):
        threading.Thread.__init__(self)

    # run method
    def run(self):
        baka.pull_down_a_shutter(str(PCI), str(BCF))


# try ~ except ~ finally.
try:
    thread = Face()
    thread.run()
# Custom Exception, raise throw.
except ValueError as ext:
    print(ext)
    raise RuntimeError from None

# Once Exec.
finally:
    # GC collection.
    gc.collect()
