from time import sleep


class FileUtils:
    def __init__(self, **kwargs):
        # Thread.__init__(self)
        if "path" not in kwargs:
            raise ValueError("Path parameters not specified.")

        self.path = kwargs.pop("path")

        if "car" not in kwargs:
            raise ValueError("Car should be specified.")

        self.car = kwargs.pop("car")
        if type(self.car) is not str:
            self.path += "%s.txt" % self.car.name
            if 'position' not in self.car.params:
                print("Car doesn't have position argument. Write_pos method won't work.")
        else:
            self.path += "%s.txt" % self.car

    def write_pos(self):
        with open(self.path, 'a+') as f:
            f.write("%s\n" % str(self.car.params['position']))

    def read_pos(self):
        with open(self.path, 'r') as f:
            last_line = f.read().splitlines()[-1]

        return last_line

    def write_forever(self, stop):
        while True:
            self.write_pos()
            sleep(1)  # wait 1 sec to update again
            if stop():
                break
