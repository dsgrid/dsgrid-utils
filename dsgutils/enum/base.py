import copy
import logging
import os

import numpy as np
import pandas as pd

from dsgutils import DSGridValueError, DSGridRuntimeError
from dsgutils.enum import ENCODING, get_str

logger = logging.getLogger(__name__)

class Enumeration(object):
    """
    dsgrid uses enumerated dimensions to define and operate on datasets. Methods
    are provided to enable working in multiple data formats including csv, HDF, 
    and parquet. Each value in the enumeration has an id and a name. For 
    compatibility reasons, these are restricted to be strings of no more than 64
    and 128 characters each, respectively.

    Class Attributes
    ----------------
    DIMENSION_NAME : str or None
        derived classes typically define a dimension name such as 'sector', 
        'geography', 'enduse', or 'time'
    MAX_ID_LEN : int
        maximum length of id strs
    MAX_NAME_LEN : int
        maximum length of name strs
    DTYPE : np.dtype
        specifies the data type for (id, name) value pairs

    Attributes
    ----------
    ids : iterable of str
        list or other iterable of strs that are the ids defined by this 
        Enumeration. ids are used directly to label datasets and must be unique.
    names : iterable of str
        list or other iterable of strs that maps one-to-one to ids, that is, 
        list(ids)[i] and list(names)[i] are expected to be short and long 
        (respectively) labels for the same point along the dimension defined by 
        this Enumeration. names are for display purposes only, that is, they 
        are stored as dataset meta-data, but are not used within data tables.
    """

    DIMENSION_NAME = None

    MAX_ID_LEN = 64
    MAX_NAME_LEN = 128
    DTYPE = np.dtype([
        ("id", "S" + str(MAX_ID_LEN)),
        ("name", "S" + str(MAX_NAME_LEN))
    ])

    def __init__(self, name, ids, names = None):
        self._name = name
        self._ids = ids
        self._names = names if names is not None else copy.deepcopy(ids)

        self._checkvalues()
        return

    @property
    def name(self):
        return self._name

    @property
    def ids(self):
        return copy.deepcopy(self._ids)

    @property
    def names(self):
        return copy.deepcopy(self._names)

    def _checkvalues(self):

        ids = list(self.ids); names = list(self.names)
        n_ids = len(ids); n_names = len(names)

        if n_ids != n_names:
            raise DSGridValueError("Number of ids (" + str(n_ids) +
                ") must match number of names (" + str(n_names) + ")")

        if len(set(ids)) != n_ids:
            raise DSGridValueError("Enumeration ids must be unique")

        if max(len(value) for value in ids) > self.MAX_ID_LEN:
            raise DSGridValueError("Enumeration ids cannot exceed " +
                "{} characters".format(self.MAX_ID_LEN))

        if max(len(value) for value in names) > self.MAX_NAME_LEN:
            raise DSGridValueError("Enumeration names cannot exceed " +
                             "{} characters".format(self.MAX_NAME_LEN))

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.__dict__ == other.__dict__
        )

    def __len__(self):
        return len(list(self.ids))

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return self.__repr__()

    def get_name(self,id):
        ind = list(self.ids).index(id)
        return self.names[ind]

    def create_subset_enum(self,ids):
        """
        Returns a new enumeration that is a subset of this one, based on keeping 
        the items in ids.

        Parameters
        ----------
        ids : list
            subset of self.ids that should be kept in the new enumeration

        Returns
        -------
        self.__class__
        """
        _ids, _names = self._get_subset_ids_names(ids)
        return self.__class__(self.name + ' Subset',_ids,_names)

    def _get_subset_ids_names(self,ids):
        n = len(ids)
        _ids = [None] * n; _names = [None] * n
        for i, full_id in enumerate(self.ids):
            if full_id in ids:
                j = ids.index(full_id)
                logger.debug("Found info for {}, which is entry {} of {}".format(full_id,j,len(_ids)))
                _ids[j] = self.ids[i]
                _names[j] = self.names[i]
        if len([x for x in _ids if x is None]):
            raise DSGridRuntimeError("At least one of {} is not in {}".format(ids,self.ids))
        return _ids, _names

    def is_subset(self,other_enum):
        """
        Returns true if this Enumeration is a subset of other_enum.
        """
        if not isinstance(other_enum,self.__class__):
            return False
        for my_id in self.ids:
            if not (my_id in other_enum.ids):
                return False
        return True

    def persist(self, h5group):

        dset = h5group.create_dataset(
            self.DIMENSION_NAME,
            dtype=self.DTYPE,
            shape=(len(self),))

        dset.attrs["name"] = self.name

        dset["id"] = np.array(self.ids)
        dset["name"] = np.array([name.encode(ENCODING) for name in self.names])

        return dset

    @classmethod
    def load(cls, h5group):
        h5dset = h5group[cls.DIMENSION_NAME]
        return cls(
            get_str(h5dset.attrs["name"]),
            [get_str(vid) for vid in h5dset["id"]],
            [get_str(vname) for vname in h5dset["name"]]
        )

    @classmethod
    def read_csv(cls, filepath, name=None):
        enum = pd.read_csv(filepath, dtype=str)
        name = cls._name_from_filepath(filepath) if name is None else name
        return cls(name, list(enum.id), list(enum.name))

    def to_csv(self, filedir=None, filepath=None, overwrite=False):
        p = self._default_filepath()
        if filepath is not None:
            p = filepath
        elif filedir is not None:
            p = os.path.join(filedir,self._default_filename())
        if not overwrite and os.path.exists(p):
            msg = "{} already exists".format(p)
            logger.error(msg)
            raise DSGridRuntimeError(msg)
        df = pd.DataFrame(list(zip(self.ids,self.names)),columns=['id','name'])
        df.to_csv(p,index=False)

    @classmethod
    def _name_from_filepath(cls,filepath):
        return os.path.splitext(os.path.basename(filepath))[0].replace("_"," ").title()

    def _default_filepath(self):
        return os.path.join(enumdata_folder,self._default_filename())

    def _default_filename(self):
        return self.name.lower().replace(' ','_') + '.csv'


# TODO: Move this to a config file
enumdata_folder = os.path.join(os.path.dirname(__file__), "enumeration_data/")
