import os
import re
import shutil
import logging
import subprocess
import contextlib
from datetime import datetime

from dateutil.tz import tzlocal

from .note import Xote


class Completer:
    """readline completion object"""

    def __init__(self, words):
        self.words = words

    def terms(self, prefix, index):
        matching_words = [
            w for w in self.words if w.startswith(prefix)
            ]
        try:
            return matching_words[index]
        except IndexError:
            return None


def view_markdown(path):
    """view file through markdown conversion"""
    cmd = "pandoc {} | lynx -stdin".format(path)
    subprocess.run(cmd, shell=True)


def edit_path(path, offset=None):
    """directly edit message at path

    WARNING: does not updated metadata in header, such as modification
    time.

    """
    if os.getenv('EDITOR'):
        cmd = os.getenv('EDITOR').split()
    else:
        cmd = ['xdg-open']
    if offset and cmd[0] in ['emacs', 'emacsclient']:
        cmd += [offset]
    cmd += [path]
    logging.debug("edit: {}".format(' '.join(cmd)))
    subprocess.run(cmd)


@contextlib.contextmanager
def edit_note(note):
    """edit a note

    This is the preferred way to edit notes.  This makes a temporary
    copy of the note to edit, opens the temp note with the preferred,
    writes the modified text back to the original note while updating
    the 'modified' header with the modification time, then unlinks the
    temp copy.

    """
    base, ext = os.path.splitext(note.path)
    editpath = base + '.edit' + ext
    if os.path.exists(editpath):
        raise IOError("note being edited")
    shutil.copy(note.path, editpath)
    edit_path(editpath, offset='+7')
    enote = Xote(editpath)
    body = enote.body
    title = enote.header.get('title')
    note.write(body=body, title=title)
    os.unlink(editpath)


def xclip(text):
    """copy text into X clipboard.

    Support wayland if the WAYLAND_DISPLAY variable is set.

    """
    if os.getenv('WAYLAND_DISPLAY'):
        cmd = ["wl-copy", "-p"]
    else:
        cmd = ["xclip", "-i"]
    subprocess.run(
        cmd,
        input=text.encode('utf-8'),
        check=True,
    )


URL_RE = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


def extract_urls(text):
    """extract all URLs from text"""
    # FIXME: how to handle URLs broken across lines?
    #text = text.replace('\n', '')
    urls = set()
    for url in URL_RE.finditer(text):
        # FIXME: how to handle URLs enclosed in parens?
        urls.add(url.group().strip(')'))
    return urls


def datetime_age(dt):
    td = datetime.now().astimezone(tzlocal()) - dt.astimezone(tzlocal())
    seconds = int(td.total_seconds())
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365)
    if years > 1:
        s = f'{years} years'
    elif years > 0:
        s = f'{years} year'
    elif days > 1:
        s = f'{days} days'
    elif days > 0:
        s = f'{days} day'
    elif hours > 1:
        s = f'{hours} hours'
    elif hours > 0:
        s = f'{hours} hour'
    elif minutes > 1:
        s = f'{minutes} minutes'
    elif minutes > 0:
        s = f'{minutes} minute'
    else:
        s = 'seconds'
    return s
