#include <stdlib.h>
#include <stdio.h>
#include "algorithms.h"

int main()
{
    double pos[3] = {0, 0, 0};
    double dir1[3] = {0.2, -0.3, 0.1};
    double dir2[3] = {0.2, -0.4, 0.1};
    double sp1 = 0.0001;
    double sp2 = 0.00015;
    count_particle_position(sp1, sp2, dir1, dir2, 1, pos);
    for (int i = 0; i < 3; i++)
    {
        printf("%f ", pos[i]);
    }
    return 0;
}
