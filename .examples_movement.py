class Robot:
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        """Move robot by dx, dy and return new position."""
        self.x += dx
        self.y += dy
        return (self.x, self.y)

if __name__ == '__main__':
    r = Robot('demo')
    print(r.move(1,2))
