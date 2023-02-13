import ctypes

import cinpy
import numpy as np
import time

"""
Same results
pycode[:10]
Out[5]: [8, 34, 22, 40, 2, 4, 72, 11, 19, 50]
resus[:10]
Out[6]: array([ 8, 34, 22, 40,  2,  4, 72, 11, 19, 50])

Time in seconds:
C++  0.003536399999999773
Python  2.8341445000000007
"""

text = np.ascontiguousarray(np.random.randint(97, 123, 1000000000, dtype=np.uint8).view('S128')).tolist()
stringlen = 512



whole_c_code = rf'''
#include <string.h>
#include <iostream>
#include <conio.h>
#include <ppl.h>
std::string convertToString(char* a, int size)
{{
    int i;
    std::string s = "";
    for (i = 0; i < size; i++) {{
        s = s + a[i];
    }}
    return s;
}}

__declspec(dllexport) void para_trans_test(char x [] [{stringlen}],int * y, int si, char sux [])
{{
    int size=si;
    char su = sux[0];
    concurrency::parallel_for (0, {stringlen}, [&](int i)
    {{
       std::string s = convertToString(x[i], {stringlen});
       std::size_t found = s.find(su);
       if (found!=std::string::npos){{
            y[i]=found;
            }}

       }});


}}
'''
all_functions = [("para_trans_test", r"""n""", "aa_", "bb_", None,
                  [ctypes.POINTER(ctypes.c_char * stringlen), ctypes.POINTER(ctypes.c_int), ctypes.c_int,
                   ctypes.POINTER(ctypes.c_char * stringlen)

                   ],), ]

vcvarsall_bat = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
cl_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe"
link_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe"
modulename = "strigi"
cinpy.get_cpp_functions(modulename=modulename, code=whole_c_code, all_functions=all_functions,
    vcvarsall_bat=vcvarsall_bat, cl_exe=cl_exe, link_exe=link_exe, recompile=True, )



def iter_str2bin(binbytes):
    return iter(chr(c) for c in binbytes)


searchsring = 'n'.encode()
bax = (ctypes.c_char * stringlen * 2)()
bax[0].value = searchsring
baxx = np.array(bax, dtype=f'S{stringlen}')
baxx[0][:len(searchsring)] = list(iter_str2bin(searchsring))
baxx=np.require(baxx, f'S{stringlen}', ['ALIGNED'])

p = baxx.ctypes.data_as(ctypes.POINTER(ctypes.c_char * stringlen))



nunu=np.array(text, dtype=f'S{stringlen}')
nunu=np.require(nunu, f'S{stringlen}', ['ALIGNED'])
py_s1 = nunu.ctypes.data_as(ctypes.POINTER(ctypes.c_char * stringlen))

nunu2=np.array([-1 for _ in range(len(text))], dtype=np.int32)
nunu2=np.require(nunu2, np.int32, ['ALIGNED'])

py_s2 = nunu2.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
print(py_s1[0].value, py_s1[1].value)
start=time.perf_counter()
cinpy.bb_para_trans_test(py_s1, py_s2, len(nunu), p)
print('C++ ',time.perf_counter()-start)
print(py_s1[0].value, py_s1[1].value)
resus = py_s2._arr
start=time.perf_counter()
pycode=[x.index(b'n') if b'n' in x else -1 for x in text ]
print('Python ',time.perf_counter()-start)
