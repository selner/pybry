import inspect
import os
import pkgutil
from abc import ABC
from loguru import logger

class AbstractPlugin(ABC):
	#     """Base class that each plugin must inherit from. within this class
	#     you must define the methods that all of your plugins must implement
	#     """
	
	def __init__(self, *args, **kwargs):
		super().__init__()
	
	@property
	def pluginclass(self):
		module = self.__class__.__module__
		if module is None or module == str.__class__.__module__:
			return self.__class__.__qualname__
		return module + '.' + self.__class__.__qualname__

		# clsmembers = inspect.getmembers(self.__module__, self.__class__)
		#
		# return f'{clsmembers.__module__}.{clsmembers.__name__}'

class PluginManager(object):
	"""Upon creation, this class will read the plugins package for modules
	that contain a class definition that is inheriting from the Plugin class
	"""
	_plugins = {}
	_baseclass = "AbstractPlugin"
	
	def __init__(self, plugin_package, baseclass=None):
		"""Constructor that initiates the reading of all available plugins
		when an instance of the PluginManager object is created
		"""
		super().__init__()
		self.plugin_package = plugin_package
		if baseclass:
			self._baseclass = baseclass
		self.reload_plugins()

	@property
	def all(self):
		return self._plugins

	def get_plugin(self, name):
		if name not in self._plugins.keys():
			raise AttributeError(f'{self._baseclass.__name__} plugin "{name}" not found.')
		
		return self._plugins[name]

	def apply_all_plugins_on_value(self, argument):
		"""Apply all of the plugins on the argument supplied to this function
		"""
		logger.debug(f'Applying all plugins on value {argument}:')
		for plugin in self._plugins.values():
			logger.debug(
				f'    Applying {plugin.pluginclass} on value {argument} yields value {plugin.do_thing()}')
	
	def do_callback_all_plugins_on_value(self, func, argument):
		"""Apply all of the plugins on the argument supplied to this function
		"""
		logger.debug(f'Calling {func} on all plugins with value {argument}:')
		for plugin in self._plugins:
			print(
				f'    Applying {plugin.description} on value {argument} yields value {plugin.func(argument)}')
	
	def reload_plugins(self):
		"""Reset the list of all plugins and initiate the walk over the main
		provided plugin package to load all available plugins
		"""
		self.seen_paths = []
		logger.debug(f'Looking for plugins under package {self.plugin_package}')
		self._walk_package(self.plugin_package)
		
		if len(self._plugins) < 1:
			logger.warning(f'    No {self._baseclass.__name__} plugins found in {self.plugin_package}')
			
	def _walk_package(self, package):
		"""Recursively walk the supplied package to retrieve all plugins
		"""
		imported_package = __import__(package, fromlist=['blah'])
		
		for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
			if not ispkg:
				plugin_module = __import__(pluginname, fromlist=['blah'])
				clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
				for (_, c) in clsmembers:
					# Only add classes that are a sub class of Plugin, but NOT Plugin itself
					if issubclass(c, self._baseclass) & (c is not self._baseclass):
						logger.debug(f'    Found plugin class: {c.__module__}.{c.__name__}')
						#self._plugins.append(c())
						self._plugins[c.__name__] = c()
		
		# Now that we have looked at all the modules in the current package, start looking
		# recursively for additional modules in sub packages
		all_current_paths = []
		if isinstance(imported_package.__path__, str):
			all_current_paths.append(imported_package.__path__)
		else:
			all_current_paths.extend([x for x in imported_package.__path__])
		
		for pkg_path in all_current_paths:
			if pkg_path not in self.seen_paths:
				self.seen_paths.append(pkg_path)
				
				# Get all sub directory of the current package path directory
				child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]
				
				# For each sub directory, apply the _walk_package method recursively
				for child_pkg in child_pkgs:
					self._walk_package(package + '.' + child_pkg)

