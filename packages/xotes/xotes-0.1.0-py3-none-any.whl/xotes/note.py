import os
import logging
from datetime import datetime

import yaml
from dateutil.tz import tzlocal


class Xote(object):
    def __init__(self, path, docid=None, header_yaml=None):
        self.path = path
        self.docid = docid
        self.__header = None
        self.__body = None
        if header_yaml:
            self.__header = yaml.safe_load(header_yaml)

    def __repr__(self):
        return '<{} {}: {}>'.format(
            self.__class__.__name__,
            self.docid,
            self.path,
        )

    def _load(self):
        logging.debug('loading {}...'.format(self.path))
        header = None
        with open(self.path, 'r') as f:
            # read/parse the yaml header
            while True:
                line = f.readline()
                if not line:
                    break
                if line.strip() == '---':
                    if header is not None:
                        break
                    else:
                        header = ''
                        continue
                header += line
            if not header:
                raise RuntimeError("Note missing header: {}".format(self.path))
            # NOTE: this expects to load unquoted ISO-format strings
            # into datetime objects.  quoted strings are loaded as
            # strings.
            try:
                self.__header = yaml.safe_load(header)
            except yaml.scanner.ScannerError as e:
                raise RuntimeError("Note header could not be parsed: {}".format(self.path))
            # blank line after header
            f.readline()
            self.__body = f.read().strip('\n')

    @property
    def header(self):
        """note header dictionary"""
        if not self.__header:
            self._load()
            if 'title' not in self.__header:
                self.__header['title'] = \
                    self.body.split('\n', 1)[0].strip('#').strip()
        return self.__header

    @property
    def header_yaml(self):
        """header, YAML encoded"""
        return yaml.safe_dump(self.header)

    @property
    def body(self):
        """full text of note"""
        if not self.__body:
            self._load()
        return self.__body

    @property
    def title(self):
        """title of note"""
        return self.header.get('title', '')

    def _parse_header_time(self, key):
        # will return KeyError if not found
        value = self.header[key]
        # header field could be datetime or str
        if isinstance(value, datetime):
            return value
        else:
            # assume it's an ISO string and convert
            return datetime.fromisoformat(value)

    @property
    def created(self):
        """creation time of note"""
        try:
            return self._parse_header_time('created')
        except KeyError:
            return datetime.utcfromtimestamp(os.stat(self.path).st_ctime)

    @property
    def modified(self):
        """last modification time of note"""
        try:
            return self._parse_header_time('modified')
        except KeyError:
            return datetime.utcfromtimestamp(os.stat(self.path).st_mtime)

    def _fmt_time(self, dt):
        return dt.isoformat(timespec='seconds')

    def write(self, title=None, body=None, created=None):
        """write note to path

        Either body or title must be specified.  If either is not
        specified the existing values are used.

        """
        if title is None and body is None:
            raise ValueError("must specify title or body to write to note.")
        if os.path.exists(self.path):
            _created = self.created
            _title = self.title
            _body = self.body
        else:
            _created = datetime.now(tzlocal())
            _title = ''
            _body = ''
        header = {
            'created': self._fmt_time(created or _created),
            'modified': self._fmt_time(datetime.now(tzlocal())),
            'title': title or _title,
        }
        body = body or _body
        logging.debug('writing {}...'.format(self.path))
        with open(self.path, 'w') as f:
            f.write('---\n')
            # NOTE: writes datetime objects as unquoted ISO strings
            yaml.safe_dump(header, f)
            f.write('---\n')
            f.write('\n')
            f.write(body)
            f.write('\n')
        self.__header = None
        self.__body = None
