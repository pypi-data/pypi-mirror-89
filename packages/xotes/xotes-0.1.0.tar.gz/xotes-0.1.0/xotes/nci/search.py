import urwid
import collections

from dateutil.tz import tzlocal

from ..util import xclip, datetime_age


############################################################


FOCUS_BG = 'dark gray'

PALETTE = [
    ('header', 'dark gray', 'dark blue'),
    ('header_args', 'dark gray', 'dark blue'),
    ('prefix', 'dark blue, bold', ''),
    ('prefix focus', 'dark blue, bold', FOCUS_BG),
    ('title', 'dark green', ''),
    ('title focus', 'dark green', FOCUS_BG),
    ]

PSELECT = [
    'age',
    'date',
    'datetime',
    'id',
]


class Search(urwid.Frame):

    keys = collections.OrderedDict([
        ('n', "nextEntry"),
        ('down', "nextEntry"),
        ('p', "prevEntry"),
        ('up', "prevEntry"),
        ('N', "pageDown"),
        ('page down', "pageDown"),
        (' ', "pageDown"),
        ('P', "pageUp"),
        ('page up', "pageUp"),
        ('<', "firstEntry"),
        ('>', "lastEntry"),
        ('o', "toggleSort"),
        ('l', "filterSearch"),
        ('meta S', "copy_search"),
        ('-', "cycle_prefix"),
        ('=', "refresh"),
        ])

    __sort = collections.deque(['relevance', 'year'])

    def __init__(self, ui, query=None):
        self.ui = ui
        if not query:
            query = '*'
        self.query = query
        super().__init__(urwid.SolidFill())
        self.__pselect_ind = 0
        self.__set_search()

    @property
    def sort_order(self):
        return self.__sort[0]

    def _pselect(self, cycle=False):
        if cycle:
            self.__pselect_ind = divmod(self.__pselect_ind+1, len(PSELECT))[1]
        return PSELECT[self.__pselect_ind]

    def __set_search(self, cycle=False):
        notes = list(self.ui.db.search(self.query))
        count = len(notes)

        if count == 0:
            self.ui.set_status('No notes found.')
        if count == 1:
            cstring = "%d result" % (count)
        else:
            cstring = "%d results" % (count)

        query = self.query
        htxt = [
            ('pack', urwid.Text("Search: ")),
            ('pack', urwid.AttrMap(urwid.Text("{}".format(query), align='left'), 'header_args')),
            # ('pack', urwid.Text(" [{}]".format(self.sort_order))),
            urwid.Text(cstring, align='right'),
        ]
        header = urwid.AttrMap(urwid.Columns(htxt), 'header')
        self.set_header(header)

        self.lenitems = count
        self.docwalker = DocWalker(self.ui, notes, self._pselect(cycle))
        self.listbox = urwid.ListBox(self.docwalker)
        body = self.listbox
        self.set_body(body)

    def keypress(self, size, key):
        # reset the status on key presses
        self.ui.set_status()
        entry, pos = self.listbox.get_focus()
        # key used if keypress returns None
        if entry and not entry.keypress(size, key):
            return
        # check if we can use key
        elif key in self.keys:
            cmd = eval("self.%s" % (self.keys[key]))
            cmd(size, key)
        # else we didn't use key so return
        else:
            return key

    def help(self):
        def get_keys(o):
            for k, cmd in o.keys.items():
                yield (k, str(getattr(getattr(o, cmd), '__doc__')))
        yield (None, "Note commands:")
        for o in get_keys(DocItem):
            yield o
        yield (None, "Search commands:")
        for o in get_keys(Search):
            yield o

    ##########

    def refresh(self, *args):
        """refresh current search"""
        self.__set_search()
        # FIXME: try to reset position to closet place in search,
        # rather than resetting to the top

    def cycle_prefix(self, *args):
        """cycle entry prefix (age, date, datetime, id)"""
        self.__set_search(cycle=True)

    def toggleSort(self, size, key):
        """toggle search sort order between year/relevance"""
        self.__sort.rotate()
        self.__set_search()

    def filterSearch(self, size, key):
        """modify current search or add additional terms"""
        prompt = 'filter search: {} '.format(self.query)
        self.ui.prompt(
            (self.filterSearch_done, []),
            prompt)

    def filterSearch_done(self, newquery):
        if not newquery:
            self.ui.set_status()
            return
        self.ui.new_buffer('search', self.query+' '+newquery)

    def nextEntry(self, size, key):
        """next entry"""
        entry, pos = self.listbox.get_focus()
        if not entry: return
        if pos + 1 >= self.lenitems: return
        self.listbox.set_focus(pos + 1)

    def prevEntry(self, size, key):
        """previous entry"""
        entry, pos = self.listbox.get_focus()
        if not entry: return
        if pos == 0: return
        self.listbox.set_focus(pos - 1)

    def pageDown(self, size, key):
        """page down"""
        self.listbox.keypress(size, 'page down')
        # self.listbox.set_focus_valign('bottom')
        # self.prevEntry(None, None)

    def pageUp(self, size, key):
        """page up"""
        self.listbox.keypress(size, 'page up')
        # self.listbox.set_focus_valign('top')

    def lastEntry(self, size, key):
        """last entry"""
        self.listbox.set_focus(-1)

    def firstEntry(self, size, key):
        """first entry"""
        self.listbox.set_focus(0)

    def copy_search(self, size, key):
        """copy current search string to clipboard"""
        xclip(self.query)
        self.ui.set_status('yanked search: {}'.format(self.query))

############################################################

class DocWalker(urwid.ListWalker):
    def __init__(self, ui, docs, pselect):
        self.ui = ui
        self.docs = docs
        self.pselect = pselect
        self.ndocs = len(docs)
        self.focus = 0
        self.items = {}

    def __getitem__(self, pos):
        if pos < 0:
            raise IndexError
        if pos not in self.items:
            doc = self.docs[pos]
            self.items[pos] = DocItem(self.ui, doc, self.pselect)
        return self.items[pos]

    def set_focus(self, focus):
        if focus == -1:
            focus = self.ndocs - 1
        self.focus = focus
        self._modified()

    def next_position(self, pos):
        return pos + 1

    def prev_position(self, pos):
        return pos - 1

############################################################

class DocItem(urwid.WidgetWrap):

    keys = collections.OrderedDict([
        ('enter', "view_note"),
        ('e', "edit_note"),
        ('meta i', "copy_id"),
        ('meta p', "copy_path"),
        ])

    def __init__(self, ui, note, pselect):
        self.ui = ui
        self.note = note
        dt = note.modified.astimezone(tzlocal())
        if pselect == 'age':
            prefix = datetime_age(dt)
            width = 10
            align = 'right'
        elif pselect == 'date':
            prefix = dt.strftime('%Y-%m-%d')
            width = 10
            align = 'left'
        elif pselect == 'datetime':
            prefix = dt.strftime('%Y-%m-%d %H:%M')
            width = 16
            align = 'left'
        elif pselect == 'id':
            prefix = 'id:{}'.format(note.docid)
            width = 28
            align = 'left'
        else:
            raise ValueError(f"unknown prefix {prefix}")
        title = note.title
        widget = urwid.AttrMap(
            urwid.Columns([
                ('fixed', width, urwid.Text(prefix, align=align)),
                ('fixed', 1, urwid.Text('')),
                urwid.AttrMap(urwid.Text(title), 'title'),
            ]),
            'prefix')
        w = urwid.AttrMap(
            urwid.AttrMap(widget, 'field'),
            '',
            {'prefix': 'prefix focus',
             'title': 'title focus',
            })
        super().__init__(w)

    def keypress(self, size, key):
        if key in self.keys:
            cmd = eval("self.{}".format(self.keys[key]))
            cmd()
        else:
            return key

    ####################

    def view_note(self):
        """view note"""
        self.ui.new_buffer('view', self.note)

    def edit_note(self):
        """edit note"""
        self.ui.edit_note(self.note.docid)

    def copy_id(self):
        """copy note ID to clipboard"""
        data = 'id:{}'.format(self.note.docid)
        xclip(data)
        self.ui.set_status('yanked id: {}'.format(data))

    def copy_path(self):
        """copy note path to clipboard"""
        data = '{}'.format(self.note.path)
        xclip(data)
        self.ui.set_status('yanked path: {}'.format(data))
