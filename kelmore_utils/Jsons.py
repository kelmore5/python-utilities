import json

from typing import Sequence, Union, Any, Dict, List, Set, Callable, Optional

Items = Union[None, Dict[str, Any]]


class DictObject:
    json: Items

    def __init__(self, json_item: Items):
        self.json = json_item

    def __str__(self):
        return str(self.json)

    def __repr__(self):
        return str(self.json)


class Jsons:
    # TODO: Should this carry the json object itself and default to operating on it???
    # TODO: Probably
    # TODO: Would need json list class too...
    keys_set: Set[str]

    @staticmethod
    def merge_all_children(json_item: dict, include_arrays: Optional[bool] = False):
        has_children: bool = Jsons.has_children(json_item, include_arrays=include_arrays)
        while has_children is True:
            json_item = Jsons.merge_children(json_item, include_arrays=include_arrays)
            has_children = Jsons.has_children(json_item)
        return json_item

    @staticmethod
    def merge_children(json_item: dict, include_arrays: Optional[bool] = False):
        keys: List[str] = list(json_item.keys())
        for key in keys:
            child: Any = json_item[key]
            if isinstance(child, dict):
                child: dict = json_item.pop(key)
                json_item = {**json_item, **child}
            elif include_arrays and isinstance(child, list):
                for datum_idx, children in enumerate(child):
                    child[datum_idx] = \
                        Jsons.merge_all_children(children, include_arrays=include_arrays)
        return json_item

    @staticmethod
    def has_children(json_item: dict, include_arrays: Optional[bool] = False) -> bool:
        if not isinstance(json_item, dict):
            return False

        keys: List[str] = list(json_item.keys())
        for key in keys:
            if isinstance(json_item[key], dict) or \
                    (include_arrays and isinstance(json_item[key], list)):
                return True
        return False

    @staticmethod
    def merge(json_a: dict, json_b: dict):
        return {**json_a, **json_b}

    @staticmethod
    def transform_matrix(fields: List[str], values: List[List[object]]) -> List[dict]:
        output: List[dict] = []
        for row in values:
            while len(row) < len(fields):
                row.append(None)
            while len(row) > len(fields):
                row.pop()

            output.append(Jsons.create_dict(fields, row))
        return output

    @staticmethod
    def create_dict(fields: Sequence[str], values: Sequence[object]) -> dict:
        if len(fields) != len(values):
            raise IndexError('Could not create the dictionary. '
                             'The length of fields and values did not match.')

        output = {}
        for idx, field in enumerate(fields):
            output[field] = values[idx]

        return output

    @staticmethod
    def get_item_index_in_json(json_list, search_key, search_tag):
        """ prec: json_list is a list of json objects, search_key is the key containing search_tag,
                    and search_tag is the tag being looked for
            postc: returns the index of the specific search term (search_tag)
                    being looked for in a list of json objects"""
        for json_idx, node in enumerate(json_list):
            node = json_list[json_idx]
            if search_key in node:
                if search_tag in node[search_key]:
                    return json_idx
        return -1

    @staticmethod
    def limit_json_data(json_list, search_key, target_items):
        """ prec: json_list is a list of json objects, search_key is the json tag being searched
                        for, and target_items is a list of items

            This function loops through a list of json objects and grabs the json tag (search_key)
                being targeted in each object. Once found, it will remove all items within
                said json tag list until only the target_items remain.
                AKA Loop through list > grab search_key in each item > remove items
                not in target_items

            postc: remove items not in target_items from each object in json_list"""
        for json_object in json_list:
            if search_key in json_object:
                search = json_object[search_key]
                to_remove = []

                if not isinstance(search, list):
                    search = [search]

                for item in search:
                    if item not in target_items:
                        to_remove.append(item)

                for item in to_remove:
                    search.remove(item)

    @staticmethod
    def get_empty_keys_specific(json_list, id_key, search_key):
        """ prec: json_list is a list of json objects, search_key is the json tag being searched
                    for, and id_key is id tag of the json objects

                This function loops through a list of json objects (json_list), grabs the node at
                search_key, and adds said objects' id_key to a list if the node at search_key is
                empty

            postc: A list of ids of all json objects in json_list with empty lists at search_key"""
        output_data = []
        # Merge the two files
        for json_object in json_list:
            if search_key in json_object:
                if not json_object[search_key]:
                    output_data.append(json_object[id_key])
            else:
                output_data.append(json_object[id_key])

        return output_data

    @staticmethod
    def json_intersection(json_list_1, json_list_2):
        """
        Takes two json dictionaries, finds the overlapping elements (aka elements that are in
        both json_list_1 and json_list_2), and then adds the overlapped element to a new
        json dictionary
        :param json_list_1: json dictionary
        :param json_list_2: json dictionary
        :return: The intersection between json_list_1 and json_list_2
        """
        json_cross = {}
        for item in json_list_1:
            if item in json_list_2:
                json_item_1 = json_list_1[item]
                json_item_2 = json_list_2[item]

                json_cross[item] = json_item_1.copy().update(json_item_2)

        return json_cross

    @staticmethod
    def json_intersection_by_fields(json_list_1, json_list_2, fields_1, fields_2):
        """
        Takes the intersection of json_list_1 and json_list_2, and updates them to
        only contain the necessary fields (fields_1 for json_list_1 and fields_2 for
        json_list_2)
        :param json_list_1: json dictionary
        :param json_list_2: json dictionary
        :param fields_1: the fields from json_list_1 to grab
        :param fields_2: the fields from json_list_2 to grab
        :return: The intersection of json_list_ 1 and json_list_2 with only fields_1
            and fields_2
        """
        json_cross = Jsons.json_intersection(json_list_1, json_list_2)
        new_json_cross = {}

        for key in json_cross:
            json_item = json_cross[key]
            new_json_item = {}

            for field in fields_1:
                new_json_item[field] = json_item[field]

            for field in fields_2:
                new_json_item[field] = json_item[field]

            new_json_cross[key] = new_json_item

        return new_json_cross

    @staticmethod
    def open_json_file(file_name):
        """ prec: file_name is a valid json file path
            postc: opens the json file and returns it as an object"""
        with open(file_name) as data_file:
            return json.load(data_file)

    @staticmethod
    def save_json_file(file_name, json_object):
        """ prec: file_name is a valid file path, json_objcet is a json object
                postc: saves the json_object to file_name"""
        with open(file_name, "w") as outfile:
            json.dump(json_object, outfile)

    @staticmethod
    def batch_remove_duplicates(json_list):
        """
        Removes all duplicate json dictionaries in a list of json dictionaries
        :param json_list: A list of json dictionaries
        :return: The json list
        """
        to_remove = []

        for json_idx in range(len(json_list) - 1):
            json_item = json_list[json_idx]

            for json_item_2 in enumerate(json_list):
                if Jsons.check_equivalence(json_item, json_item_2):
                    to_remove.append(json_item_2)

        for remove in to_remove:
            if remove in json_list:
                json_list.remove(remove)

        return json_list

    @staticmethod
    def check_equivalence(json_list_1, json_list_2):
        """
        Checks if two json items are equivalent
        :param json_list_1: A json dictionary
        :param json_list_2: A json dictionary
        :return: True if the two items are equivalent, False otherwise
        """
        for key in json_list_1:
            if key in json_list_2:
                if json_list_1[key] not in json_list_2[key]:
                    return False
            else:
                return False

        return True

    @staticmethod
    def replace_keys(json_list: Sequence[dict], keys_to_replace: Sequence[str],
                     replacement_keys: Sequence[str]) -> Sequence[dict]:
        if len(keys_to_replace) != len(replacement_keys):
            raise IndexError('Could not replace the json keys for the given list. '
                             'The length of the key arrays do not match.')

        for json_dict in json_list:
            for key_idx, key in enumerate(keys_to_replace):
                if key in json_dict:
                    replacement = replacement_keys[key_idx]
                    datum = json_dict[key]
                    del json_dict[key]
                    json_dict[replacement] = datum

        return json_list

    @staticmethod
    def replace_keys_callback(jsons: dict, replace_function: Callable[[str], str]) -> dict:
        keys: List[str] = list(jsons.keys())
        for key in keys:
            new_key: str = replace_function(key)
            datum: Any = jsons[key]
            del jsons[key]
            jsons[new_key] = datum
        return jsons

    @staticmethod
    def replace_keys_callback_list(json_list: Sequence[dict],
                                   replace_function: Callable[[str], str]) -> List[dict]:
        return [Jsons.replace_keys_callback(x, replace_function) for x in json_list]

    @staticmethod
    def reduce(jsons: dict, keys_to_keep: Sequence[str]):
        keys = [x for x in jsons.keys() if x not in keys_to_keep]
        for key in keys:
            if key in jsons:
                del jsons[key]

        return jsons

    @staticmethod
    def reduce_list(json_list: Sequence[dict], keys_to_keep: Sequence[str]) -> Sequence[dict]:
        """
        Removes all the keys except those in keys_to_keep from all the json items with json_list

        :param json_list: (Sequence[dict]) A list of dictionary objects
        :param keys_to_keep: (Sequence[str]) A list of keys to keep within each item in json_list
        :return: The json_list but reduced to only the specified keys from keys_to_keep
        """
        for item in json_list:
            Jsons.reduce(item, keys_to_keep)

        return json_list

    @staticmethod
    def remove_null_values(json_item: dict) -> dict:
        keys: List[str] = list(json_item.keys())
        for key in keys:
            if json_item.get(key) is None:
                del json_item[key]
        return json_item

    @staticmethod
    def get_all_keys_list(json_list: List[Dict[str, any]]) -> List[str]:
        all_keys: Set[str] = set()
        for json_item in json_list:
            all_keys = all_keys | set(json_item.keys())
        return list(all_keys)

    def get_all_keys(self, jsons: Dict[str, dict]) -> List[str]:
        self.keys_set = set()
        self.get_all_keys_helper(jsons)
        return list(self.keys_set)

    def get_all_keys_helper(self, jsons: Dict[str, dict]) -> None:
        keys: List[str] = jsons.keys()
        self.keys_set = self.keys_set.union(keys)
        for key in keys:
            node: dict = jsons[key]
            if node is not None:
                self.get_all_keys_helper(node)
