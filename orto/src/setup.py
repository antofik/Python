from distutils.core import setup
from glob import glob
import py2exe


class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.version = "1.0.0.0"
        self.company_name = "As Program"
        self.copyright = "As Program"
        self.name = "Export"

win = Target(
    icon_resources=[(1, r"favicon.ico",), ],
    description="ORTO",
    script="main.py",
)
data_files = [
    ("dancecompetition", glob(r'dancecompetition\*.*')),
]
setup(
    options={"py2exe": {"compressed": 1,
                        "optimize": 2,
                        #"ascii": 1,
                        "bundle_files": 1,
                        "includes": ["sqlalchemy.dialects.mysql","sqlalchemy.connectors",
                                     "MySQLdb", #"distutils", "distutils.command",
                                     ],
                        #"packages":['distutils', 'distutils.command'],
    },
    },
    data_files=data_files,
    zipfile=None,
    windows=[win],
)