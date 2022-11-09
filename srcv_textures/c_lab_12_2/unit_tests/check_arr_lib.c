#include "check_main.h"

START_TEST(test_fill_array_prime_num_1_number)
{
    int a[1];
    int n = 1;
    fill_array_prime_num(a, n);
    ck_assert_int_eq(a[0], 1);
}
START_TEST(test_fill_array_prime_num_several_numbers_1_full_arr)
{
    int a[3];
    int n = 3;
    fill_array_prime_num(a, n);
    ck_assert_int_eq(a[0], 1);
    ck_assert_int_eq(a[1], 2);
    ck_assert_int_eq(a[2], 3);
}
START_TEST(test_fill_array_prime_num_several_numbers_2_not_full_arr)
{
    int a[7] = {0};
    int n = 6;
    fill_array_prime_num(a, n);
    ck_assert_int_eq(a[0], 1);
    ck_assert_int_eq(a[1], 2);
    ck_assert_int_eq(a[2], 3);
    ck_assert_int_eq(a[3], 5);
    ck_assert_int_eq(a[4], 7);
    ck_assert_int_eq(a[5], 11);
    ck_assert_int_eq(a[6], 0);
}
START_TEST(test_fill_array_prime_num_zero_numbers)
{
    int a[3] = {0};
    int n = 0;
    fill_array_prime_num(a, n);
    ck_assert_int_eq(a[0], 1);
    ck_assert_int_eq(a[1], 0);
    ck_assert_int_eq(a[2], 0);
}
Suite* fill_array_prime_num_suite(void)
{
    Suite *s;
    TCase *tc_neg;
    TCase *tc_pos;

    s = suite_create("fill_array_prime_num");
    tc_neg = tcase_create("negatives");
    tcase_add_test(tc_neg, test_fill_array_prime_num_zero_numbers);
    suite_add_tcase(s, tc_neg);

    tc_pos = tcase_create("positives");
    tcase_add_test(tc_pos, test_fill_array_prime_num_1_number);
    tcase_add_test(tc_pos, test_fill_array_prime_num_several_numbers_1_full_arr);
    tcase_add_test(tc_pos, test_fill_array_prime_num_several_numbers_2_not_full_arr);
    suite_add_tcase(s, tc_pos);
    return s;
}
START_TEST(test_insert_num_after_even_empty_arr)
{
    int src[5];
    int dst[3] = {0};
    int num = -7;
    int n1 = 0, n2 = 3;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 0);
    ck_assert_int_eq(dst[0], 0);
    ck_assert_int_eq(dst[1], 0);
    ck_assert_int_eq(dst[2], 0);
}
START_TEST(test_insert_num_after_even_no_even_nums)
{
    int src[3] = {1, 5, 7};
    int dst[4] = {0};
    int n1 = 3, n2 = 3, num = 10;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 3);
    ck_assert_int_eq(dst[0], 1);
    ck_assert_int_eq(dst[1], 5);
    ck_assert_int_eq(dst[2], 7);
    ck_assert_int_eq(dst[3], 0);
}
START_TEST(test_insert_num_after_even_not_enough_size)
{
    int src[3] = {1, 2, 7};
    int dst[4] = {0};
    int n1 = 3, n2 = 3, num = 10;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 4);
    ck_assert_int_eq(dst[0], 0);
}
START_TEST(test_insert_num_after_even_enough_size_equal)
{
    int src[3] = {1, 2, 7};
    int dst[4] = {0};
    int n1 = 3, n2 = 4, num = 10;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 4);
    ck_assert_int_eq(dst[0], 1);
    ck_assert_int_eq(dst[1], 2);
    ck_assert_int_eq(dst[2], 10);
    ck_assert_int_eq(dst[3], 7);
}
START_TEST(test_insert_num_after_even_enough_size_more)
{
    int src[3] = {1, 2, 7};
    int dst[7] = {0};
    int n1 = 3, n2 = 7, num = 10;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 4);
    ck_assert_int_eq(dst[0], 1);
    ck_assert_int_eq(dst[1], 2);
    ck_assert_int_eq(dst[2], 10);
    ck_assert_int_eq(dst[3], 7);
    ck_assert_int_eq(dst[4], 0);
}
START_TEST(test_insert_num_after_even_all_even)
{
    int src[3] = {2, 2, 8};
    int dst[7] = {0};
    int n1 = 3, n2 = 7, num = -1;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 6);
    ck_assert_int_eq(dst[0], 2);
    ck_assert_int_eq(dst[1], -1);
    ck_assert_int_eq(dst[2], 2);
    ck_assert_int_eq(dst[3], -1);
    ck_assert_int_eq(dst[4], 8);
    ck_assert_int_eq(dst[5], -1);
    ck_assert_int_eq(dst[6], 0);
}
START_TEST(test_insert_num_after_even_in_begin)
{
    int src[3] = {2, 7, 9};
    int dst[7] = {0};
    int n1 = 3, n2 = 7, num = -1;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 4);
    ck_assert_int_eq(dst[0], 2);
    ck_assert_int_eq(dst[1], -1);
    ck_assert_int_eq(dst[2], 7);
    ck_assert_int_eq(dst[3], 9);
    ck_assert_int_eq(dst[4], 0);
    ck_assert_int_eq(dst[5], 0);
    ck_assert_int_eq(dst[6], 0);
}
START_TEST(test_insert_num_after_even_in_middle)
{
    int src[3] = {1, 0, 9};
    int dst[7] = {0};
    int n1 = 3, n2 = 7, num = -1;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 4);
    ck_assert_int_eq(dst[0], 1);
    ck_assert_int_eq(dst[1], 0);
    ck_assert_int_eq(dst[2], -1);
    ck_assert_int_eq(dst[3], 9);
    ck_assert_int_eq(dst[4], 0);
    ck_assert_int_eq(dst[5], 0);
    ck_assert_int_eq(dst[6], 0);
}
START_TEST(test_insert_num_after_even_in_end)
{
    int src[3] = {1, 7, 12};
    int dst[7] = {0};
    int n1 = 3, n2 = 7, num = -1;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 4);
    ck_assert_int_eq(dst[0], 1);
    ck_assert_int_eq(dst[1], 7);
    ck_assert_int_eq(dst[2], 12);
    ck_assert_int_eq(dst[3], -1);
    ck_assert_int_eq(dst[4], 0);
    ck_assert_int_eq(dst[5], 0);
    ck_assert_int_eq(dst[6], 0);
}
START_TEST(test_insert_num_after_even_several_even)
{
    int src[3] = {-44, 7, 12};
    int dst[7] = {0};
    int n1 = 3, n2 = 7, num = -5;
    insert_num_after_even(src, n1, dst, &n2, num);
    ck_assert_int_eq(n2, 5);
    ck_assert_int_eq(dst[0], -44);
    ck_assert_int_eq(dst[1], -5);
    ck_assert_int_eq(dst[2], 7);
    ck_assert_int_eq(dst[3], 12);
    ck_assert_int_eq(dst[4], -5);
    ck_assert_int_eq(dst[5], 0);
    ck_assert_int_eq(dst[6], 0);
}
Suite* insert_num_after_even_suite(void)
{
    Suite *s;
    TCase *tc_neg;
    TCase *tc_pos;

    s = suite_create("insert_num_after_even");
    tc_neg = tcase_create("negatives");
    tcase_add_test(tc_neg, test_insert_num_after_even_no_even_nums);
    tcase_add_test(tc_pos, test_insert_num_after_even_not_enough_size);
    tcase_add_test(tc_pos, test_insert_num_after_even_empty_arr);
    suite_add_tcase(s, tc_neg);

    tc_pos = tcase_create("positives");
    tcase_add_test(tc_pos, test_insert_num_after_even_in_begin);
    tcase_add_test(tc_pos, test_insert_num_after_even_in_middle);
    tcase_add_test(tc_pos, test_insert_num_after_even_in_end);
    tcase_add_test(tc_pos, test_insert_num_after_even_several_even);
    tcase_add_test(tc_pos, test_insert_num_after_even_all_even);
    tcase_add_test(tc_pos, test_insert_num_after_even_enough_size_equal);
    tcase_add_test(tc_pos, test_insert_num_after_even_enough_size_more);
    suite_add_tcase(s, tc_pos);
    return s;
}
