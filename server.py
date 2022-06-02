import sys, socket, select

import session

LISTENQUEUE = 32

class Server:
    def __init__(self, ip, port):
        try:
            self.ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.ls.bind((ip, port))
            self.ls.listen(LISTENQUEUE)
        except socket.error as err:
            print(err, file=sys.stderr)
            return
        self.sess = []

    def __del__(self):
        self.ls.close()
        for i in range(len(self.sess)):
            self.close_session(i)

    def accept_client(self):
        self.sess.append(session.Session(self.ls.accept()))

    def close_session(self, i):
        self.sess.pop(i)

    def run(self):
        rlist = [self.ls]

        while True:
            try:
                slist = select.select(rlist, [], [])
            except KeyboardInterrupt:
                break

            if self.ls in slist[0]:
                self.accept_client()
                rlist.append(self.sess[len(self.sess)-1].sd)

            for i in range(len(self.sess)):
                if self.sess[i].sd in slist[0]:
                    res = self.sess[i].handle()
                    if not res:
                        rlist.remove(self.sess[i].sd)
                        self.close_session(i)