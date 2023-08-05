try:
    from dune.packagemetadata import metaData
except ImportError:
    from packagemetadata import metaData
from skbuild import setup
setup(**metaData('0.2.0.dev20201218')[1])
