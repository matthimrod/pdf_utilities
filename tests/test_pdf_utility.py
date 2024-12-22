from assertpy import assert_that
from pypdf import PdfReader

import pdf_utility

TEST_PDF_1 = 'tests/test_pdf_1.pdf'
TEST_PDF_2 = 'tests/test_pdf_2.pdf'


def test_parse_ranges():
    result = pdf_utility.parse_ranges('2-5')

    assert_that(result).contains_only(1, 2, 3, 4)


def test_parse_ranges_single():
    result = pdf_utility.parse_ranges('6')

    assert_that(result).contains_only(5)


def test_flatten():
    result = pdf_utility.flatten([1, [2, 3], 4])

    assert_that(result) \
        .contains_only(1, 2, 3, 4) \
        .does_not_contain([2, 3])


def test_flatten_multiple():
    result = pdf_utility.flatten([[2, 3], 4, [5, 6, 7], 8, [9, 10]])

    assert_that(result) \
        .contains_only(2, 3, 4, 5, 6, 7, 8, 9, 10) \
        .does_not_contain([2, 3]) \
        .does_not_contain([5, 6, 7]) \
        .does_not_contain([9, 10])


def test_flatten_already_flat():
    result = pdf_utility.flatten([1, 2, 3, 4])

    assert_that(result) \
        .contains_only(1, 2, 3, 4)
