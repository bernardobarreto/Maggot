from socket import socket


class HTTPMessage(object):

    def __setitem__(self, key, value):
        self._header[key] = value

    def __getitem__(self, key):
        return self._header[key]

    def __str__(self):
        return "\r\n".join([self.first_line, self.header, "\r\n", self.content])

    @property
    def header(self):
        return "\r\n".join(["%s: %s" % item for item in self._header.items()])


class Request(HTTPMessage):

    def __init__(self, method, path, version):
        self.method = method
        self.path = path
        self.version = version
        self._header = {}
        self.content = ""

    @classmethod
    def parse(cls, text):
        lines = text.split("\r\n")
        first_line = lines.pop(0)
        method, path, version = first_line.split(" ")
        request = Request(method, path, version)
        for line in lines:
            if line.count(": ") == 1:
                key, value = line.split(": ")
                request[key] = value
        return request

    @property
    def first_line(self):
        return " ".join([self.method, self.path, self.version])


class Response(HTTPMessage):

    def __init__(self, version, status, reason):
        self.version = version
        self.status = status
        self.reason = reason
        self._header = {}
        self.content = ""

    @property
    def first_line(self):
        return " ".join([self.version, self.status, self.reason])


class Server(object):

    def __init__(self, port):
        self.port = port
        self.sock = socket()
        self.running = False

    def run(self):
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(100)
        self.running = True
        while self.running:
            client = Client(*self.sock.accept())
            response = client.process_request()
            client.sock.send(str(response))
            client.sock.close()


class Client(object):

    def __init__(self, sock, (ip, port)):
        self.sock = sock
        self.ip = ip
        self.port = port
        self.request = Request.parse(self.sock.recv(5 * 1024 * 1024))

    def process_request(self):
        response = Response(self.request.version, str(200), "OK")
        response["Content-Type"] = "text/html"
        response.content = "xunda"
        return response
