from rich.console import Console


class CustomConsole(Console):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def print_lvl1(self, text: str):
        self.print(f'[bold blue]=> {text}[/bold blue]')

    def print_lvl2(self, text: str):
        self.print(f'[bold green]==> {text}[/bold green]')

    def print_lvl3(self, text: str):
        self.print(f'[bold yellow]===> {text}[/bold yellow]')


console = CustomConsole()
