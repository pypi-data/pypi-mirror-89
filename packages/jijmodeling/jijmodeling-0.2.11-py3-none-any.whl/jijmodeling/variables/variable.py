from jijmodeling.expression.expression import Expression

class Variable(Expression):
    def __init__(self, label: str, children:list=[]):
        self.label = label
        super().__init__(children=children)

    def _rdiv_validate(self, other):
        pass

    def __rtruediv__(self, other):
        self._rdiv_validate(other)
        return super().__rtruediv__(other)

    def __repr__(self):
        return self.label

    def __hash__(self) -> int:
        class_name = self.__class__.__name__
        return hash(self.label + class_name)


class Binary(Variable):
    def _rdiv_validate(self, other):
        """This method is called before the calculation when the div method is called.
        Raises:
            ZeroDivisionError: cannot perform division with binary.
        """
        # other / self <- {0,1}
        raise ZeroDivisionError("'Binary' can take zero")

class Placeholder(Variable):
    def __init__(self, label: str):
        super().__init__(label)


class LogEncInteger(Variable):
    """Log encoded interger

    .. math::
        x = \\frac{\\text{upper}-\\text{lower}}{2^l} \sum_{l=0}^{\\text{bits}-1} 2^l s_l + \\text{lower},~(s_l \in \{0, 1\}~ \\forall l)

    .. math::
        \\text{lower} \leq x \leq \\text{upper}
    """
    def __init__(self, label: str, lower, upper):
        super().__init__(label, [lower, upper])

    @property
    def lower(self):
        return self.children[0]

    @property
    def upper(self):
        return self.children[1]

    def _rdiv_validate(self, other):
        # other / self <- {0,1}
        if self.lower <= 0 and self.upper >= 0:
            raise ZeroDivisionError("'Binary' can take zero")
        else:
            super()._rdiv_validate(other)


class DisNum(Variable):
    """Discreated number class
    
    .. math::
        x = \\frac{\\text{upper}-\\text{lower}}{2^{\\text{bits}}-1} \sum_{l=0}^{\\text{bits}-1} 2^l s_l + \\text{lower},~
        (s_l \in \{0, 1\}~ \\forall l)
    .. math::
        \\text{lower} \leq x \leq \\text{upper}
    """
    def __init__(self, label: str, lower: float=0.0, upper: float=1.0, bits: int=3):
        super().__init__(label, [lower, upper, bits])
    
    @property
    def lower(self):
        return self.children[0]

    @property
    def upper(self):
        return self.children[1]

    @property
    def bits(self):
        return self.children[2]

        
