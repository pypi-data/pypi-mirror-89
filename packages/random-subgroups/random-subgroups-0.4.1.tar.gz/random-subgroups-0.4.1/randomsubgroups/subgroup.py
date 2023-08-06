import numpy as np
from pysubgroup import ps
from pysubgroup.subgroup_description import Conjunction


def encode_subgroup(decoded_subgroup):

    conjunction = []
    for attribute_name, cond in decoded_subgroup['conditions'].items():

        selector_type = cond['selector_type']
        if selector_type == 'IntervalSelector':
            conjunction.append(ps.subgroup_description.IntervalSelector(attribute_name,
                                                                        lower_bound=cond['lower_bound'],
                                                                        upper_bound=cond['upper_bound']))
        elif selector_type == 'EqualitySelector':
            for att_value in cond['attribute_value']:
                conjunction.append(ps.subgroup_description.EqualitySelector(attribute_name, att_value))
        else:
            msg = "Unknown pysubgroup Selector type"
            raise ValueError(msg)

    conjunction = ps.subgroup_description.Conjunction(conjunction)

    return tuple((decoded_subgroup['score'], conjunction))


class SubgroupPredictor(Conjunction):
    """
    Class for the Subgroup predictors.

    """
    def __init__(self,
                 subgroup,
                 target,
                 alternative_target=None,
                 predict_complement=False
                 ):
        Conjunction.__init__(self, subgroup[1].selectors)

        self.target = target
        self.alternative_target = alternative_target
        self.predict_complement = predict_complement
        self.score = subgroup[0]
        if predict_complement and alternative_target is None:
            msg = "Cannot predict complement if alternative target is not given"
            raise ValueError(msg)

    @classmethod
    def from_dict(cls, decoded_subgroup):
        subgroup = encode_subgroup(decoded_subgroup)
        target = decoded_subgroup['target']

        return cls(subgroup, target=target, alternative_target=decoded_subgroup['alternative_target'])

    def predict(self, x):
        """
        Predict class for x.

        The predicted class of an input sample is the associated target
        of the subgroup if the latter covers the input. Otherwise predicts
        the alternative target.

        Parameters
        ----------
        x : {array-like, sparse matrix} of shape (n_samples, n_features)
            The input samples. Internally, its dtype will be converted to
            ``dtype=np.float32``.

        Returns
        -------
        p : ndarray of shape (n_samples, n_classes)
            The class probabilities of the input samples. The order of the
            classes corresponds to that in the attribute :term:`classes_`.
        """
        # Check is fit had been called
        # check_is_fitted(self)

        predictions = np.array([None] * x.shape[0])
        covered_ids = self.covers(x)
        predictions[covered_ids] = self.target

        return predictions

    def to_dict(self):

        dict_subgroup = {'description': self.__str__(), 'conditions': {},
                         'score': self.score, 'target': self.target, 'alternative_target': self.alternative_target}

        for condition in self._selectors:

            attribute_name = condition._attribute_name
            already_exists = attribute_name in dict_subgroup['conditions'].keys()

            if issubclass(type(condition), ps.subgroup_description.IntervalSelector):
                if already_exists:
                    stored_condition = dict_subgroup['conditions'][attribute_name]
                    lower_bound = max([condition._lower_bound, stored_condition['lower_bound']])
                    upper_bound = min([condition._upper_bound, stored_condition['upper_bound']])
                else:
                    lower_bound = condition._lower_bound
                    upper_bound = condition._upper_bound

                dict_subgroup['conditions'].update({attribute_name: {'lower_bound': lower_bound,
                                                                     'upper_bound': upper_bound,
                                                                     'selector_type': 'IntervalSelector'}})

            elif issubclass(type(condition), ps.subgroup_description.EqualitySelector):
                attribute_value = condition._attribute_value
                if already_exists and dict_subgroup['conditions'][attribute_name]['selector_type'] == 'EqualitySelector':
                    if attribute_value not in dict_subgroup['conditions'][attribute_name]['attribute_value']:
                        dict_subgroup['conditions'][attribute_name]['attribute_value'].append(
                            attribute_value)
                else:
                    dict_subgroup['conditions'].update(
                        {attribute_name: {'attribute_value': [attribute_value],
                                          'selector_type': 'EqualitySelector'}})

        return dict_subgroup

    def get_features(self):

        attribute_list = []
        for condition in self._selectors:
            if condition._attribute_name not in attribute_list:
                attribute_list.append(condition._attribute_name)
        return attribute_list
