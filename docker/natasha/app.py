

import os
import sys
import json
from datetime import datetime
from http import HTTPStatus
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler
)

from natasha import (
    NamesExtractor,
    OrganisationExtractor,
    LocationExtractor,
)
from natasha.extractors import serialize as serialize_match


HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

CONSTRUCTORS = [
    NamesExtractor,
    OrganisationExtractor,
    LocationExtractor,
]
EXTRACTORS = []


def log(format, *args):
    message = format % args
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, message, file=sys.stderr, flush=True)


def process(text, extractors):
    matches = []
    for extractor in extractors:
        matches.extend(extractor(text))
    return sorted(matches, key=lambda _: _.span)


def serialize(matches):
    data = []
    for match in matches:
        data.append(serialize_match(match))
    return data


class HTTPHandler(BaseHTTPRequestHandler):
    error_message_format = '%(message)s'
    error_content_type = 'text/plain; charset=utf-8'

    def log_message(self, format, *args):
        # custom logging in do_POST
        pass

    def do_POST(self):
        if self.path != '/':
            self.send_error(
                HTTPStatus.NOT_FOUND,
                'Bad path: %r' % self.path
            )
            return

        length = self.headers.get('Content-Length')
        if not length or not length.isdigit():
            self.send_error(
                HTTPStatus.LENGTH_REQUIRED,
                'Bad Content-Length: %r' % length
            )
            return

        text = self.rfile.read(int(length))
        try:
            text = text.decode('utf8')
        except UnicodeDecodeError as error:
            self.send_error(
                HTTPStatus.BAD_REQUEST,
                'Unicode error: "%s"' % error
            )
            return

        matches = process(text, EXTRACTORS)
        log('Processed %d chars, %d matches', len(text), len(matches))

        data = serialize(matches)
        response = json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ).encode('utf8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(response)


def main():
    try:
        global EXTRACTORS
        for constructor in CONSTRUCTORS:
            log('Init %s', constructor.__name__)
            extractor = constructor()
            EXTRACTORS.append(extractor)
    except Exception as error:
        log('Can not init: "%s"', error)
        return

    server = HTTPServer((HOST, PORT), HTTPHandler)
    try:
        log('Listening http://%s:%d', HOST, PORT)
        server.serve_forever()
    except KeyboardInterrupt:
        log('Quiting')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
