'''
Copyright 2020 Tabacaru Eric

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

import subprocess
from typing import List
import click
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import subprocess
import os

class Server:
    def __init__(self, main_file: str, extra_args: List[str] = []) -> None:
        self.main_file = main_file

        self.args = ["python", self.main_file]

        for a in extra_args:
            self.args.append(a)

        self.process = subprocess.Popen(
            self.args
        )

    def restart(self):
        self.process.terminate()

        self.process = subprocess.Popen(
            self.args
        )


class Handler(PatternMatchingEventHandler):
    def __init__(
        self,
        main_file: str,
        extra_args: List[str],
        patterns=None,
        ignore_patterns=None,
        ignore_directories=False,
        case_sensitive=False
    ):
        self.sv = Server(main_file=main_file, extra_args=extra_args)
        
        super().__init__(
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=ignore_directories,
            case_sensitive=case_sensitive
        )
    
    def on_modified(self, event):
        click.echo(click.style(f"[*] Detected file modified at {event.src_path} - Restarting...", fg="blue"))

        self.sv.restart()
    
    def on_created(self, event):
        click.echo(click.style(f"[*] Detected file created at {event.src_path} - Restarting...", fg="blue"))
    
        self.sv.restart()

    def on_deleted(self, event):
        click.echo(click.style(f"[*] Detected file deleted at {event.src_path} - Restarting...", fg="blue"))

        self.sv.restart()

    def on_moved(self, event):
        click.echo(click.style(f"[*] Detected file moved at {event.src_path} - Restarting...", fg="blue"))

        self.sv.restart()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('main_file', required=False, default="./bot.py")
@click.option('--extra-args', required=False, default="")
def start(main_file, extra_args):
    if os.path.exists(os.path.abspath(main_file)):
        observer = Observer()

        if extra_args != "":
            extra_args = extra_args.split(',')

        observer.schedule(
            Handler(main_file=main_file, extra_args=extra_args),
            path=".",
            recursive=True
        )

        click.echo(click.style("[!] Starting server...", fg="green"))
        
        observer.start()

        click.echo(click.style("[!] Started server. Listening for file changes...\n", fg="green"))

        try:
            while True:
                time.sleep(1)
            
        except KeyboardInterrupt:
            click.echo("[stop] Keyboard Interrupt - stopping server...")
            observer.stop()

        observer.join()
    
    else:
        click.echo(click.style(f"[x] No file at {main_file}", fg="red"))