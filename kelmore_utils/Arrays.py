from typing import List, TypeVar, Any, Union, Optional, Iterable

from .types.UtilsTypes import Point, UniqueResp

GenT = TypeVar('GenT')


class Arrays:

    @staticmethod
    def append_missing(source: List[Any], dest: List[Any]) -> List[Any]:
        for item in source:
            if item not in dest:
                dest.append(item)
        return dest

    @staticmethod
    def complement(_set: Iterable[Any], subset: Iterable[Any], unique: bool = False) -> UniqueResp:
        output: UniqueResp = set() if unique else []
        for item in _set:
            if item not in subset:
                if unique:
                    output.add(item)
                else:
                    output.append(item)
        return output

    @staticmethod
    def force_equal(list_a: List[Any], list_b: List[Any]):
        while len(list_a) > len(list_b):
            list_a.pop()

        while len(list_b) > len(list_a):
            list_b.pop()

    @staticmethod
    def equal_length(list_a: List[Any], list_b: List[Any],
                     raise_error: Optional[bool] = False) -> bool:
        if len(list_a) == len(list_b):
            return True
        if raise_error:
            raise ValueError('The passed arrays were not of equal length')
        return False

    @staticmethod
    def first(array: Union[List[GenT], GenT]) -> Union[GenT, None]:
        if isinstance(array, list):
            if not array:
                return None
            return array[0]
        return array

    @staticmethod
    def iter_all_in(search: Iterable[str], dest: Iterable[str]) -> bool:
        for item in search:
            if item not in dest:
                return False
        return True

    @staticmethod
    def remove_null(array: List[GenT]) -> List[GenT]:
        array = [] if array is None else array
        return [x for x in array if x is not None]

    @staticmethod
    def unique(array: List[GenT]) -> List[GenT]:
        return [] if array is None else list(set(array))

    @staticmethod
    def remove_none_inner(array: List[GenT]) -> List[GenT]:
        remove_indexes: List[int] = []
        for idx, item in enumerate(array):
            if item is None:
                remove_indexes.append(idx)
        return Arrays.remove_indexes(array, remove_indexes)

    @staticmethod
    def remove_none(array: List[GenT]) -> List[GenT]:
        return [x for x in array if x is not None]

    @staticmethod
    def listify(item: Any):
        if item is None:
            return []
        if not isinstance(item, list) and not isinstance(item, set):
            return [item]

        return item

    @staticmethod
    def delistify(item: Any, force_first: bool = False):
        if isinstance(item, list):
            if not item:
                return None
            if len(item) == 1:
                return item[0]
            if force_first:
                return item[0]
            return item
        return item

    @staticmethod
    def remove_indexes(array: List[GenT], remove_idxs: List[int]) -> List[GenT]:
        remove_idxs.sort()
        count: int = 0
        for idx in remove_idxs:
            del array[idx - count]
            count += 1

        return array

    @staticmethod
    def reverse(string: str):
        """ prec: s is a list
            postc: returns the reversed list s"""
        return string[::-1]

    @staticmethod
    def merge_lists_remove_duplicates(list1, list2):
        """ prec: both list1 and list2 are valid lists
            postc: merges list2 into list1 while removing any duplicate values"""
        for item in list2:
            if item not in list1:
                list1.append(item)

    @staticmethod
    def get_index_in_list(_list, query):
        """ prec: _list is a list, query is a string
            postc: returns the index of the query in the list, or -1 if it is not found"""

        try:
            return _list.index(query)
        except ValueError:
            return -1

    @staticmethod
    def get_index_in_list_insensitive(_list, query):
        """ prec: _list is a list, query is a string
            postc: returns the index of the query in the list, or -1 if it is not found.
                    Ignores case"""
        temp_list = [str(x).lower() for x in list(_list)]
        return Arrays.get_index_in_list(temp_list, query.lower())

    @staticmethod
    def swap(_list, index1, index2):
        """ prec: _list is a list, index1 and index2 are numbers less than length of _list
            postc: swaps the two indexes in the _list"""
        temp = _list[index1]
        _list[index1] = _list[index2]
        _list[index2] = temp

    @staticmethod
    def chunk(array: List[Any], chunk_size: int) -> List[List[Any]]:
        output: List[List[Any]] = []
        idx = 0
        while idx < len(array):
            new_array: List[Any] = []
            while idx < len(array) and len(new_array) < chunk_size:
                new_array.append(array[idx])
                idx += 1
            output.append(new_array)

        return output

    @staticmethod
    def remove_items(array: List[Any], removal: List[Any]) -> List[Any]:
        for remove in removal:
            if remove in array:
                array.remove(remove)
        return array

    @staticmethod
    def all_not_null(*params: Any):
        all_not_none: bool = True
        for item in params:
            all_not_none = all_not_none and item is not None
            if not all_not_none:
                break
        return all_not_none

    @staticmethod
    def check_any_none(*params: Any) -> bool:
        """
        Checks an array and returns True if any of the values are none, else returns False
        :return: True if array contains a None value, False otherwise
        """
        for item in params:
            if item is None or item == '':
                return True
        return False

    @staticmethod
    def check_all_none(*params: Any) -> bool:
        # Checks an array and returns True if all the items are None
        all_none: bool = True
        for item in params:
            all_none = all_none and item is None
        return all_none

    @staticmethod
    def get_matrix_point(array: List[List[Any]], point: Point) -> Any:
        # TODO: Maybe make 2D class??
        # TODO: Swap x, y
        """
        Gets the value from a 2D array using the given point
        :param array: The lookup array
        :param point: The point of the value - defined as (y, x) or (row, col)
        :return: The value
        """
        pos_y = point[0]
        pos_x = point[1]

        datum = None
        if pos_y < len(array):
            row = array[pos_y]
            if pos_x < len(row):
                datum = row[pos_x]

        return datum

    @staticmethod
    def get_matrix_col(array: List[List[Any]], col: int) -> List[Any]:
        # TODO: Test
        output: List[Any] = []
        for row in array:
            if len(row) > col:
                output.append(row[col])
        return output

    @staticmethod
    def transform_matrix_to_json(array: List[List[Any]],
                                 headers: Optional[List[str]] = None) -> List[dict]:
        output: List[dict] = []
        if not array:
            return output

        headers = array.pop(0) if headers is None else headers
        headers = [str(x) for x in headers]
        for row in array:
            new_json: dict = {}
            for header_idx, header in enumerate(headers):
                if header_idx < len(row):
                    new_json[header] = row[header_idx]
            output.append(new_json)
        return output
