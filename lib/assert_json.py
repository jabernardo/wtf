class AssertJSON:
    __results = []

    def __init__(self, expected, actual):
        if not type(expected) == dict:
            raise Exception("Expected results should be a type(dict)")

        if not type(actual) == dict:
            raise Exception("Actual results should be a type(dict)")

        self.__assert(expected, actual)

    def __assert(self, expected, actual, parent = ""):
        for key in expected:
            assert_key = key

            if parent:
                assert_key = f"{parent}.{key}"

            status = "PASSED"

            if not key in actual:
                status = "FAILED"

            self.__results.append({
                "status": status,
                "key": assert_key
            })

            if type(expected[key]) == dict:
                self.__assert(expected[key], actual[key], assert_key)

    def get_results(self):
        return self.__results
