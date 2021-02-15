class Disk:

    def __init__(self, x, y, color, diameter, y_to_stop, y_vel=0):
        self.x = x
        self.y_vel = y_vel
        self.y = y
        self.color = color
        self.dia = diameter
        self.landed = 0
        self.y_to_stop = y_to_stop

    def draw_disk(self):
        """Draw the disk on the screen"""
        fill(*self.color)
        noStroke()
        ellipse(self.x, self.y + self.y_vel, self.dia, self.dia)
