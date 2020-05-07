from abc import ABC

from typing import List, Dict, Tuple
import numpy as np


class FieldRepresentation(ABC):
    """
    Abstract class that generalize the concept of "field representation".
    A field representation is a semantic way to represent a field of an item.
    """

    def __init__(self, name: str):
        self.__name = name

    def get_name(self):
        return self.__name


class FeaturesBagField(FieldRepresentation):
    """
    Class for represent a baf of feature.
    This class can represent a bag of word if the key value of the dict "features" is a keyword
    instead of a url for represent a bag of feature.

    Args:
        features (dict): <str, object> the dictionary where feature are indexed
    """

    def __init__(self, name: str, features: Dict[str, object] = None):
        super().__init__(name)
        if features is None:
            features = {}
        self.__features: Dict[str, object] = features

    def add_feature(self, feature_key: str, feature_value):
        """
        Add a feature (feature_key, feature_value) to the dict

        Args:
            feature_key (str): key, can be a url or a keyword
            feature_value: the value of the field

        """
        self.__features[feature_key] = feature_value

    def get_feature(self, feature_key):
        """
        Get the feature_value from the dict[feature_key]

        Args:
            feature_key (str): key, can be a url or a keyword

        Returns:
            feature_value: the value of the field
        """
        return self.__features[feature_key]

    def get_feature_dict(self):
        """
        Get the features dict

        Returns:
            features: the features dict
        """
        return self.__features


class EmbeddingField(FieldRepresentation):
    """
    Class for represent a embedding.
    A embedding is a dense numeric vector.
    The shape of the array can be set for a n dimensional array, with n > 1

    Examples:
        shape (4) = [x,x,x,x]
        shape (2,2) = [[x,x],
                       [x,x]]

    Args:
        embedding_array:
    """
    
    def __init__(self, name: str, embedding_array: np.ndarray):
        super().__init__(name)
        self.__embedding_array = embedding_array


class GraphField(FieldRepresentation):
    """
    Class for represent a graph-field.
    """

    def __init__(self, name):
        super().__init__(name)


class ContentField:
    """
    A field of an item can be represented in different ways, indexed in representation_list.
    Args:
        field_name (str): the name of the field
        representations_list (list<FieldContent>): the list of the representations.
    """

    def __init__(self, field_name: str, representations_list: List[FieldRepresentation] = None):
        if representations_list is None:
            representations_list = []
        self.__field_name: str = field_name
        self.__representations_list: List[FieldRepresentation] = representations_list

    def __eq__(self, other):
        """
        override of the method __eq__ of object.

        Args:
            other (ContentField): another field

        Returns:
            True if the names are the same
        """
        return self.__field_name == other.__field_name

    def append(self, representation: FieldRepresentation):
        """
        Append a new representation to the representation_list

        Args:
            representation (FieldRepresentation): a representation
        """
        self.__representations_list.append(representation)

    def get_name(self):
        return self.__field_name
