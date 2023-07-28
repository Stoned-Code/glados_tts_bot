from os import name


class Command:
    """SC Command
    
    An object containg basic information about commands.

    Used for indexing command info.

    Static Variables
    -----------
    prefix: `string`
        Defaulted to "!".

        Change using `set_prefix` method.

    Methods
    -----------
    - set_prefix

    Arguments
    -----------
    name: :class: `string` (Required)
        Discord command name without prefix.

    description: :class: `string`
        The description that gives details about the command.

    example: :class: `string`
        The example command that's shown.
        Input without prefix.

    category: :class: `string`
        The category that the command is in.

    aliases: :class: `list[string]`
        The aliases used for the command.

    argumentDescriptions: :class: `string`
        The descriptions of the command's arguments.

    prefix: :class: `string`
        The prefix used for the commands
    """

    def __init__(self, name, description = 'No description available.', example = None, category = 'Default', aliases = None, argumentDescriptions = None):
        self.name = name
        self.description = description
        self.example = example
        self.category = category
        self.aliases = aliases
        self.argumentDescriptions = argumentDescriptions

    def __call__(self, func):

        def decoration(**kwargs):
            return func

        return decoration


    def __str__(self):
        info = 'Name: {0.name}\nExample: {0.prefix}{0.example}\nCategory: {0.category}\nDescription: {0.description}'.format(self)
        return info
    

class SCCommands:
    def __init__(self, prefix = '!'):
        self.commandList = []
        self.categories = []
        self.prefix = prefix


    def set_prefix(cls, prefix):
        """Sets the prefix of the `SC_Command` class

        Properties
        -----------
        prefix: `string`
            The prefix used for the commands
        """
        cls.prefix = prefix
    
    # def add_command(self, name, description = 'No description available', example = None, category = 'Default', aliases = None, argumentDescriptions = None):


    #     # def wrapper(*args, **kwargs):
    #     #     return func(*args, **kwargs)
        
    #     if example == None:
    #         example = name
            
    #     # description = kwargs.get('description', "No description available.")
    #     # example = kwargs.get('example', name)
    #     # category = kwargs.get('category', "Default")
    #     # aliases = kwargs.get('aliases', None)
    #     # argumentDescriptions = kwargs.get('argumentDescriptions', None)
    #     # name = name if name != None else func.__name__
        
    #     if self.has_command(name):
    #         return

    #     if category != None and category not in self.categories:
    #         self.categories.append(category)

    #     self.commandList.append(Command(name, description=description, example = example, category = category, aliases = aliases, argumentDescriptions=argumentDescriptions))

    #     # return wrapper

    def add_command(self, *args,  **kwargs):
        def decorator(func):

            name = kwargs.get('name', func.name)
            description = kwargs.get('description', "No description available.")
            example = kwargs.get('example', name)
            category = kwargs.get('category', "Default")
            aliases = kwargs.get('aliases', None)
            argumentDescriptions = kwargs.get('argumentDescriptions', None)


            if self.has_command(name):
                return func

            if category is not None and category not in self.categories:
                self.categories.append(category)

            self.commandList.append(Command(name, description=description, example = example, category = category, aliases = aliases, argumentDescriptions=argumentDescriptions))
            return func
        return decorator

    def has_command(self, command_name):
        commands = [command.name for command in self.commandList]
        return command_name in commands
