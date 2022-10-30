
#ifndef ALGOSC_ALGORITHMS_H
#define ALGOSC_ALGORITHMS_H

#ifdef ALG_EXPORTS
#define ALG_DLL __declspec(dllexport)
#else
#define ALG_DLL __declspec(dllimport)
#endif

#define ALG_DECL __cdecl

#define OK 0
#define ERR -1

ALG_DLL int ALG_DECL count_particle_position(double old_speed, double cur_speed, double *old_dir,
                                             double *cur_dir, int fl, double *pos);

#endif //ALGOSC_ALGORITHMS_H
