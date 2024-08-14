import json
from pprint import pprint

# The environment files to compare. You can set these to "dev", "staging", or "prod".
FILE1 = "staging"
FILE2 = "dev"
SORT_KEY_ORDER = ["brand_name", "brand", "segment", "year"]

class PayloadComparer:
    """
    Class for comparing JSON payloads between different environments.
    """

    def __init__(self):
        self.messages = []

    def load_json_to_dict(self, filename):
        """
        Loads the JSON data from a file and converts it to a Python dictionary.

        Args:
            filename (str): The name of the file to load.

        Returns:
            dict: The loaded JSON data as a dictionary.
        """
        with open(filename, 'r') as file:
            return json.load(file)

    def sort_dicts_by_key_value(self, dict_list):
        """
        Sorts a list of dictionaries based on the values of specified keys.

        Args:
            dict_list (list): A list of dictionaries to sort.

        Returns:
            list: A sorted list of dictionaries.
        """
        def sort_key_func(dictionary):
            # Create a tuple with values of the specified keys in SORT_KEY_ORDER
            key_values = tuple(dictionary.get(key) for key in SORT_KEY_ORDER)
            # If all keys in key_values are None (missing), sort by the dictionary keys alphabetically
            if all(value is None for value in key_values):
                return tuple(sorted(dictionary.items()))
            return key_values
        
        return sorted(dict_list, key=sort_key_func)

    def compare_lists(self, list1, list2):
        """
        Compares two lists and accumulates the differences.

        Args:
            list1 (list): The first list to compare.
            list2 (list): The second list to compare.
        """
        set1 = set(item if isinstance(item, str) else str(item) for item in list1)
        set2 = set(item if isinstance(item, str) else str(item) for item in list2)
        self.set_comparetor(set1, set2)

    
    def set_comparetor(self, set1, set2):
        if set1 != set2:
            unique_to_list1 = set1 - set2
            unique_to_list2 = set2 - set1

            if unique_to_list1 or unique_to_list2:
                max_len = max(len(unique_to_list1), len(unique_to_list2))
                
                for index in range(max_len):
                    item1 = list(unique_to_list1)[index] if index < len(unique_to_list1) else "None"
                    item2 = list(unique_to_list2)[index] if index < len(unique_to_list2) else "None"
            
                    if isinstance(item1, (dict, list)):
                        item1 = json.dumps(item1, indent=4)
                    if isinstance(item2, (dict, list)):
                        item2 = json.dumps(item2, indent=4)

                    primary_message = f"\n\nMismatch at index {index} and key '{self.process_key}':"
                    self.messages.append(primary_message)
                    self.messages.append("-"*len(primary_message))
                    self.messages.append(f"\t*{FILE1} value: {item1}")
                    self.messages.append(f"\t*{FILE2} value: {item2}")

    def handle_dict(self, dict1, dict2):
        """
        Compares two dictionaries and processes the differences.

        Args:
            dict1 (dict): The first dictionary to compare.
            dict2 (dict): The second dictionary to compare.
        """
        for key, value in dict1.items():
            value2 = dict2.get(key)
            self.handle_format(key, value, value2)

    def handle_array(self, key, list1, list2):
        """
        Handles the comparison of two lists (arrays) of items.

        Args:
            key (str): The key associated with the list.
            list1 (list): The first list to compare.
            list2 (list): The second list to compare.
        """
        try:
            self.compare_lists(list1, list2)
            sorted_list1 = self.sort_dicts_by_key_value(list1)
            sorted_list2 = self.sort_dicts_by_key_value(list2)
            for index, item1 in enumerate(sorted_list1):
                item2 = sorted_list2[index]
                self.handle_format(key, item1, item2)
        except:
            pass

    def handle_single_key(self, key, value1, value2):
        """
        Handles the comparison of single key-value pairs.

        Args:
            key (str): The key being compared.
            value1: The value from the first JSON.
            value2: The value from the second JSON.
        """
        if value1 != value2:
            primary_message = f"\n\nKey '{key}' mismatch:"
            self.messages.append(primary_message)
            self.messages.append("-"*len(primary_message))
            self.messages.append(f"\t{FILE1} value: {json.dumps(value1, indent=4)}")
            self.messages.append(f"\t{FILE2} value: {json.dumps(value2, indent=4)}")

    def handle_format(self, key, value1, value2):
        """
        Determines the type of the value (dict, list, or single value) 
        and calls the appropriate handler.

        Args:
            key (str): The key being compared.
            value1: The value from the first JSON.
            value2: The value from the second JSON.
        """
        if isinstance(value1, dict):
            self.handle_dict(value1, value2)
        elif isinstance(value1, list):
            self.handle_array(key, value1, value2)
        else:
            self.handle_single_key(key, value1, value2)

    def process_comparison(self):
        """
        Loads and compares two JSON payloads, handling mismatches and differences.
        """
        json_data_1 = self.load_json_to_dict(f"{FILE1}_payload.json")
        json_data_2 = self.load_json_to_dict(f"{FILE2}_payload.json")
        
        # self.set_comparetor(set(json_data_1.keys()), set(json_data_2.keys()))
        
        for key, value1 in json_data_1.items():
            self.process_key = f"{key} "
            value2 = json_data_2.get(key, "not_found")
            if value2 != "not_found":
                self.handle_format(key, value1, value2)
            else:
                primary_message = f"\n\nKey '{key}' is missing in '{FILE2}':"
                self.messages.append(primary_message)
                self.messages.append("-"*len(primary_message))
                self.messages.append(f"  Present in '{FILE1}' with value: {value1}")

    def print_messages(self):
        """
        Prints all accumulated messages in order with headings underlined.
        """
        print("\n" + "="*30 + " Unmatched Items " + "="*30)
        for message in self.messages:
            print(message)

if __name__ == '__main__':
    comparer = PayloadComparer()
    comparer.process_comparison()
    comparer.print_messages()
