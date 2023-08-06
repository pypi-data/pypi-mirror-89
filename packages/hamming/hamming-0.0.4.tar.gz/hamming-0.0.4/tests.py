"""
File:		tests.py
Author:		Ambuj Dubey (ambujdubey2426@gmail.com)
Created:	December 20, 2020

Suite of unit tests for functions in hammmingcode.py.
Each test returns a tuple of ((0, '') if test passed else # tests failed,
 textual info about the failure).
"""
from sys import stderr, stdout
from hamming import hammingcode

# total number of unit tests (for nice output format purposes when running)
N_TESTS = 9


# GENERATE HAMMING CODE FOR "101" DATA
def generate_hamming_code_for_101_binary_data_test1():
    actual = hammingcode.generate_hamming_code("101")
    expected = "101101"
    return (0, "") if str(actual) == expected else (
        1, "generate_hamming_code_for_101_binary_data_test1 FAILED! Expected: "
           "{0}, Actual: {1}\n".format(expected, actual))


# GENERATE HAMMING CODE FOR INTEGER TYPE DATA - NEGATIVE TEST CASE
def generate_hamming_code_for_102_integer_type_data_Negative_test2():
    try:
        actual = hammingcode.generate_hamming_code(102)
    except Exception as e:
        error = e
    expected = "\'int\' object is not iterable"
    return (0, "") if str(error) == expected else (
        1, "generate_hamming_code_for_101_binary_data_test1 FAILED! Expected: "
           "{0}, Actual: {1}\n".format(expected, error))


# GENERATE HAMMING CODE FOR LONG LENGTH 285 BITS DATA


def generate_hamming_code_for_long_binary_data_test3():
    actual = hammingcode.generate_hamming_code("10100101010010101001010100101"
                                               "01001010101001010101001010101"
                                               "00101010100101010101010101010"
                                               "01010010100101001010100101010"
                                               "01001010010100101010010100101"
                                               "01010100101010010010100101001"
                                               "01001001010010101001001010010"
                                               "01100101010100101010010100101"
                                               "01001010010100101001010010101"
                                               "001010011001010101101001")
    expected = "1010010101001010100101010010101001010110100101010100101010" \
               "1001010101001010101010101010100101001010010100101010010101" \
               "0010010100101001010100101001010101010010101001001001001010" \
               "0101001001010010101001001010010011001010101001010100101000" \
               "10101001010010100101001010010100100101001100100101011001001100"
    return (0, "") if str(actual) == expected else (
        1, "generate_hamming_code_for_101_binary_data_test1 FAILED! Expected:"
           " {0}, Actual: {1}\n".format(expected, actual))


# DETECT ERROR IN CORRECT HAMMING CODE
def detect_zero_bit_error_in_hamming_code_test4():
    actual = hammingcode.detect_error_in_hamming_code("101101")
    expected = "There is no error in the hamming code received"
    return (0, "") if actual == expected else (
        1, "generate_hamming_code_for_101_binary_data_test1 FAILED! Expected:"
           " {0}, Actual: {1}\n".format(expected, actual))


# DETECT SINGLE BIT ERROR IN HAMMING CODE
def detect_single_bit_error_in_hamming_code_test5():
    actual = hammingcode.detect_error_in_hamming_code("101001")
    expected = "Error is in,3, bit\nAfter correction hamming code is:-\n101101"
    return (0, "") if actual == expected else (
        1, "generate_hamming_code_for_101_binary_data_test1 FAILED! Expected:"
           " {0}, Actual: {1}\n".format(expected, actual))


# DETECT MULTIPLE BIT ERROR IN HAMMING CODE
def detect_multiple_bit_error_in_hamming_code_test6():
    actual = hammingcode.detect_error_in_hamming_code("100001")
    expected = "Error cannot be detected"
    return (0, "") if actual == expected else (
        1, "generate_hamming_code_for_101_binary_data_test1 FAILED! Expected:"
           " {0}, Actual: {1}\n".format(expected, actual))


# DETECT SINGLE BIT ERROR IN LONG LENGTH HAMMING CODE
def detect_error_in_long_length_hamming_code_test7():
    actual = hammingcode.detect_error_in_hamming_code("101001010100101010010"
                                                      "101001010100101011010"
                                                      "010101010010101010010"
                                                      "101010010101010101010"
                                                      "101001010010100101001"
                                                      "010100101010010010100"
                                                      "101001010100101001010"
                                                      "101010010101001001001"
                                                      "001010010100100101001"
                                                      "010100100101001001100"
                                                      "101010100101010010100"
                                                      "010101001010010100101"
                                                      "001010010100100101001"
                                                      "100100101011001001101")
    expected = "Error is in,1, bit\nAfter correction hamming code is:-\n1010" \
               "010101001010100101010010101001010110100101010100101010100101" \
               "010100101010101010101010010100101001010010101001010100100101" \
               "001010010101001010010101010100101010010010010010100101001001" \
               "010010101001001010010011001010101001010100101000101010010100" \
               "10100101001010010100100101001100100101011001001100"
    return (0, "") if str(actual) == expected else (
        1, "generate_hamming_code_for_101_binary_data_test1 FAILED! Expected:"
           " {0}, Actual: {1}\n".format(expected, actual))


# DETECT ERROR IN WRONG HAMMING CODE-NEGATIVE TEST CASE
def detect_error_in_non_binary_hamming_code_Negative_test8():
    try:
        actual = hammingcode.detect_error_in_hamming_code("a01001")
    except Exception as e:
        error = e
    expected = "invalid literal for int() with base 10: \'a\'"
    return (0, "") if str(error) == expected else (
        1, "generate_hamming_code_for_101_binary_data_test1 FAILED! Expected:"
           " {0}, Actual: {1}\n".format(expected, error))


# DETECT ERROR IN INTEGER TYPE HAMMING CODE-NEGATIVE TEST CASE
def detect_error_in_integer_type_hamming_code_Negative_test9():
    try:
        actual = hammingcode.detect_error_in_hamming_code(101001)
    except Exception as e:
        error = e
    expected = "\'int\' object is not iterable"
    return (0, "") if str(error) == expected else (
        1, "generate_hamming_code_for_101_binary_data_test1 FAILED! Expected:"
           " {0}, Actual: {1}\n".format(expected, error))


# RUN ALL THE TEST CASES
def run_tests():
    test1 = generate_hamming_code_for_101_binary_data_test1()
    test2 = generate_hamming_code_for_102_integer_type_data_Negative_test2()
    test3 = generate_hamming_code_for_long_binary_data_test3()
    test4 = detect_zero_bit_error_in_hamming_code_test4()
    test5 = detect_single_bit_error_in_hamming_code_test5()
    test6 = detect_multiple_bit_error_in_hamming_code_test6()
    test7 = detect_error_in_long_length_hamming_code_test7()
    test8 = detect_error_in_non_binary_hamming_code_Negative_test8()
    test9 = detect_error_in_integer_type_hamming_code_Negative_test9()
    total_failed_test_cases = test1[0] + test2[0] + test3[0] + test4[0] \
                              + test5[0] + test6[0] + test7[0] + test8[0] \
                              + test9[0]
    error_output = test1[1] + test2[1] + test3[1] + test4[1] + test5[1] +\
                   test6[1] + test7[1] + test8[1] + test9[1]
    return total_failed_test_cases, error_output


def main():
    total_failed, error_output = run_tests()
    if total_failed:
        stderr.write(error_output)
        stderr.write("{0} of {1} test cases passed. {2} tests failed.\n"
                     .format(N_TESTS - total_failed, N_TESTS, total_failed))
        exit(1)
    stdout.write("All {0} test cases passed!\n".format(N_TESTS))
    return None


if __name__ == '__main__':
    main()
