import os
import xapian
import logging

from .note import Xote


class XoteDatabaseError(Exception):
    pass


class XoteDatabase():
    """Xotes xapian database"""

    # https://xapian.org/docs/omega/termprefixes.html
    BOOLEAN_PREFIX = {
        'id': 'Q',
        }

    PROBABILISTIC_PREFIX = {
        'title': 'S',
        't': 'S',
        }

    # purely internal prefixes (not added to query parser)
    BOOLEAN_PREFIX_INTERNAL = {
        'file': 'F',
        }

    # value facets
    # https://xapian.org/docs/facets
    # https://getting-started-with-xapian.readthedocs.io/en/latest/concepts/indexing/values.html
    FACET = {
        'mtime': 0,
        }

    # FIXME: need database version

    def _prefix(self, name, value=None):
        prefix = dict(
            self.BOOLEAN_PREFIX,
            **self.PROBABILISTIC_PREFIX,
            **self.BOOLEAN_PREFIX_INTERNAL,
        )[name]
        if value:
            return '{}{}'.format(prefix, value)
        else:
            return prefix

    def _facet(self, name):
        return self.FACET[name]

    ########################################

    def __init__(self, root, writable=False):
        self.root = root
        self.db_root = os.path.join(self.root, '.xapian')
        self.new = False
        if writable:
            if not os.path.exists(self.db_root):
                self.new = True
            try:
                self.xapian = xapian.WritableDatabase(self.db_root, xapian.DB_CREATE_OR_OPEN)
            except xapian.DatabaseLockError:
                raise XoteDatabaseError("xotes xapian database locked.")
        else:
            if not os.path.exists(self.db_root):
                raise XoteDatabaseError("xapian db does not exist.")
            self.xapian = xapian.Database(self.db_root)

        stemmer = xapian.Stem("english")

        # The Xapian TermGenerator
        # http://trac.xapian.org/wiki/FAQ/TermGenerator
        self.term_gen = xapian.TermGenerator()
        self.term_gen.set_stemmer(stemmer)

        # The Xapian QueryParser
        self.query_parser = xapian.QueryParser()
        self.query_parser.set_database(self.xapian)
        self.query_parser.set_stemmer(stemmer)
        self.query_parser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        self.query_parser.set_default_op(xapian.Query.OP_AND)

        # add boolean internal prefixes
        for name, prefix in self.BOOLEAN_PREFIX.items():
            self.query_parser.add_boolean_prefix(name, prefix)

        # add probabalistic prefixes
        for name, prefix in self.PROBABILISTIC_PREFIX.items():
            self.query_parser.add_prefix(name, prefix)

        # add facets
        for name, facet in self.FACET.items():
            self.query_parser.add_valuerangeprocessor(
                xapian.NumberValueRangeProcessor(facet, name+':')
                )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.xapian.close()

    def reopen(self):
        self.xapian.reopen()

    ########################################

    def _doc_for_id(self, docid):
        """Get document for docid"""
        # https://trac.xapian.org/wiki/FAQ/UniqueIds
        term = self._prefix('id', docid)
        postlist = self.xapian.postlist(term)
        try:
            plitem = next(postlist)
        except StopIteration:
            raise xapian.DocNotFoundError(docid)
        return self.xapian.get_document(plitem.docid)

    def __contains__(self, docid):
        try:
            self._doc_for_id(docid)
            return True
        except xapian.DocNotFoundError:
            return False

    # generate a new doc id, based on the last availabe doc id
    def _generate_docid(self):
        return self.xapian.get_lastdocid() + 1

    ########################################

    def _term_iter(self, xapian_object, name=None):
        """Generator of terms in the database.

        `xapian_object` can be either the full database or a single
        document.  If a prefix name is provided, will iterate over
        only the prefixed terms, and the prefix will be removed from
        the returned terms.

        """
        prefix = None
        plen = 0
        if name:
            prefix = self._prefix(name)
            plen = len(prefix)

        term_iter = iter(xapian_object)
        # skip straight to terms with prefix
        if prefix:
            term = term_iter.skip_to(prefix).term.decode()
            if not term.startswith(prefix):
                return
            yield term[plen:]
        for tli in term_iter:
            term = tli.term.decode()
            if prefix and not term.startswith(prefix):
                break
            yield term[plen:]

    def _search(self, query_string, sort='relevance', reverse=False, limit=None):
        """Generator of database documents from query

        """
        if query_string == "*":
            query = xapian.Query.MatchAll
        else:
            # parse the query string to produce a Xapian::Query object.
            query = self.query_parser.parse_query(query_string)

        # FIXME: need to catch Xapian::Error when using enquire
        enquire = xapian.Enquire(self.xapian)
        enquire.set_query(query)

        if sort == 'relevance':
            enquire.set_sort_by_relevance_then_value(self._facet('mtime'), True)
        elif sort == 'mtime':
            enquire.set_sort_by_value_then_relevance(self._facet('mtime'), True)
        else:
            raise ValueError("Sort parameter must be 'relevance' or 'mtime' (not '{}').".format(sort))

        # FIXME: why is this not working??
        enquire.set_weighting_scheme(xapian.BoolWeight())
        if reverse:
            enquire.set_docid_order(xapian.Enquire.DESCENDING)
        else:
            enquire.set_docid_order(xapian.Enquire.ASCENDING)

        logging.debug("xapian query string: {}".format(query_string))
        logging.debug("xapian final query: {}".format(query))
        logging.debug("xapian enquire sort: {} (reverse={})".format(sort, reverse))

        if limit:
            mset = enquire.get_mset(0, limit)
        else:
            mset = enquire.get_mset(0, self.xapian.get_doccount())

        return mset

    ########################################

    def update(self, doc_iter):
        """Update the database.

        This does a scan for all notes in the root path and updates
        them in the database if they modification time is newer than
        what is stored in the database.  This also incorporates new
        notes that have shown up in the store, and deletes notes that
        have been removed from the store.

        """
        # FIXME: directory mtime isn't updated if file contents are
        # modified, so need better check here. just skip for now
        #
        # if not self.new and \
        #    os.stat(self.root).st_mtime <= os.stat(self.db_root).st_mtime:
        #     logging.debug("db: up-to-date.")
        #     return

        logging.debug("db scan...")
        for note in doc_iter:
            # logging.debug('  {}'.format(note))

            # retrieve db document, or create new if not found
            try:
                doc = self._doc_for_id(note.docid)
            except xapian.DocNotFoundError:
                doc = xapian.Document()
                doc.add_term(self._prefix('id', note.docid))
                doc.add_term(self._prefix('file', note.path))
                doc.add_value(self._facet('mtime'), xapian.sortable_serialise(0))

            # check if file mtime is later than what's been recorded
            note_mtime = os.stat(note.path).st_mtime
            db_mtime = xapian.sortable_unserialise(doc.get_value(self._facet('mtime')))
            if note_mtime <= db_mtime:
                continue

            logging.info("updating id:{}...".format(note.docid))

            term_gen = self.term_gen
            term_gen.set_document(doc)

            # generate basic and prefixed terms for title
            term_gen.index_text(note.title)
            term_gen.index_text(note.title, 1, self._prefix('title'))

            # generate basic terms from note text
            term_gen.index_text(note.body)

            # store full header structure as data
            # FIXME: should this be encoded somehow?
            doc.set_data(note.header_yaml)

            # add mtime value
            doc.add_value(self._facet('mtime'), xapian.sortable_serialise(note_mtime))

            # replace document in db
            self.xapian.replace_document(self._prefix('id', note.docid), doc)

        # handle deletes
        for match in self._search('*'):
            path = next(self._term_iter(match.document, 'file'))
            if not os.path.exists(path):
                docid = next(self._term_iter(match.document, 'id'))
                self.__delitem__(docid)

    def __delitem__(self, docid):
        """Delete note by docid."""
        logging.info("deleting id:{}...".format(docid))
        self.xapian.delete_document(self._prefix('id', docid))

    ########################################

    def _doc2note(self, doc):
        """Return Xote note for xapian doc."""
        # FIXME: check that these lists aren't longer than one
        path = next(self._term_iter(doc, 'file'))
        docid = next(self._term_iter(doc, 'id'))
        # FIXME: should this decode?
        header = doc.get_data()
        return Xote(path, docid, header_yaml=header)

    def __getitem__(self, docid):
        """Retrieve note directly by docid."""
        doc = self._doc_for_id(docid)
        return self._doc2note(doc)

    def search(self, *args, **kwargs):
        """Generator of notes matching query

        The `sort` keyword argument can be 'relevance' (default) or
        'mtime'.  If `reverse` is True, the sort order is reversed.
        `limit` can be used to limit the number of returned documents
        (default is None to return all notes matching query).

        """
        for match in self._search(*args, **kwargs):
            yield self._doc2note(match.document)

    def count(self, query_string):
        """Count notes matching search terms.

        """
        return self._search(query_string).get_matches_estimated()
