    def add_insect(self, insect):
        """Add an Insect to this Place.

        There can be at most one Ant in a Place, unless exactly one of them is
        a BodyguardAnt (Phase 2), in which case there can be two. If add_insect
        tries to add more Ants than is allowed, an assertion error is raised.

        There can be any number of Bees in a Place.
        """
        if not insect.is_ant():
            self.bees.append(insect)
#        if insect.is_ant():
        else:
            # Phase 2: Special handling for BodyguardAnt
            if self.ant != None and self.ant.can_contain(insect):
                insect.place = self
                self.ant.contain_ant(insect)
            if self.ant != None and insect.can_contain(self.ant) == True:
                insect.place = self
                insect.contain_ant(self.ant)
            else:
                assert self.ant is None, 'Two ants in {0}'.format(self)
                self.ant = insect
#        else:
#            self.bees.append(insect)