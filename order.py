class Order(object):

    def __init__(self, typ, num):
        self.typ = typ
        self.num = num
        self.filled = False

    def fill(self, wh):
        tmp = wh.get_inventory(self.typ)
        if tmp >= self.num:
            self.filled = True
            wh.remove(self.typ, self.num)

    def is_filled(self):
        return self.filled
