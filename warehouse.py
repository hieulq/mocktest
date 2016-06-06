class Warehouse(object):
    def __init__(self):
        self.prod = {}

    def remove(self, name, num):
        if self.prod.has_key(name) and self.prod[name] >= num:
            self.prod[name] -= num

    def add(self, name, num):
        if self.prod.has_key(name):
            self.prod[name] += num
        else:
            self.prod[name] = num

    def get_inventory(self, name):
        return self.prod[name]
