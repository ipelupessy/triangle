"""
ctypes interface for triangle

known issues:
- trimalloc takes int, may limit data set size
- harcoded libtriangle name (not platform independent)

"""

import os
import ctypes
import numpy

root = os.path.abspath(os.path.dirname(__file__))
librarypath=os.path.join(root,"libtriangle.so")
libtriangle=ctypes.CDLL(librarypath)

double_pointer=ctypes.POINTER(ctypes.c_double)
int_pointer=ctypes.POINTER(ctypes.c_int)

to_void_p=lambda x: ctypes.cast(x,ctypes.c_voidp)
to_double_p=lambda x: ctypes.cast(x, double_pointer)
to_int_p=lambda x: ctypes.cast(x, int_pointer)

class triangulate_io(ctypes.Structure):
    _fields_=[("pointlist", double_pointer),
              ("pointattributelist", double_pointer),
              ("pointmarkerlist",int_pointer),
              ("numberofpoints",ctypes.c_int),
              ("numberofpointattributes",ctypes.c_int),
              ("trianglelist",int_pointer),
              ("triangleattributelist",double_pointer),
              ("trianglearealist",double_pointer),
              ("neighborlist",int_pointer),
              ("numberoftriangles",ctypes.c_int),
              ("numberofcorners",ctypes.c_int),
              ("numberoftriangleattributes",ctypes.c_int),
              ("segmentlist",int_pointer),
              ("segmentmarkerlist",int_pointer),
              ("numberofsegments",ctypes.c_int),
              ("holelist",double_pointer),
              ("numberofholes",ctypes.c_int),
              ("regionlist",double_pointer),
              ("numberofregions",ctypes.c_int),
              ("edgelist",int_pointer),
              ("edgemarkerlist",int_pointer),
              ("normlist",double_pointer),
              ("numberofedges",ctypes.c_int), ]
    def __init__(self):
        self.numberofpoints = 0
        self.numberofpointattributes = 0
        self.numberoftriangles = 0
        self.numberofcorners = 3
        self.numberoftriangleattributes = 0
        self.numberofsegments = 0
        self.numberofholes = 0
        self.numberofregions = 0
        self.numberofedges = 0
    def __del__(self):
        for name,t in self._fields_:
            if t in [double_pointer,int_pointer]:
                self.cleanup(getattr(self,name))
    @staticmethod
    def cleanup(p):
        if p:
          libtriangle.trifree(p)
    @staticmethod
    def assign(p,arr):
        if p:
            libtriangle.trifree(p)
        if type(p) is double_pointer:
            arr=numpy.ascontiguousarray(arr,dtype='d')
            N=arr.itemsize*arr.size
            p.contents=to_double_p(libtriangle.trimalloc(N)).contents
            q=arr.ctypes.data_as(double_pointer)
        elif type(p) is int_pointer:
            arr=numpy.ascontiguousarray(arr,dtype='i')
            N=arr.itemsize*arr.size
            p.contents=to_int_p(libtriangle.trimalloc(N)).contents
            q=arr.ctypes.data_as(int_pointer)
        else:
            raise Exception("unsupported data")
        ctypes.memmove(p,q,N)
    @staticmethod
    def copy(p,N):
        if p and N>0:
          q=ctypes.pointer(p.contents)
          p.contents=to_double_p(libtriangle.trimalloc(N)).contents
          ctypes.memmove(p,q,N)        

triangulate_io_pointer=ctypes.POINTER(triangulate_io)

libtriangle.trimalloc.restype=ctypes.c_voidp
libtriangle.trimalloc.argtypes=[ctypes.c_int]
libtriangle.trifree.argtypes=[ctypes.c_voidp]
libtriangle.triangulate.argtypes=[ctypes.c_char_p]+3*[triangulate_io_pointer]

class TriangulateIO(object):
    def __init__(self):
        self.c=triangulate_io()
    @property
    def pointlist(self):
        N=self.c.numberofpoints*2
        if N==0: raise ValueError
        return numpy.array(self.c.pointlist[0:N])
    @pointlist.setter
    def pointlist(self,value):
        self.c.numberofpoints=value.size/2
        self.c.assign(self.c.pointlist, value)
    
    @property 
    def pointattributelist(self):
        N=self.c.numberofpoints*self.c.numberofpointattributes
        if N==0: raise ValueError
        return numpy.array(self.c.pointattributelist[0:N])
    @pointattributelist.setter
    def pointattributelist(self,value):
        assert value.size%self.c.numberofpoints==0
        self.c.numberofpointattributes=value.size/self.c.numberofpoints
        assert value.size==self.c.numberofpoints*self.c.numberofpointattributes
        self.c.assign(self.c.pointattributelist, value)

    @property
    def pointmarkerlist(self):
        N=self.c.numberofpoints
        if N==0: raise ValueError
        return numpy.array(self.c.pointmarkerlist[0:N])
    @pointmarkerlist.setter
    def pointmarkerlist(self,value):
        assert value.size==self.c.numberofpoints
        self.c.assign(self.c.pointmarkerlist, value)

    @property
    def trianglelist(self):
        N=self.c.numberoftriangles*self.c.numberofcorners
        if N==0: raise ValueError
        return numpy.array(self.c.trianglelist[0:N])
    @trianglelist.setter
    def trianglelist(self,value):
        self.c.numberoftriangles=value.size/self.c.numberofcorners
        self.c.assign(self.c.trianglelist, value)

    @property
    def triangleattributelist(self):
        N=self.c.numberoftriangles*self.c.numberoftriangleattributes
        if N==0: raise ValueError
        return numpy.array(self.c.triangleattributelist[0:N])
    @triangleattributelist.setter
    def triangleattributelist(self,value):
        assert value.size%self.c.numberoftriangles==0
        self.c.numberoftriangleattributes=value.size/self.c.numberoftriangles
        assert value.size==self.c.numberoftriangles*self.c.numberoftriangleattributes
        self.c.assign(self.c.triangleattributelist, value)

    @property
    def trianglearealist(self):
        N=self.c.numberoftriangleattributes
        if N==0: raise ValueError
        return numpy.array(self.c.trianglearealist[0:N])
    @trianglearealist.setter
    def trianglearealist(self,value):
        if value.size==0:
          self.c.cleanup(self.c.trianglearealist)
          return
        else:
          assert value.size==self.c.numberoftriangles
          self.c.assign(self.c.trianglearealist, value)

    @property
    def numberoftriangles(self):
        return self.c.numberoftriangles
    @numberoftriangles.setter
    def numberoftriangles(self,value):
        self.c.numberoftriangles=value
    @property
    def numberoftriangleattributes(self):
        return self.c.numberoftriangleattributes
    @numberoftriangleattributes.setter
    def numberoftriangleattributes(self,value):
        self.c.numberoftriangleattributes=value

    @property
    def neighborlist(self):
        N=self.c.numberoftriangles*3
        if N==0 or not bool(self.c.neighborlist): raise ValueError
        return numpy.array(self.c.neighborlist[0:N])

    @property
    def segmentlist(self):
        N=self.c.numberofsegments*2
        if N==0 or not bool(self.c.segmentlist): raise ValueError
        return numpy.array(self.c.segmentlist[0:N])
    @segmentlist.setter
    def segmentlist(self,value):
        self.c.numberofsegments=value.size/2        
        self.c.assign(self.c.segmentlist, value)

    @property
    def segmentmarkerlist(self):
        N=self.c.numberofsegments
        if N==0 or not bool(self.c.segmentmarkerlist): raise ValueError
        return numpy.array(self.c.segmentmarkerlist[0:N])
    @segmentmarkerlist.setter
    def segmentmarkerlist(self,value):
        assert self.c.numberofsegments==value.size        
        self.c.assign(self.c.segmentmarkerlist, value)

    @property
    def holelist(self):
        N=self.c.numberofholes*2
        if N==0: raise ValueError
        return numpy.array(self.c.holelist[0:N])
    @holelist.setter
    def holelist(self,value):
        self.c.numberofholes=value.size/2        
        if value.size==0:
            self.c.cleanup(self.c.holelist)
        else:
            self.c.assign(self.c.holelist, value)

    @property
    def regionlist(self):
        N=self.c.numberofregions*4
        if N==0: raise ValueError
        return numpy.array(self.c.regionlist[0:N])
    @regionlist.setter
    def regionlist(self,value):
        self.c.numberofregions=value.size/4
        if value.size==0:
            self.c.cleanup(self.c.regionlist)
        else:
            self.c.assign(self.c.regionlist, value)

    @property
    def edgelist(self):
        N=self.c.numberofedges*2
        if N==0: raise ValueError
        return numpy.array(self.c.edgelist[0:N])
    @property
    def edgemarkerlist(self):
        N=self.c.numberofsegments
        if N==0: raise ValueError
        return numpy.array(self.c.edgemarkerlist[0:N])
    @property
    def normlist(self):
        N=self.c.numberofedges*2
        if N==0: raise ValueError
        return numpy.array(self.c.normlist[0:N])

def triang(switch, in_, out_, vorout=None):
    libtriangle.triangulate(switch, in_.c, out_.c, 
      None if vorout is None else vorout.c)

    # Copy whole array to avoid freeing of non-allocated pointers
    if out_.c.holelist:
      out_.c.copy(out_.c.holelist,out_.c.numberofholes*2)
    if out_.c.regionlist:
      out_.c.copy(out_.c.regionlist,out_.c.numberofregions*2)
 
if __name__=="__main__":
  a=libtriangle.trimalloc(300000)
  p=to_int_p(a)
  libtriangle.trifree(p)
