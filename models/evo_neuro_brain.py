class NEBrain:
    def __init__(self, nn):
        self.nn = nn
        self.pawn = None

    def set_pawn(self, pawn):
        self.pawn = pawn

    def on_tick(self, delta_time):
        if self.pawn.env.__frame_count__ % 15 != 0:
            return

        self.look()
        self.think()
        self.act()

    def look(self):
        """
        Grabs all sensory data.

        Features:
            Pawn X
            Pawn Y
            Pawn VelX
            Pawn VelY
            Pawn Shields
            Pawn Shield Active
            Pawn Dir
            Pawn Health

            Enemy X
            Enemy Y
            Enemy VelX
            Enemy VelY
            Enemy Shields
            Enemy Shield Active
            Enemy Dir
            Enemy Health

            Closest Laser X
            Closest Laser Y
            Closest Laser Dir
        """

        p = self.pawn
        e = p.env.get_closest_enemy(p)
        l = p.env.get_closest_enemy_laser(p)

        self.data = [
            # Self Data
            p.pos[0],
            p.pos[1],
            p.vel[0],
            p.vel[1],
            p.shield_count,
            1 if p.__shield_on__ else 0,  # Convert to boolean
            p.dir,
            p.health,

            # Enemy Data
            - 1 if e == None else e.pos[0],
            -1 if e == None else e.pos[1],
            -1 if e == None else e.vel[0],
            -1 if e == None else e.vel[1],
            -1 if e == None else e.shield_count,
            -1 if e == None else 1 if e.__shield_on__ else 0,  # Convert to boolean
            -1 if e == None else e.dir,
            -1 if e == None else e.health,

            -1 if l == None else l.pos[0],
            -1 if l == None else l.pos[1],
            -1 if l == None else l.dir
        ]

        # print("Data: ")
        # print(self.data)

    def think(self):
        """
        Calculates the neural net output.
        """

        self.output = self.nn.output(self.data)

        # print("Output: ")
        # print(self.output)

    def act(self):
        """
        According to the net's outputs, react accordingly.

        Actions:
            [0]: Move LEFT
            [1]: Move UP
            [2]: Move RIGHT
            [3]: Move DOWN

            [4]: Fire Short Laser
            [5]: Fire Long Laser
            [6]: Use Shield

            [7]: Look Right
            [8]: Look Left
        """

        o = self.output
        p = self.pawn

        if o[0] > 0.8:
            # LEFT
            p.move(-1, None)

        if o[1] > 0.8:
            # UP
            p.move(None, 1)

        if o[2] > 0.8:
            # RIGHT
            p.move(1, None)

        if o[3] > 0.8:
            # DOWN
            p.move(None, -1)

        if o[4] > 0.8:
            # Long
            p.attack("long")
        elif o[5] > 0.8:
            # Short
            p.attack("short")

        if o[6] > 0.8:
            # Shield
            p.use_shield()

        if o[7] > 0.8:
            # Look RIGHT
            p.look("right")
        elif o[8] > 0.8:
            # Look LEFT
            p.look("left")
        else:
            p.look(None)
