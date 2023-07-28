import threading

from discord.ext.commands import Bot


class Command_Class:
    """SC Command Class
    
    Base class for a discord bot command class.

    Call `super().__init__(client)` in
    the child constructor if you're using it.

    Properties:
    ----------
    bot_client: :class: `discord.ext.commands.Bot`
        Discord bot client.

    Arguments
    ----------
    client: :class: `discord.ext.commands.Bot`
        Discord bot client.
    """

    @property
    def bot_client(self) -> Bot:
        return self._client
    
    # Constructor method
    def __init__(self, client: Bot):
        self._client = client # Sets the client.

        # Creates a new thread.
        load_thread = threading.Thread(target=self.load_commands) 
        load_thread.run() # Loads the commands using the created thread.
    
    
    # Method that loads bot commands from the class.
    def load_commands(self):
        """Override this method in child class.

        Put command methods in here like you would normally but with `@self.client.command()` instead of `@client.command()`.
        """
        pass