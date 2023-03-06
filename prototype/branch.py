import matplotlib.pyplot as plt
import random
import math


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return (self.x**2 + self.y**2) ** 0.5

    def normalize(self):
        length = self.length()
        self.x /= length
        self.y /= length
        return self

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float):
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        if isinstance(other, float):
            return Point(self.x * other, self.y * other)
        raise Exception("Invalid type")


BRANCHING_PROBABILITY = 0.2
# normal branch grouwth direction
DIRECTION_LOW = Point(10, 9).normalize()
DIRECTION_HIGH = Point(10, -9).normalize()

NEW_BRANCH_DIRECTION_HIGH = Point(0, 5)
NEW_BRANCH_DIRECTION_LOW = Point(0, -5)


def lerpPoint(a: Point, b: Point, t: float):
    return Point(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t)


def create_brach(start: Point, maxLen: float, direction: Point, depth=1):
    if maxLen < 1:
        return

    prev_point = start
    prev_direction = direction

    # plot the branch origin point
    plt.plot(start.x, start.y, "x", color="red")

    remainingLen = maxLen
    while remainingLen > 1:
        # calculate direction
        new_direction = lerpPoint(DIRECTION_LOW, DIRECTION_HIGH, random.random())
        # new_direction.normalize()
        new_direction = (prev_direction * 0.2 + new_direction * 0.8).normalize()

        # calculate point
        new_point = prev_point + new_direction * (float(remainingLen) * 5.0)

        # plot the branch as a line
        plt.plot(
            [prev_point.x, new_point.x], [prev_point.y, new_point.y], color="black"
        )

        # mybe branch
        if remainingLen > 5 and depth < 3:
            if BRANCHING_PROBABILITY / (math.log(depth + 0.2) * 2) > random.random():
                branching_dir = lerpPoint(
                    NEW_BRANCH_DIRECTION_LOW, NEW_BRANCH_DIRECTION_HIGH, random.random()
                )
                new_branch_dir = branching_dir + new_direction
                create_brach(
                    prev_point, int(remainingLen / 1.7), new_branch_dir, depth + 1
                )

        prev_point = new_point
        prev_direction = new_direction
        remainingLen -= 1


def main():
    # plt.ion()
    # plt.show()
    while True:
        create_brach(Point(0, 0), 20, Point(1, 0))

        # plt.ioff()
        ax = plt.gca()
        ax.set_aspect("equal", adjustable="box")
        plt.show()


if __name__ == "__main__":
    main()
