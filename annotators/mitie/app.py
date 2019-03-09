
import os
import sys
import json
from os.path import exists
from datetime import datetime
from http import HTTPStatus
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler
)

import mitie


HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))
MODEL = os.getenv('MODEL', 'ru_model.dat')

NER = None


def log(format, *args):
    message = format % args
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, message, file=sys.stderr, flush=True)


def process(text, model):
    tokens = mitie.tokenize(text)
    entities = model.extract_entities(tokens)
    return tokens, entities


def serialize(ner):
    tokens, entities = ner
    tokens = [_.decode('utf8') for _ in tokens]
    entities = [
        [range.start, range.stop, type, weight]
        for range, type, weight in entities
    ]
    return [tokens, entities]


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

        ner = process(text, NER)
        tokens, entities = ner
        log('Processed %d tokens, found %d entities', len(tokens), len(entities))

        data = serialize(ner)
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
        log('Loading %s', MODEL)
        global NER
        NER = mitie.named_entity_extractor(MODEL)
    except Exception as error:
        log('Can not load model: "%s"', error)
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
