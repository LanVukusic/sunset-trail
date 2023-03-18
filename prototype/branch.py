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

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        if isinstance(other, float):
            return Point(self.x * other, self.y * other)
        raise Exception("Invalid type")


BRANCHING_PROBABILITY = 0.2
# normal branch grouwth direction
DIRECTION_LOW = Point(10, 17).normalize()
DIRECTION_HIGH = Point(10, -17).normalize()

NEW_BRANCH_DIRECTION_HIGH = Point(0, 12)
NEW_BRANCH_DIRECTION_LOW = Point(0, 5)

branches = []


def lerpPoint(a: Point, b: Point, t: float):
    return Point(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t)


def create_brach(start: Point, maxLen: float, direction: Point, depth=1, width=0):
    if maxLen < 1:
        return

    points = []

    i = 0
    prev_point = start
    prev_direction = direction

    # plot the branch origin point
    plt.plot(start.x, start.y, "x", color="red")

    remainingLen = maxLen
    while remainingLen > 1:
        u = i / maxLen

        if (i + 1) % 4 == 0 and i >= 2:
            # mirror i-2 point over i-1 point
            new_direction = prev_point - points[-2]
            new_point = prev_point + (new_direction)
            # plot point with a circle
            plt.plot(new_point.x, new_point.y, "o", color="purple", markersize=7)

        else:
            # calculate direction
            new_direction = lerpPoint(DIRECTION_LOW, DIRECTION_HIGH, random.random())
            # new_direction.normalize()
            new_direction = (prev_direction * 0.2 + new_direction * 0.8).normalize()

            # calculate point
            new_point = prev_point + new_direction * (8.0)
            # plot point with a circle
            plt.plot(new_point.x, new_point.y, "o", color="orange", markersize=7)

        # plot the branch as a line
        plt.plot(
            [prev_point.x, new_point.x],
            [prev_point.y, new_point.y],
            color="green",
            linewidth=(1 - u) * 4,
        )

        points.append(new_point)

        # line width based on provided width, decreasing with i
        width = width - 0.1
        # mybe branch
        if i > 2 and remainingLen > 10 and depth < 3:
            if BRANCHING_PROBABILITY / (math.log(depth + 0.5) * 2) > random.random():
                branching_dir = lerpPoint(
                    NEW_BRANCH_DIRECTION_LOW,
                    NEW_BRANCH_DIRECTION_HIGH,
                    random.random(),
                )
                if random.random() > 0.5:
                    branching_dir = Point(branching_dir.x, -branching_dir.y)
                branching_dir.normalize()

                new_branch_dir = branching_dir + new_direction
                create_brach(
                    prev_point,
                    int(remainingLen / (depth + 0.3)),
                    new_branch_dir,
                    depth + 1,
                    width,
                )

        prev_point = new_point
        prev_direction = new_direction
        remainingLen -= 1
        i += 1

    branches.append(points)


def flatten(points: list[Point]):

    out = []
    for point_i in range(0, len(points), 3):
        print(point_i)
        if point_i + 3 >= len(points):
            break
        out.append(points[point_i].x)
        out.append(points[point_i].y)

        out.append(points[point_i + 1].x)
        out.append(points[point_i + 1].y)

        out.append(points[point_i + 2].x)
        out.append(points[point_i + 2].y)

        out.append(points[point_i + 3].x)
        out.append(points[point_i + 3].y)

    return out[: len(out) - (len(out) - 1) % 4]


def main():
    # plt.ion()
    # plt.show()
    while True:
        create_brach(Point(0, 0), 50, Point(1, 0), 1, 10)

        # plt.ioff()
        ax = plt.gca()
        ax.set_aspect("equal", adjustable="box")
        print()
        print("Branches: ", len(branches[0]))
        print(flatten(branches[0]))
        plt.show()


if __name__ == "__main__":
    main()
