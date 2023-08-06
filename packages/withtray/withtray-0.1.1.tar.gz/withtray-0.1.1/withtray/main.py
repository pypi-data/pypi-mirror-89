import click
import shlex
import signal
import threading
import subprocess
from PIL import Image, ImageDraw
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pystray import Icon, Menu, MenuItem


def popen_and_call(on_exit, *popen_args, **popen_kwargs):
    proc = subprocess.Popen(*popen_args, **popen_kwargs)
    def run_in_thread(on_exit, popen_args, popen_kwargs):
        proc.wait()
        on_exit()
    thread = threading.Thread(target=run_in_thread,
                              args=(on_exit, popen_args, popen_kwargs))
    thread.daemon = True
    thread.start()
    return proc


def find_icon(icon_name):
    theme = Gtk.IconTheme.get_default()
    found_icons = set()
    for res in range(0, 512, 2):
        icon = theme.lookup_icon(icon_name, res, 0)
        if icon:
            found_icons.add(icon.get_filename())
    return list(found_icons)


def create_image(width=16, height=16, color1='red', color2='blue'):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image


class Tray:
    def __init__(self, image, name, cmd):
        self.cmd = cmd
        self.icon = Icon(name, image, menu=Menu(MenuItem('Quit', self.quit)))

    def run(self):
        self.process = popen_and_call(self.on_quit, shlex.split(self.cmd))
        self.icon.run()

    def on_quit(self):
        self.icon.stop()

    def quit(self):
        self.process.send_signal(signal.SIGINT)


def run_tray(image):
    menu = Menu(MenuItem('Quit', quit),)
    icon = Icon('withtray', image, menu=menu)
    icon.run()


@click.command()
@click.argument('cmd')
@click.option('--name', default='withtray')
@click.option('--icon', default=None)
def main(cmd, name, icon):
    if icon is not None and (files := find_icon(icon)):
        icon = Image.open(files[0])
    else:
        icon = create_image()

    Tray(icon, name, cmd).run()


if __name__ == '__main__':
    main()
