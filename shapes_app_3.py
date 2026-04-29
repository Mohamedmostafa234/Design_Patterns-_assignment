import copy
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Singleton - Drawing Canvas
# only one canvas should exist at a time, thats the whole point

class Canvas:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.shapes = []
            print("Canvas ready.")
        return cls._instance

    def add(self, shape):
        self.shapes.append(shape)

    def show(self):
        print("\n== Shapes on canvas ==")
        for s in self.shapes:
            s.draw()
        print("======================\n")


# Prototype - Shape base class
# instead of creating shapes from scratch each time, we just clone them

class Shape:
    def __init__(self, color):
        self.color = color

    def clone(self):
        return copy.deepcopy(self)

    def draw(self):
        raise NotImplementedError("subclass must implement draw()")


class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def draw(self):
        print(f"  Circle   -> color: {self.color}, radius: {self.radius}")


class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height

    def draw(self):
        print(f"  Rectangle -> color: {self.color}, width: {self.width}, height: {self.height}")


class Triangle(Shape):
    def __init__(self, color, base, height):
        super().__init__(color)
        self.base = base
        self.height = height

    def draw(self):
        print(f"  Triangle  -> color: {self.color}, base: {self.base}, height: {self.height}")


# Factory - ShapeFactory
# cleaner way to create shapes without hardcoding the class names everywhere

class ShapeFactory:
    @staticmethod
    def create(kind, **props):
        kind = kind.lower()
        if kind == "circle":
            return Circle(props.get("color", "black"), props.get("radius", 1))
        elif kind == "rectangle":
            return Rectangle(props.get("color", "black"), props.get("width", 1), props.get("height", 1))
        elif kind == "triangle":
            return Triangle(props.get("color", "black"), props.get("base", 1), props.get("height", 1))
        else:
            raise ValueError(f"don't know how to make a '{kind}'")


if __name__ == "__main__":

    # test singleton
    c1 = Canvas()
    c2 = Canvas()
    print(f"same canvas? -> {c1 is c2}")

    print()

    # create shapes using the factory
    s1 = ShapeFactory.create("circle", color="red", radius=5)
    s2 = ShapeFactory.create("rectangle", color="blue", width=8, height=4)
    s3 = ShapeFactory.create("triangle", color="green", base=6, height=3)

    # clone s1 and change the color (prototype pattern)
    s4 = s1.clone()
    s4.color = "yellow"

    # add everything to the canvas
    for s in [s1, s2, s3, s4]:
        c1.add(s)

    c1.show()

    # adding through c2 should still show on c1 (singleton proof)
    c2.add(ShapeFactory.create("circle", color="purple", radius=2))
    print("added via c2, showing via c1:")
    c1.show()
