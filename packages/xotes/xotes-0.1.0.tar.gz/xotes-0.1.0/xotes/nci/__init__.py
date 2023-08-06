import logging
import subprocess
import collections

import urwid

from .. import util
from . import search
from . import view
from . import help


PALETTE = [
    ('footer', 'light gray', 'dark magenta'),
    ('footer_error', 'white', 'dark red'),
    ('prompt', 'black', 'dark green'),
    ]


class UI():

    keys = collections.OrderedDict([
        ('s', "prompt_search"),
        ('c', "prompt_new_note"),
        ('x', "sync"),
        ('q', "kill_buffer"),
        ('Q', "quit"),
        ('?', "help"),
        ])

    default_status_string = "c: new note, s: search, q: close buffer, Q: quit, ?: help"
    buffers = []
    search_history = []

    def __init__(self, db, query=None, session_id=None):
        self.db = db
        self.session_id = session_id

        # FIXME: set this properly
        self.palette = list(set(PALETTE) | set(search.PALETTE) | set(view.PALETTE))

        self.view = urwid.Frame(urwid.SolidFill())

        self.set_status()

        self.mainloop = urwid.MainLoop(
            self.view,
            self.palette,
            unhandled_input=self.keypress,
            handle_mouse=False,
            )
        self.mainloop.screen.set_terminal_properties(colors=88)

        self.new_buffer('search', '*')
        self.search(query)

        self.mainloop.run()

    ##########

    def set_status(self, text=None, error=False):
        if text:
            T = [urwid.Text(text)]
        else:
            T = [('pack', urwid.Text('[{}]'.format(len(self.buffers)-1))),
                 ('pack', urwid.Text(' Xotes ({})'.format(self.session_id))),
                 urwid.Text(self.default_status_string, align='right'),
                 ]
        if error:
            self.view.set_footer(urwid.AttrMap(urwid.Columns(T), 'footer_error'))
        else:
            self.view.set_footer(urwid.AttrMap(urwid.Columns(T), 'footer'))

    def new_buffer(self, cmd, *args, **kwargs):
        logging.debug("new buffer: {} {}". format(cmd, args))
        if cmd == 'search':
            meth = search.Search
        elif cmd == 'view':
            meth = view.NoteView
        elif cmd == 'help':
            meth = help.Help
        else:
            meth = help.Help
            self.set_status("Unknown command '%s'." % (cmd))
        buf = meth(self, *args, **kwargs)
        self.buffers.append(buf)
        self.view.set_body(buf)
        self.set_status()

    def refresh_buffers(self):
        for buf in self.buffers:
            buf.refresh()

    def kill_buffer(self):
        """close current buffer"""
        if len(self.buffers) == 1:
            return
        self.buffers.pop()
        self.refresh_buffers()
        buf = self.buffers[-1]
        self.view.set_body(buf)
        self.set_status()
        self.mainloop.draw_screen()

    def prompt(self, final, *args, **kwargs):
        """user prompt

        final is a (func, args) tuple to be executed upon complection:
        func(text, *args)

        further args and kwargs are passed to PromptEdit

        """
        pe = PromptEdit(*args, **kwargs)
        urwid.connect_signal(pe, 'done', self.prompt_done, final)
        self.view.set_footer(urwid.AttrMap(pe, 'prompt'))
        self.view.set_focus('footer')

    def prompt_done(self, text, final):
        self.view.set_focus('body')
        urwid.disconnect_signal(self, 'done', self.prompt_done)
        (func, args) = final
        func(text, *args)

    ##########

    def prompt_search(self):
        """search database"""
        prompt = 'search: '
        self.prompt(
            (self.search, []),
            prompt,
            completions=['id:', 'title:'],
            history=self.search_history,
        )

    def search(self, query):
        if not query:
            self.set_status()
            return
        if self.db.count(query) == 1:
            cmd = 'view'
            arg = list(self.db.search(query))[0]
        else:
            cmd = 'search'
            arg = query
        if not self.search_history or query != self.search_history[-1]:
            self.search_history.append(query)
        self.new_buffer(cmd, arg)

    def edit_note(self, docid):
        """edit note"""
        note = self.db[docid]
        # self.set_status("editing {}...".format(docid))
        try:
            util.edit_note(note)
            #util.edit_path(note.path)
        except IOError as e:
            self.set_status(
                "FAILED to edit {}: {}".format(docid, e),
                error=True,
            )
        else:
            self.db.commit()
            self.db.push()
        finally:
            self.mainloop.screen.clear()
            self.refresh_buffers()

    def prompt_new_note(self):
        """create new note"""
        self.prompt(
            (self.new_note, []),
            "new note title: ",
        )

    def new_note(self, title):
        if not title:
            self.set_status()
            return
        note = self.db.new_note()
        note.write(title=title)
        self.edit_note(note.docid)

    def sync(self):
        """sync"""
        # FIXME: use callback to update status
        #self.set_status("syncing...")
        # FIXME: do sync in urwid buffer
        #self.db.sync()
        subprocess.run(
            ['x-terminal-emulator', '-e', 'bash', '-c', 'if ! LOG_LEVEL=DEBUG xotes -x; then read -p : -n 1; fi'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.mainloop.screen.clear()
        self.refresh_buffers()

    def quit(self):
        """quit"""
        raise urwid.ExitMainLoop()

    def help(self):
        """help"""
        self.new_buffer('help', self.buffers[-1])

    def keypress(self, key):
        if key in self.keys:
            cmd = "self.%s()" % (self.keys[key])
            eval(cmd)


##################################################


class PromptEdit(urwid.Edit):
    __metaclass__ = urwid.signals.MetaSignals
    signals = ['done']

    def __init__(self, prompt, initial=None, completions=None, history=None):
        """

        `completions` should be a dictionary keyed by prefix

        """
        super().__init__(caption=prompt)
        if initial:
            self.insert_text(initial)
        self.completions = completions
        self.completion_data = {}
        self.history = history
        self.history_pos = -1
        self.last_text = ''

    def keypress(self, size, key):
        if self.last_text and self.edit_text != self.last_text:
            self.completion_data.clear()
            self.history_pos = -1

        if key == 'enter':
            urwid.emit_signal(self, 'done', self.get_edit_text())
            return
        elif key in ['esc', 'ctrl g']:
            urwid.emit_signal(self, 'done', None)
            return

        # navigation
        elif key == 'ctrl a':
            # move to beginning
            key = 'home'
        elif key == 'ctrl e':
            # move to end
            key = 'end'
        elif key == 'ctrl b':
            # back character
            self.set_edit_pos(self.edit_pos-1)
        elif key == 'ctrl f':
            # forward character
            self.set_edit_pos(self.edit_pos+1)
        elif key == 'meta b':
            # back word
            text = self.edit_text
            pos = self.edit_pos - 1
            inword = False
            while True:
                try:
                    text[pos]
                except IndexError:
                    break
                if text[pos] != ' ' and not inword:
                    inword = True
                    continue
                if inword:
                    if text[pos] == ' ':
                        break
                pos -= 1
            self.set_edit_pos(pos+1)
        elif key == 'meta f':
            # forward word
            text = self.edit_text
            pos = self.edit_pos
            inword = False
            while True:
                try:
                    text[pos]
                except IndexError:
                    break
                if text[pos] != ' ' and not inword:
                    inword = True
                    continue
                if inword:
                    if text[pos] == ' ':
                        break
                pos += 1
            self.set_edit_pos(pos+1)

        # deletion
        elif key == 'ctrl d':
            # delete character
            text = self.edit_text
            pos = self.edit_pos
            ntext = text[:pos] + text[pos+1:]
            self.set_edit_text(ntext)
        elif key == 'ctrl k':
            # delete to end
            self.set_edit_text(self.edit_text[:self.edit_pos])

        # history
        elif key in ['up', 'ctrl p']:
            if self.history:
                if self.history_pos == -1:
                    self.history_full = self.history + [self.edit_text]
                try:
                    self.history_pos -= 1
                    self.set_edit_text(self.history_full[self.history_pos])
                    self.set_edit_pos(len(self.edit_text))
                except IndexError:
                    self.history_pos += 1
        elif key in ['down', 'ctrl n']:
            if self.history:
                if self.history_pos != -1:
                    self.history_pos += 1
                    self.set_edit_text(self.history_full[self.history_pos])
                    self.set_edit_pos(len(self.edit_text))

        # tab completion
        elif key == 'tab' and self.completions:
            # tab complete on individual words

            # retrieve current text and position
            text = self.edit_text
            pos = self.edit_pos

            # find the completion prefix
            tpos = pos - 1
            while True:
                try:
                    if text[tpos] == ' ':
                        tpos += 1
                        break
                except IndexError:
                    break
                tpos -= 1
            prefix = text[tpos:pos]
            # FIXME: this prefix stripping should not be done here
            prefix = prefix.lstrip('+-')
            # find the end of the word
            tpos += 1
            while True:
                try:
                    if text[tpos] == ' ':
                        break
                except IndexError:
                    break
                tpos += 1

            # record/clear completion data
            if self.completion_data:
                # clear the data if the prefix is new
                if prefix != self.completion_data['prefix']:
                    self.completion_data.clear()
                # otherwise rotate the queue
                else:
                    self.completion_data['q'].rotate(-1)
            else:
                self.completion_data['prefix'] = prefix
                # harvest completions
                q = collections.deque()
                for c in self.completions:
                    if c.startswith(prefix):
                        q.append(c)
                self.completion_data['q'] = q

            logging.debug(self.completion_data)

            # insert completion at point
            if self.completion_data and self.completion_data['q']:
                c = self.completion_data['q'][0][len(prefix):]
                ntext = text[:pos] + c + text[tpos:]
                self.set_edit_text(ntext)
                self.set_edit_pos(pos)

        # record the last text
        self.last_text = self.edit_text
        return super().keypress(size, key)
