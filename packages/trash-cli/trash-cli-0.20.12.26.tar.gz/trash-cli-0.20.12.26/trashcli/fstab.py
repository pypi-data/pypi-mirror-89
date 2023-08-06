import os


def volume_of(path) :
    func = VolumeOf(os.path.ismount, os.path.abspath)
    return func(path)

class FakeFstab:
    def __init__(self):
        self.ismount = FakeIsMount()
        self.volume_of = VolumeOf(self.ismount, os.path.normpath)

    def mount_points(self):
        return self.ismount.mount_points()

    def volume_of(self, path):
        volume_of = VolumeOf(self.ismount, os.path.abspath)
        return volume_of(path)

    def add_mount(self, path):
        self.ismount.add_mount(path)

from trashcli.list_mount_points import os_mount_points
class OsIsMount:
    def __call__(self, path):
        return os.path.ismount(path)
    def mount_points(self):
        return os_mount_points()

class FakeIsMount:
    def __init__(self):
        self.fakes = set(['/'])
    def add_mount(self, path):
        self.fakes.add(path)
    def __call__(self, path):
        if path == '/':
            return True
        path = os.path.normpath(path)
        if path in self.fakes:
            return True
        return False

class VolumeOf:
    def __init__(self, ismount, abspath):
        self.ismount = ismount
        self.abspath = abspath

    def __call__(self, path):
        path = self.abspath(path)
        while path != os.path.dirname(path):
            if self.ismount(path):
                break
            path = os.path.dirname(path)
        return path

