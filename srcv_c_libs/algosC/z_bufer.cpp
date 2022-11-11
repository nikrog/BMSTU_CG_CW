#include "z_bufer.h"

ZBuffer::ZBuffer (int ax, int ay) {
    sX = ax; sY = ay;
    for (int i = 0; i < sY; i++) {
        //Выделение памяти под ячейки буфера
        buff[i] = (struct Cell *)malloc (sX * sizeof(struct Cell));
    }
}

ZBuffer::~ZBuffer() {
    for (int i = 0; i < sY; i++)
        free(buff[i]); //Освобождение памяти
}

void ZBuffer::PutObjects(Object3d *objs, int n) {
    int ymax, ymin, ysc, e1, e, i;
    int x[3], y[3];
    //Заносим x,y из objects в массивы для последующей работы с ними
    for (i = 0; i < n; i++)
        x[i] = int(objs[i].v.x);
    y[i] = int(objs[i].v.y);
    //Определяем максимальный и минимальный y
    ymax = ymin = y[0];
    if (ymax < y[1]) ymax = y[1];
    else if (ymin > y[1]) ymin = y[1];
    if (ymax < y[2]) ymax = y[2];
    else if (ymin > y[2]) ymin = y[2];
    ymin = (ymin < 0) ? 0 : ymin;
    ymax = (ymax < sY) ? ymax : sY;
    int ne;
    int x1, x2, xsc1, xsc2;
    double z1, z2, tc, z;
    //Следующий участок кода перебирает все строки сцены
    //и определяет глубину каждого пикселя
    //для соответствующего объекта
    for (ysc = ymin; ysc < ymax; ysc++) {
        ne = 0;
        for (int e = 0; e < 3; e++) {
            e1 = e + 1;
            if (e1 == 3) e1 = 0;
            if (y[e] < y[e1]) {
                if (y[e1] <= ysc || ysc < y[e]) continue;
            }
            else if (y[e] > y[e1]) {
                if (y[e1] > ysc || ysc >= y[e]) continue;
            }
            else continue;
            tc = double(y[e] - ysc) / (y[e] - y[e1]);
            if (ne)
                x2 = x[e] + int (tc * (x[e1] - x[e])),
                        z2 = objs[e].v.z + tc * (objs[e1].v.z - objs[e].v.z);
            else
                x1 = x[e] + int (tc * (x[e1] - x[e])),
                z1 = objs[e].v.z + tc * (objs[e1].v.z - objs[e].v.z),
                ne = 1;
        }
        if (x2 < x1) e = x1, x1 = x2, x2 = e, tc = z1, z1 = z2, z2 = tc;
        xsc1 = (x1 < 0) ? 0 : x1;
        xsc2 = (x2 < sX) ? x2 : sX;
        for (int xsc = xsc1; xsc < xsc2; xsc++) {
            tc = double(x1 - xsc) / (x1 - x2);
            z = z1 + tc * (z2 - z1);
            //Если полученная глубина пиксела меньше той,
            //что находится в Z-Буфере - заменяем храняшуюся на новую.
            if (z < (*(buff[ysc] + xsc)).z)
                for (int i = 0; i < 3; i++) {
                    (*(buff[ysc] + xsc)).color = objects[ysc].color;
                }
            (*( buff[ysc] + xsc)).z = z;
        }
    }
}

//Функция, очищающая Z-буфер.
void ZBuffer::Clear() {
    for (int j = 0; j < sY; j++ )
        for (int i = 0; i < sX; i++)
            //Инициализируем ячейки Z-буфера
            (*( buff[j] + i)).z = ZFAR;
    (*( buff[j] + i)).color = {0, 0, 0};
}

void ZBuffer::Show() {
    return buff;
}


