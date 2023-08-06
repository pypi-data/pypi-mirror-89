import os
import sys
import logging
import argparse

from . import __version__
from .store import ROOT, XoteStore
from . import util


SESSION_ID = '{}'.format(os.getpid())

if os.getenv('LOG_FILE'):
    level = os.getenv('LOG_LEVEL', 'DEBUG').upper()
else:
    level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=level,
    filename=os.getenv('LOG_FILE'),
    format='{}: %(message)s'.format(SESSION_ID),
)

##################################################

PRINT_FORMAT = {
    'list': 'id:{docid:<{pad}} {title}',
    'full': 'id:{docid:<{pad}} {path} {title}',
    'sexp': '(:id "{docid}" :path "{path}" :title "{title}")',
    'json': '{{"id": "{docid}", "path": "{path}", "title": "{title}"}}',
    'files': '{path}',
    }


def print_note(fmt, note, pad=0):
    print(
        PRINT_FORMAT[fmt].format(
            docid=note.docid,
            path=note.path,
            title=note.title,
            pad=pad,
        )
    )


def edit(note):
    try:
        util.edit_note(note)
    except IOError as e:
        raise SystemExit(f"Error: {e}")
    #util.edit_path(note.path)


##################################################


parser = argparse.ArgumentParser(
    prog='xotes',
    usage="xotes [OPTIONS] [QUERY...]",
    description="""Xotes: simple note management

Xotes are simple markdown files with a YAML header.  All notes are
indexed into a xapian database.  QUERY is a list of search terms
joined with a logical AND (other logical operators may be used if the
xapian interface is available).  The search prefixes "id:" and
"title:" (or "t:") are recognized as well.  Different list formats are
provided.  If no command options are given an ncurses search interface
is presented.""",
    epilog="""
When editing or creating new notes, the note will be opened with
EDITOR, or the default XDG text editor.

If the XOTES_ROOT is not specified, the store lives in an
XDG_DATA_HOME path used.  Your current store path is:

  {}

All notes are stored in a git repository.  Any remotes configured in
the git repo can be synchronized with the local store.  Use the
'--sync' option to synchronize with remotes when executing
commands.""".format(ROOT),
    formatter_class=argparse.RawDescriptionHelpFormatter,
    )

parser.add_argument(
    "query", nargs='*',
    help="search terms")
parser.add_argument(
    '-v', '--version', action='version', version=__version__)
parser.add_argument(
    '-x', '--sync', action='store_true',
    help="sync store with git remotes")
cgroup = parser.add_mutually_exclusive_group()
cgroup.add_argument(
    '-n', '--new', action='store_const', dest='cmd', const='new',
    help="create new note (arguments are initial title)")
cgroup.add_argument(
    '-e', '--edit', action='store_const', dest='cmd', const='edit',
    help="edit note (first line in editor is title)")
cgroup.add_argument(
    '-p', '--print', action='store_const', dest='cmd', const='print',
    help="print note to stdout")
cgroup.add_argument(
    '-d', '--delete', action='store_const', dest='cmd', const='delete',
    help="delete note")
cgroup.add_argument(
    '--delete-force', action='store_const', dest='cmd', const='delete_force',
    help="delete note without prompting")
cgroup.add_argument(
    '-l', '--list', action='store_const', dest='cmd', const='list',
    help="list notes matching search")
cgroup.add_argument(
    '-lf', '--list-full', action='store_const', dest='cmd', const='full',
    help="list notes, including paths")
cgroup.add_argument(
    '-ls', '--list-sexp', action='store_const', dest='cmd', const='sexp',
    help="list notes, s-expression stream")
cgroup.add_argument(
    '-lj', '--list-json', action='store_const', dest='cmd', const='json',
    help="list notes, json stream")
cgroup.add_argument(
    '-f', '--files', action='store_const', dest='cmd', const='files',
    help="print just note file paths")
parser.add_argument(
    '-s', '--sort', choices=['relevance', 'mtime'],
    help="sort notes by relevance or modification time")
parser.add_argument(
    '-r', '--reverse', action='store_true',
    help="reverse sort order")
cgroup.add_argument(
    '-c', '--count', action='store_const', dest='cmd', const='count',
    help="count notes matching search")


def main():
    args = parser.parse_args()
    logging.debug(args)

    cmd = args.cmd
    query = ' '.join(args.query)
    sort = args.sort or 'relevance'
    reverse = bool(args.reverse)

    if cmd == 'new':
        title = query
        with XoteStore() as store:
            if args.sync:
                store.pull()
            note = store.new_note()
            note.write(title=title)
            edit(note)
        XoteStore().push()

    elif cmd == 'edit':
        with XoteStore() as store:
            if args.sync:
                store.pull()
            notes = list(store.search(query))
            if len(notes) != 1:
                sys.exit("Edit query did not match exactly one note.")
            note = notes[0]
            edit(note)
        XoteStore().push()

    elif cmd in ['delete', 'delete_force']:
        with XoteStore() as store:
            if args.sync:
                store.pull()
            notes = list(store.search(query))
            if len(notes) != 1:
                sys.exit("Delete query did not match exactly one note.")
            note = notes[0]
            docid = note.docid
            if cmd != 'delete_force':
                print("Are you sure wish to delete note?:")
                print_note('list', note)
                try:
                    r = input("Type 'yes' to delete: ")
                except KeyboardInterrupt:
                    sys.exit('\nAbort!')
                if r != 'yes':
                    print("Nothing deleted.")
                    sys.exit()
            store.delete_note(note.docid)
            print("Note id:{} deleted.".format(docid))
        XoteStore().push()

    elif cmd == 'print':
        store = XoteStore()
        if args.sync:
            store.pull()
        notes = list(store.search(query))
        if len(notes) != 1:
            sys.exit("Print query did not match exactly one note.")
        note = notes[0]
        with open(note.path) as f:
            print(f.read())

    elif cmd in PRINT_FORMAT:
        store = XoteStore()
        if args.sync:
            store.pull()
        pad = store.docid_pad()
        for note in store.search(query, sort=sort, reverse=reverse):
            print_note(cmd, note, pad)

    elif cmd == 'count':
        store = XoteStore()
        if args.sync:
            store.pull()
        if not query:
            query = '*'
        print(store.count(query))

    elif args.sync:
        XoteStore().sync()

    else:
        try:
            from . import nci
        except ImportError as e:
            sys.exit("error: ncurses interface not available: {}".format(e))
        if not os.getenv('LOG_FILE'):
            logging.getLogger().setLevel(logging.WARNING)
        try:
            with XoteStore() as store:
                store.pull()
                nci.UI(store, query, session_id=SESSION_ID)
        except KeyboardInterrupt:
            pass
        os.system('clear')

##################################################

if __name__ == '__main__':
    main()
