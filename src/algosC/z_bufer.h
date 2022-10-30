#ifndef ALGOSC_Z_BUFER_H
#define ALGOSC_Z_BUFER_H

#include <math.h>
#include <stdio.h>
#include <alloc.h>

#define MAXLINES 1000
#define ZFAR 200

typedef struct Point3d P;
typedef struct Cell C;

//Структура для точки в трехмерном пространстве
struct Point3d {
    double x, y, z;
};

//Структура для ячейки Z-буфера
struct Cell {
    double z;
    double color[3];
};

class ZBuffer {
public:
    C *buff[MAXLINES];
    int sX, sY;	// Размер Z-Буфера
    ZBuffer(int, int);
    ~ZBuffer();
    void PutObjects(Point3d *vertices, double *colors, int n);
    C* Show();
    void Clear();
};
#endif //ALGOSC_Z_BUFER_H
