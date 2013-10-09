#setup.py
from distutils.core import setup
import py2exe
setup(console=["gao.py"],
        options = { "py2exe":
            {"dll_excludes":["MSVCP90.dll"], 
            "includes":["sip",],
            "optimize":2,
            "bundle_files":1,
            }},
        zipfile = None
        )


