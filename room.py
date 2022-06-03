import session

class Room:
    def __init__(self, rid, sess_name):
        self.id = rid
        self.owner = sess_name
        self.name = f'{sess_name}\'s room'
        self.max_count = 5
        self.sess = []

    def __del__(self):
        while self.sess:
            self.kick(self.sess[0])

    def __is_owner(self, sess):
        return self.owner == sess.get_name()

    def __check_owner(self):
        for sess in self.sess:
            if sess.get_name() == self.owner:
                return
        if self.sess:
            self.owner = self.sess[0].get_name()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_max_count(self):
        return self.max_count

    def count(self):
        return len(self.sess)

    def get_online(self):
        buf = f'[{self.id}] {self.name} ({self.count()}/{self.max_count}):\n'
        for sess in self.sess:
            buf += f'\t{sess.name}'
            if self.__is_owner(sess):
                buf += ' *OWNER'
            buf += '\n'
        return buf

    def add_session(self, sess):
        if self.count() < self.max_count:
            self.sess.append(sess)
            self.send_msg(f'{sess.get_name()} has joined our room!\n',
                          sess, True)
            return True
        return False

    def remove_session(self, sess):
        self.sess.remove(sess)
        self.send_msg(f'{sess.get_name()} has left the room...\n', sess, True)

    def kick(self, sess):
        sess.leave_room()
        self.remove_session(sess)

    def refresh(self):
        i = 0
        while i < len(self.sess):
            if self.sess[i].get_room() != self.id:
                self.remove_session(self.sess[i])
            else:
                i += 1
        self.__check_owner()

    def send_msg(self, msg, exception, prefix=False):
        if prefix:
            msg = '\n> ' + msg
        for sess in self.sess:
            if sess != exception:
                sess.send_msg(msg)

def get_free_rid(r):
    last = -1
    for t in r:
        if t.get_id() - last > 1:
            break
        last = t.get_id()
    return last+1

def get_room_by_id(r, rid):
    for t in r:
        if t.get_id() == rid:
            return t
    return None
