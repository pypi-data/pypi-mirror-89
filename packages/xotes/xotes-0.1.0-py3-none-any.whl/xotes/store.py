import os
import re
import git
import uuid
import logging

from .note import Xote
try:
    from .db import XoteDatabase
except ModuleNotFoundError:
    XoteDatabase = None


ROOT = os.getenv('XOTES_ROOT')
if not ROOT:
    XDG_DATA_HOME = os.getenv(
        'XDG_DATA_HOME',
        os.path.join('~', '.local', 'share'),
    )
    ROOT = os.path.join(XDG_DATA_HOME, 'xotes', 'store')
ROOT = os.path.expanduser(ROOT)


PREFIX_REGEXP = {
    'id': r'id:(\S*)',
    'title': r'title|t:(\S*)',
}


def create_gitignore(root):
    gitignore = os.path.join(root, '.gitignore')
    if os.path.exists(gitignore):
        return gitignore
    with open(gitignore, 'w') as f:
        f.write('.xapian\n')
        f.write('*~\n')
        f.write('\#*\n')
    return gitignore


class XoteStore(object):
    def __init__(self, root=ROOT):
        self.root = os.path.abspath(os.path.expanduser(root))

        # check for store git repo or initialize if doesn't exist
        try:
            self.repo = git.Repo(self.root)
        #except git.exc.InvalidGitRepositoryError:
        except git.exc.NoSuchPathError:
            if not os.path.exists(self.root):
                os.makedirs(self.root)
            self.repo = git.Repo.init(self.root)
            gitignore = create_gitignore(self.root)
            self.repo.index.add([gitignore])
            self.repo.index.commit("Xotes initial commit")

        gitignore = create_gitignore(self.root)
        if gitignore:
            # FIXME: don't add if we don't need to
            self.repo.index.add([gitignore])

        if XoteDatabase:
            with XoteDatabase(self.root, writable=True) as db:
                db.update(self)
            self.db = XoteDatabase(self.root)
        else:
            self.db = None

    def __path_for_docid(self, docid):
        """filesystem path string for docid"""
        return os.path.join(self.root, '{}.md'.format(docid))

    def __iter__(self):
        """iterator of notes in store

        """
        for f in sorted(os.listdir(self.root)):
            try:
                docid, ext = f.split('.', 1)
            except ValueError:
                continue
            if ext != 'md':
                continue
            path = self.__path_for_docid(docid)
            yield Xote(path, docid)

    def commit(self):
        """commit note changes to archive"""
        if self.db:
            with XoteDatabase(self.db.root, writable=True) as db:
                db.update(self)
        # FIXME: why do we have to call out to git for this?
        # this should return string if there are untracked or modified
        # files
        # if self.repo.git.status('--porcelain'):
        #
        # NOTE: this is not sufficient for handling deletes:
        # https://github.com/gitpython-developers/GitPython/issues/351
        # self.repo.index.add(self.repo.untracked_files)
        # self.repo.index.add(self.repo.git.diff(name_only=True).splitlines())
        self.repo.git.add(all=True)
        if self.repo.is_dirty():
            self.repo.index.commit("Xotes commit")

    def pull(self):
        for remote in self.repo.remotes:
            logging.info("git pull {}...".format(remote))
            try:
                remote.pull()
            except Exception as e:
                logging.warning("WARNING: could not pull from remote {}:".format(remote))
                logging.warning(e)

    def push(self):
        for remote in self.repo.remotes:
            logging.info("git push {}...".format(remote))
            try:
                remote.push()
            except Exception as e:
                logging.warning("WARNING: could not push to remote {}:".format(remote))
                logging.warning(e)

    def sync(self):
        """sync repo with remotes"""
        for remote in self.repo.remotes:
            logging.info("git sync {}...".format(remote))
            try:
                remote.pull()
                remote.push()
            except Exception as e:
                logging.warning("WARNING: could not sync remote {}:".format(remote))
                logging.warning(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # FIXME: do something with exceptions (reset index?)
        self.commit()

    def __repr__(self):
        return '<{}({!r})>'.format(self.__class__.__name__,
                                   self.root)

    ##########

    def docid_pad(self):
        """length of string representation of largest docid in store"""
        # FIXME: how to determine this better
        # len('2020-01-25T01:25:07-08:00')
        return 36

    def __generate_docid(self, dt=None):
        """generate new docid"""
        return uuid.uuid4()

    def __contains__(self, docid):
        """True if store contains docid"""
        return os.path.exists(self.__path_for_docid(docid))

    def __getitem__(self, docid):
        """retrieve note by id

        """
        path = self.__path_for_docid(docid)
        if not os.path.exists(path):
            raise KeyError("No note id:{}".format(docid))
        return Xote(path, docid)

    def __len__(self):
        """number of notes in database"""
        return len(list(self))

    def new_note(self):
        """Create and return a new note object in the store

        It's up to the caller to call the write method on the note
        object to actually write the new note to the store.

        """
        docid = self.__generate_docid()
        path = self.__path_for_docid(docid)
        assert not os.path.exists(path), "note already exists at {}".format(path)
        return Xote(path, docid)

    def delete_note(self, docid):
        """delete note from store"""
        path = self.__path_for_docid(docid)
        os.remove(path)
        if self.db:
            with XoteDatabase(self.db.root, writable=True) as db:
                del db[docid]

    ##########

    def _fmt_query(self, query):
        if not query:
            return '*'
        elif isinstance(query, str):
            return query
        elif isinstance(query, list):
            return ' ' .join(query)
        else:
            raise ValueError("unsupported value for query: {}".format(type(query)))

    def search(self, query=None, sort='relevance', reverse=False):
        """Generator of notes matching query

        `query` should be a string or list of terms to match with AND
        in notes.  If the query contains an 'id:' string that matches
        a note document id then that note will be returned.  The
        prefix 'title:' can be used to search note titles.

        """
        query_string = self._fmt_query(query)
        logging.debug("search query: {}".format(query_string))

        # if we have a db use it's search
        if self.db:
            self.db.reopen()
            for note in self.db.search(query_string, sort=sort, reverse=reverse):
                yield note
            return

        # if we don't have a db we do a very simple "grep" search for
        # words in note matching query terms

        if query_string == '*':
            for note in self:
                yield note
            return

        # parse the query
        prefix_re = {}
        prefix_terms = {}
        for prefix, regexp in PREFIX_REGEXP.items():
            prefix_re[prefix] = re.compile(regexp, re.IGNORECASE)
            prefix_terms[prefix] = set()
        terms = set()
        for word in ' '.join(query).split():
            for prefix, regexp in prefix_re.items():
                match = regexp.fullmatch(word)
                if match:
                    prefix_terms[prefix].add(match.groups()[0])
                    break
            if not match:
                terms.add(word.lower())

        if prefix_terms['id']:
            if len(prefix_terms['id']) == 1 and not terms and not prefix_terms['title']:
                try:
                    yield self[list(prefix_terms['id'])[0]]
                except KeyError:
                    pass
            return

        # scan the notes
        for note in self:
            body_text = set([s.lower() for s in note.body.split()])
            title_text = set([s.lower() for s in note.title.split()])
            if prefix_terms['title'] and not (prefix_terms['title'] & title_text):
                continue
            if terms and not (terms & (title_text | body_text)):
                continue
            yield note

    def count(self, query=None):
        """Count notes for search."""
        query_string = self._fmt_query(query)
        if self.db:
            self.db.reopen()
            return self.db.count(query_string)
        else:
            return len(list(self.search(query)))
