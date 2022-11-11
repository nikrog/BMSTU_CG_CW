#ifndef ARRAY_LIB_H
#define ARRAY_LIB_H

#ifdef ARR_EXPORTS
#define ARR_DLL __declspec(dllexport)
#else
#define ARR_DLL __declspec(dllimport)
#endif

#define ARR_DECL __cdecl

ARR_DLL void ARR_DECL fill_array_prime_num(int *arr, int n);
//ARR_DLL int ARR_DECL count_particle_position(double old_speed, double cur_speed, double *old_dir,
                                             double *cur_dir, int fl, double *pos);
int next_prime_num(int a);
ARR_DLL int ARR_DECL insert_num_after_even(int *src, int n1, int *dst, int *n2, int num);

#endif // ARRAY_LIB_H
