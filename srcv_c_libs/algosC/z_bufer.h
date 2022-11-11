#ifndef ALGOSC_Z_BUFER_H
#define ALGOSC_Z_BUFER_H

#include <math.h>
#include <stdio.h>
#include <alloc.h>

#define MAXLINES 1000
#define ZFAR 200

typedef struct Point3d P;
typedef struct Cell C;
typedef struct Object3d Object3d;

//Структура для точки в трехмерном пространстве
struct Point3d {
    double x, y, z;
};

//Структура для объектов в трехмерном пространстве
struct Object3d {
    Point3d *v;
    double color[3];
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
    void PutObjects(Object3d *objs, int n);
    C* Show();
    void Clear();
};
#endif //ALGOSC_Z_BUFER_H
