class Composite:
    pass

class Object(Composite):
    pass

class Action(Composite):
    pass

class Comparable(Composite):
    pass

class Environment(Object):
    pass

class Link(Composite):
    pass

class Treat(Composite):
    pass

class MoreLink(Link):
    property

class LessLink(Link):
    property

class EqualLink(Link):
    property

class TreatLink(Link):
    pass

class ReasonLink(Link):
    pass

class GeneralizationLink(Link):
    pass

class Selector(Composite):
    pass


class AI:
    def Live(self):
        print("To live and die...")

ai = AI()
ai.Live()



