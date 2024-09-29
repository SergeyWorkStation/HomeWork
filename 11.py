class Command:
    def execute(self):
        pass

    def undo(self):
        pass


class LightOnCommand(Command):
    def __init__(self, control):
        self.control = control

    def execute(self):
        self.control.light_on()

    def undo(self):
        self.control.undo()


class LightOffCommand(Command):
    def __init__(self, control):
        self.control = control

    def execute(self):
        self.control.light_off()

    def undo(self):
        self.control.undo()


class RemoteControl:
    def __init__(self):
        self._history_control = []

    def light_on(self):
        self._history_control.append("on")
        print(f"Light is: {self._history_control[-1]}")

    def light_off(self):
        self._history_control.append("off")
        print(f"Light is: {self._history_control[-1]}")

    def undo(self):
        self._history_control.pop()
        print(f"Light is: {self._history_control[-1] if self._history_control else "___"}")

class CommandInvoker:
    def __init__(self):
        self.history = []

    def execute_command(self, command):
        command.execute()
        self.history.append(command)

    def undo_command(self):
        if self.history:
            command = self.history.pop()
            command.undo()


control = RemoteControl()
invoker = CommandInvoker()

light_on = LightOnCommand(control)
light_off = LightOffCommand(control)

invoker.execute_command(light_on)
invoker.execute_command(light_off)
invoker.undo_command()
invoker.execute_command(light_off)
invoker.execute_command(light_on)

print()
invoker.undo_command()
invoker.undo_command()
invoker.undo_command()
invoker.undo_command()