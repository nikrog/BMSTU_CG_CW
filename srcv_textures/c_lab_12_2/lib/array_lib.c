#include "array_lib.h"
int next_prime_num(int a)
{
    int flag = 1;
    while (flag)
    {
        int k_del = 0;
        a += 1;
        for (int d = 2; d < a - 1; d++)
        {
            if (a % d == 0)
            {
                k_del++;
                break;
            }
        }
        if (k_del == 0)
            flag = 0;
    }
    return a;
}
ARR_DLL void ARR_DECL fill_array_prime_num(int *arr, int n)
{
    int a = 1;
    arr[0] = a;
    if (n > 1)
    {
        for (int i = 1; i < n; i++)
        {
            a = next_prime_num(a);
            arr[i] = a;
        }
    }
}
ARR_DLL int ARR_DECL insert_num_after_even(int *src, int n1, int *dst, int *n2, int num)
{
    int n = 0;
    for (int i = 0; i < n1; i++)
    {
        if (src[i] % 2 == 0)
            n++;
        n++;
    }
    if (n > *n2)
    {
        *n2 = n;
        return 1;
    }
    n = 0;
    for (int i = 0; i < n1; i++)
    {
        dst[n] = src[i];
        if (src[i] % 2 == 0)
        {
            n++;
            dst[n] = num;
        }
        n++;
    }
    *n2 = n;
    return 0;
}