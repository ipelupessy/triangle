#include "triangle.h"

typedef REAL *vertex;

#ifdef EXTERNAL_TEST

#ifdef ANSI_DECLARATORS
int triunsuitable_(vertex triorg, vertex tridest, vertex triapex, REAL area)
#else /* not ANSI_DECLARATORS */
int triunsuitable_(triorg, tridest, triapex, area)
vertex triorg;                              /* The triangle's origin vertex. */
vertex tridest;                        /* The triangle's destination vertex. */
vertex triapex;                               /* The triangle's apex vertex. */
REAL area;                                      /* The area of the triangle. */
#endif /* not ANSI_DECLARATORS */
{
  REAL dxoa, dxda, dxod;
  REAL dyoa, dyda, dyod;
  REAL oalen, dalen, odlen;
  REAL maxlen;

  dxoa = triorg[0] - triapex[0];
  dyoa = triorg[1] - triapex[1];
  dxda = tridest[0] - triapex[0];
  dyda = tridest[1] - triapex[1];
  dxod = triorg[0] - tridest[0];
  dyod = triorg[1] - tridest[1];
  /* Find the squares of the lengths of the triangle's three edges. */
  oalen = dxoa * dxoa + dyoa * dyoa;
  dalen = dxda * dxda + dyda * dyda;
  odlen = dxod * dxod + dyod * dyod;
  /* Find the square of the length of the longest edge. */
  maxlen = (dalen > oalen) ? dalen : oalen;
  maxlen = (odlen > maxlen) ? odlen : maxlen;

  if (maxlen > 0.05 * (triorg[0] * triorg[0] + triorg[1] * triorg[1]) + 0.02) {
    return 1;
  } else {
    return 0;
  }
}

int (*triangle_refinement_test)()=triunsuitable_;

#ifdef ANSI_DECLARATORS
int triunsuitable(vertex triorg, vertex tridest, vertex triapex, REAL area)
#else /* not ANSI_DECLARATORS */
int triunsuitable(triorg, tridest, triapex, area)
vertex triorg;                              /* The triangle's origin vertex. */
vertex tridest;                        /* The triangle's destination vertex. */
vertex triapex;                               /* The triangle's apex vertex. */
REAL area;                                      /* The area of the triangle. */
#endif /* not ANSI_DECLARATORS */
{
  return triangle_refinement_test(triorg,tridest,triapex,area);
}

#else /* not EXTERNAL_TEST */

/* nothing to add */

#endif /* not EXTERNAL_TEST */
