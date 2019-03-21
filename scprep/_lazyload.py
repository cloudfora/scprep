import importlib

importspec = {
    'matplotlib': [{'colors': ['is_color_like', 'to_rgba', 'Normalize',
                               'ListedColormap', 'LinearSegmentedColormap',
                               'LogNorm', 'SymLogNorm', 'PowerNorm'],
                    'pyplot': ['scatter', 'rcParams', 'subplots',
                               'hist', 'setp', 'close', 'show'],
                    'animation': ['FuncAnimation'],
                    'cm': ['tab10'],
                    'axes': ['Axes'],
                    'lines': ['Line2D'],
                    'ticker':['MaxNLocator'],
                    'transforms':['ScaledTranslation']},
                   'get_backend', 'rc'],
    'mpl_toolkits': [{'mplot3d': ['Axes3D']}],
    'fcsparser': [{'api': ['ParserFeatureNotImplementedError', 'parse']}],
    'rpy2': [{'robjects': [{'numpy2ri': ['activate', 'ri2py'],
                            'packages':['STAP'],
                            'vectors':['ListVector'],
                            'conversion':['ri2py']}],
              'rinterface':['NULL', 'RRuntimeWarning']}],
    'h5py': ['File', 'Group', 'Dataset'],
    'tables': ['open_file', 'File', 'Group', 'CArray']
}


class AliasModule(object):

    def __init__(self, name, members):
        self.__module_name__ = name
        self.__module_members__ = members
        self.__implicit_members__ = [
            '__version__', '__warning_registry__', '__file__',
            '__loader__', '__path__', '__doc__', '__package__']
        self.__loaded__ = False
        for member in members:
            if isinstance(member, dict):
                # submodules
                for submodule, submembers in member.items():
                    setattr(self, submodule, AliasModule(
                        "{}.{}".format(name, submodule), submembers))

    def __getattribute__(self, attr):
        super_getattr = super().__getattribute__
        if attr in (super_getattr("__module_members__") +
                    super_getattr("__implicit_members__")):
            if not super_getattr("__loaded__"):
                setattr(
                    self, "__module__",
                    importlib.import_module(super_getattr("__module_name__")))
            return getattr(super_getattr("__module__"), attr)
        else:
            return super_getattr(attr)

    def __str__(self):
        super_getattr = super().__getattribute__
        return 'AliasModule {}'.format(super_getattr("__module_name__"))


for module, members in importspec.items():
    globals()[module] = AliasModule(module, members)
