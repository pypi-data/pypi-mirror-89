from qtpy import QtGui

from prettyqt import core


class Vector3D(QtGui.QVector3D):
    # def __repr__(self):
    #     return f"{type(self).__name__}()"
    pass

    def __bool__(self):
        return not self.isNull()

    def __abs__(self) -> float:
        return self.length()

    def to_point(self) -> core.Point:
        return core.Point(self.toPoint())

    def to_pointf(self) -> core.PointF:
        return core.PointF(self.toPointF())


if __name__ == "__main__":
    vector = Vector3D(0, 0, 1)
    print(abs(vector))
