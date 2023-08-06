import subprocess
import collections

import urwid

from ..util import xclip, extract_urls


############################################################


PALETTE = [
    ('header', 'black', 'dark blue'),
]


class NoteView(urwid.Frame):

    keys = collections.OrderedDict([
        ('enter', "edit_note"),
        ('e', "edit_note"),
        ('r', "view_raw"),
        ('u', "open_urls"),
        ('d', "delete_note"),
        ('meta i', "copy_id"),
        ('meta p', "copy_path"),
        ('=', "refresh"),
        ])

    def __init__(self, ui, note, raw=False):
        self.ui = ui
        self.note = note
        self.raw = raw
        super().__init__(urwid.SolidFill())
        self.__set_view()

    def __set_view(self):
        # td = datetime.now(timezone.utc) - note.modified
        # ts = str(timedelta(seconds=td.seconds)) + ' ago'
        ts = self.note.modified.date()
        header = urwid.AttrMap(
            urwid.Columns(
                [urwid.Text('{}'.format(self.note.title)),
                 #('pack', urwid.Text('id:{}'.format(note.docid), align='right')),
                 #('pack', urwid.Text(' (last modified: {})'.format(ts), align='right')),
                 ('pack', urwid.Text('last modified: {}'.format(ts), align='right')),
                 ]
            ),
            'header')
        self.set_header(header)

        if self.raw:
            with open(self.note.path) as f:
                text = f.read().splitlines()
        else:
            text = [''] + self.note.body.splitlines()
        # from pygments import highlight
        # from pygments.lexers import MarkdownLexer
        # from pygments.formatters import HtmlFormatter
        # text = highlight(text, MarkdownLexer(), HtmlFormatter())
        body = urwid.ListBox(urwid.SimpleListWalker(
            [urwid.Text(s) for s in text]
        ))
        self.set_body(body)

    def refresh(self, *args):
        self.note._load()
        self.__set_view()

    def help(self):
        def get_keys(o):
            for k, cmd in o.keys.items():
                yield (k, str(getattr(getattr(o, cmd), '__doc__')))
        yield (None, "View commands:")
        for o in get_keys(NoteView):
            yield o

    def keypress(self, size, key):
        if key == ' ':
            return self.get_body().keypress(size, 'page down')
        elif key in self.keys:
            cmd = eval("self.%s" % (self.keys[key]))
            cmd(size, key)
        else:
            return super().keypress(size, key)

    def edit_note(self, size, key):
        """edit note"""
        self.ui.edit_note(self.note.docid)

    def view_raw(self, size, key):
        """view raw note"""
        self.ui.new_buffer('view', self.note, raw=True)

    def delete_note(self, size, key):
        """delete note"""
        self.ui.prompt((self.delete_note_done, []),
                       "Definitely delete this note? Type 'yes' to delete: ")

    def delete_note_done(self, confirm):
        if not confirm or confirm.lower() != 'yes':
            self.ui.set_status()
            #self.ui.mainloop.draw_screen()
            return
        with self.ui.db as store:
            store.delete_note(self.note.docid)
        self.ui.db.push()
        self.ui.kill_buffer()

    def copy_id(self, size, key):
        """copy note ID to clipboard"""
        data = 'id:{}'.format(self.note.docid)
        xclip(data)
        self.ui.set_status('yanked id: {}'.format(data))

    def copy_path(self, size, key):
        """copy note path to clipboard"""
        data = '{}'.format(self.note.path)
        xclip(data)
        self.ui.set_status('yanked path: {}'.format(data))

    def open_urls(self, size, key):
        """open all URLs in note"""
        urls = extract_urls(self.note.body)
        # FIXME: can we open multiple URLs in a generic way?
        for url in urls:
            subprocess.Popen(['xdg-open', url])
