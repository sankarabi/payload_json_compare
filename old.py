import json

# The environment files to compare. You can set these to "dev", "staging", or "prod".
FILE1 = "staging"
FILE2 = "dev"

class PayloadComparison:
    def __init__(self):
        # Initialize an empty list to store unmatched items between the payloads.
        self.unmatched_items = []
        
        # These will hold the names of the files being compared.
        self.file1 = ""
        self.file2 = ""
        
    def load_json_to_dict(self, filename):
        """Loads the JSON data from a file and converts it to a Python dictionary."""
        with open(filename, 'r') as f:
            return json.load(f)

    def handle_dict(self, key, dict1, dict2):
        """Compares two dictionaries to find differences."""
        if isinstance(dict1, list):
            # If the value is a list, handle it with handle_array method.
            self.handle_array(key, dict1, dict2)
        elif isinstance(dict1, dict):
            try:
                # Identify keys present only in dict1 or only in dict2
                keys_only_in_dict1 = dict1.keys() - dict2.keys()
                keys_only_in_dict2 = dict2.keys() - dict1.keys()
                
                # Log keys only present in dict1.
                if keys_only_in_dict1:
                    self.unmatched_items.append(f"\nKeys only in {self.file1}:\n\t{', '.join(keys_only_in_dict1)}")
                
                # Log keys only present in dict2.
                if keys_only_in_dict2:
                    self.unmatched_items.append(f"\nKeys only in {self.file2}:\n\t{', '.join(keys_only_in_dict2)}")
            
                # Compare values for keys present in both dictionaries.
                for k in dict1.keys() & dict2.keys():
                    if isinstance(dict1[k], list) and isinstance(dict2[k], list):
                        # If both values are lists, handle with handle_array method.
                        self.handle_array(k, dict1[k], dict2[k])
                    elif dict1[k] != dict2[k]:
                        # Log any value differences for matching keys.
                        mismatch_message = (
                            f'\nKey "{k}" mismatch:\n'
                            f'\t{self.file1} value: {dict1[k]}\n'
                            f'\t{self.file2} value: {dict2[k]}'
                        )
                        self.unmatched_items.append(mismatch_message)
                    else:
                        # Recursively compare nested dictionaries.
                        self.handle_dict(key, dict1[k], dict2[k])
            except:pass
        else:
            # If the values for a key do not match, log the difference.
            if dict1 != dict2:
                mismatch_message = (
                    f'\nKey "{key}" mismatch:\n'
                    f'\t{self.file1} value: {dict1}\n'
                    f'\t{self.file2} value: {dict2}'
                )
                self.unmatched_items.append(mismatch_message)
                
    def handle_array(self, key, dict_list1, dict_list2):
        """Compares two lists of dictionaries."""
        try:
            # Sort each dictionary in the list by keys for consistent comparison.
            dict_list1 = [{k: v for k, v in sorted(d.items())} for d in dict_list1]
            dict_list2 = [{k: v for k, v in sorted(d.items())} for d in dict_list2]
        except:
            pass
        
        count1 = len(dict_list1)
        count2 = len(dict_list2)
        
        # Check if the lists have different lengths.
        if count1 != count2:
            self.unmatched_items.append(f"\nKey '{key}' count mismatch:\n\t{self.file1} count: {count1}\n\t{self.file2} count: {count2}")
                
        # Compare each dictionary in the two lists.
        for dict1, dict2 in zip(dict_list1, dict_list2):
            self.handle_format(key, dict1, dict2)

    def handle_format(self, key, value, value2):
        """Determines whether to compare as dicts, lists, or simple values."""
        if isinstance(value, dict):
            # If the value is a dictionary, handle it with handle_dict method.
            self.handle_dict(key, value, value2)
        elif isinstance(value, list):
            # If the value is a list, handle it with handle_array method.
            self.handle_array(key, value, value2)
        else:
            # Compare simple non-dict, non-list values.
            if value != value2:
                mismatch_message = (
                    f'\nKey "{key}" mismatch:\n'
                    f'\t{self.file1} value: {value}\n'
                    f'\t{self.file2} value: {value2}'
                )
                self.unmatched_items.append(mismatch_message)
                
    def compare_json_data_from_files(self):
        """Loads JSON files and compares their content."""
        # Load and convert JSON files to dictionaries.
        json_data_1 = self.load_json_to_dict(f"{self.file1}_payload.json")
        json_data_2 = self.load_json_to_dict(f"{self.file2}_payload.json")
    
        # Compare the data for each key in json_data_1.
        for key, value in json_data_1.items():
            if key in json_data_2:
                value2 = json_data_2.get(key)
                self.handle_format(key, value, value2)
            else:
                # Log if a key from json_data_1 is missing in json_data_2.
                missing_message = (
                    f'\nKey "{key}" is missing in "{self.file2}"\n'
                    f'\tPresent in "{self.file1}" with value: {value}'
                )
                self.unmatched_items.append(missing_message)
        
if __name__ == '__main__':
    # Create an instance of the PayloadComparison class.
    instance = PayloadComparison()
    
    # Set the file names for comparison based on the FILE1 and FILE2 variables.
    instance.file1 = FILE1
    instance.file2 = FILE2
    
    # Start the comparison process.
    instance.compare_json_data_from_files()
    
    # Print the results of unmatched items.
    print(f"\n{'='*30} Unmatched Items {'='*30}")
    for ele in instance.unmatched_items:
        print(ele)
