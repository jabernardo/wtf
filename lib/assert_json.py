class AssertJSON:
    """Assert JSON Class"""

    __results = []

    __check_type_sub = "type:"
    __datatype_map = {
        "string": str.__name__,
        "list": list.__name__,
        "dictionary": dict.__name__,
        "integer": int.__name__,
        "float": float.__name__
    }

    def __init__(self, expected, actual):
        """Assert JSON Class\n

        \nArguments:\n
        `expected` (dict) -- Expected output
        `actual` (dict) -- Actual output
        """
        if not type(expected) == dict:
            raise Exception("Expected results should be a type(dict)")

        if not type(actual) == dict:
            raise Exception("Actual results should be a type(dict)")

        self.__assert(expected, actual)

    def __assert(self, expected, actual, parent = ""):
        """Assert JSON\n

        \nArguments:\n
        `expected` (dict) Expected output
        `actual` (dict) Actual output
        `parent` (str) Key
        """
        for key in expected:
            assert_key = key

            if parent:
                assert_key = f"{parent}.{key}"

            status = "FAILED"
            actual_val = "None"
            actual_type = "None"
            expected_val = expected[key]
            expected_type = type(expected_val).__name__

            if key in actual:
                actual_val = actual[key]
                actual_type = type(actual[key]).__name__

                if expected_type == 'str' and expected_val.startswith(self.__check_type_sub):
                    expected_type = self.__get_type_from_string(expected_val[len(self.__check_type_sub):])
                    if actual_type == expected_type:
                        status = "PASSED"
                elif (expected_type == actual_type and expected_type in ("dict", "list")) or (expected_val == actual[key]):
                    status = "PASSED"

            self.__results.append({
                "status": status,
                "key": assert_key,
                "expected_val": expected_val,
                "expected_type": expected_type,
                "actual_val": actual_val,
                "actual_type": actual_type
            })

            if type(expected_val).__name__ == 'dict' and actual_type == 'dict':
                self.__assert(expected[key], actual[key], assert_key)

    def __get_type_from_string(self, text):
        """Get type from string (example: "type:string")\n
        
        \nArguments:\n
        `text` (str) String

        \nReturns:\n
        `str`
        """
        return self.__datatype_map[text]

    def get_results(self):
        """Get test results\n

        \nReturns:\n
        `list<dict>`
        """
        return self.__results
