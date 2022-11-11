#include "algorithms.h"

ALG_DLL int ALG_DECL count_particle_position(double old_speed, double cur_speed,
                                             double *old_dir, double *cur_dir, int fl, double *pos)
{
    if (fl == 2)
    {
        pos[0] = pos[0] + old_speed * old_dir[0] + (cur_speed * cur_dir[0]) / 2;
        pos[1] = pos[1] - (old_speed * old_dir[1] + (cur_speed * cur_dir[1]) / 2);
        pos[2] = pos[2] - (old_speed * old_dir[2] + (cur_speed * cur_dir[2]) / 2);
    }
    else
    {
        pos[0] = pos[0] + old_speed * old_dir[0] + (cur_speed * cur_dir[0]) / 2;
        if (fl == 1) {
            pos[1] = pos[1] + old_speed * old_dir[1] + (cur_speed * cur_dir[1]) / 2;
        }
        pos[2] = pos[2] + old_speed * old_dir[2] + (cur_speed * cur_dir[2]) / 2;
    }
    return OK;
}



