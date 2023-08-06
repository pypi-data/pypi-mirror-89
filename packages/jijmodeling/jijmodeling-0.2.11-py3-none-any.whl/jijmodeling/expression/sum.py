
from typing import Any, List, Tuple
from jijmodeling.expression.from_serializable import from_serializable
from jijmodeling.expression.expression import Add, Expression, _latex_repr


def Sum(indices: dict, term: Expression, condition=None):
    """[summary]

    Args:
        indices (dict): [description]
        term ([type]): [description]
        condition ([type], optional): [description]. Defaults to None.

    Example:
        Create :math:`\sum_{i=0}^n d_i x_i`

        >>> from jijmodeling import PlaceholderArray, BinaryArray, Sum
        >>> d = PlaceholderArray('d', dim=1)
        >>> n = d.shape[0]
        >>> x = BinaryArray('x', shape=n)
        >>> Sum({'i': n}, d['i']*x['i'])
        Σ_{i}(d[i]x[i])
    """
    sum_ind_list = [[k, v] for k, v in indices.items()]
    return SumOperator([term, sum_ind_list], condition=condition)

class SumOperator(Expression):
    """Class that represents the sum.

    Args:
        indices (dict): subscript to take the sum.
        term (:class:`Expression`): term to be summed.

    Attributes:
        indices (dict): subscript to take the sum.
        index_set (list): set of indices.
        condition (:class:`Condition`): conditions of summation.

    Example:
        Create :math:`\sum_{i=0}^n d_i x_i`

        >>> from jijmodeling import PlaceholderArray, BinaryArray, Sum
        >>> d = PlaceholderArray('d', dim=1)
        >>> n = d.shape[0]
        >>> x = BinaryArray('x', shape=n)
        >>> Sum({'i': n}, d['i']*x['i'])
        Σ_{i}(d[i]x[i])

    """
    def __init__(self, children: List[Any], condition=None) -> None:
        super().__init__(children=children)
        
        self.indices = {k: v for k, v in children[1]}

        from jijmodeling.variables.element import Element
        def extract_index(ind):
            if isinstance(ind, str):
                return ind.split(' ')[0]
            elif isinstance(ind, Element):
                return ind.label
            return ind
        self.index_keys = [extract_index(ind) for ind in self.indices.keys()]

        self.condition = condition


    @property
    def index_set(self):
        index_set = self.children.index_set
        return [ind for ind in index_set if ind.label not in self.index_keys]

    def __repr__(self):
        repr_str = 'Σ_{'
        for i in self.indices.keys():
            repr_str += str(i) + ', '
        term = self.children[0]
        repr_str = repr_str[:-2] + '}}({})'.format(term.__repr__()) 
        return repr_str

    def __make_latex__(self):
        ind_str = ""
        ind_end = ""
        for ind, ind_set in self.indices.items():
            ind_latex = _latex_repr(ind)
            ind_conds = []
            if len(ind_latex.split(' ')) == 3:
                ind_conds = ind_latex.split(' ')[1:]
                ind_latex = ind_latex.split(' ')[0]
            from jijmodeling.variables.array import Array
            if isinstance(ind_set, Array):
                ind_str += "{} \in {}, ".format(ind_latex, _latex_repr(ind_set))
            elif isinstance(ind_set, tuple):
                iset0 = _latex_repr(ind_set[0])
                ind_end += _latex_repr(ind_set[1]) + '- 1' + ", "
                ind_str += "{} = {}".format(ind_latex, iset0) + ", "
            else:
                ind_end += _latex_repr(ind_set) + '- 1' + ", "
                ind_str += "{} = 0".format(ind_latex) + ", "

            if len(ind_conds) > 0:
                cond_latex = {'!=': '\\neq', '==': '=', '<=': '\leq', '>=': '\geq', '<': '<', '>': '>'}
                ind_str = ind_str[:-2]
                ind_str += '({} {} {}), '.format(ind_latex, cond_latex[ind_conds[0]], ind_conds[1])

        if isinstance(self.children[0], Add):
            term = _latex_repr(self.children[0])
        else:
            term = _latex_repr(self.children[0], False)

        return  "\sum_{{{}}}^{{{}}} {}".format(ind_str[:-2], ind_end[:-2], term)
        

    # @classmethod
    # def from_serializable(cls, serializable: dict):
    #     indices:dict = from_serializable(serializable['attributes']['indices'])
    #     term = from_serializable(serializable['attributes']['children'])[0]
    #     return cls(indices, term)