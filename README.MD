# You have no clue about C/C++, but want to boost Python using C/C++ code? Try this!

**cinpy** is made for people who never coded in C/C++, but want to use C/C++ functions/algorithms found somewhere on the internet (GitHub, Stack Overflow, ChatGPT …) in their Python code to speed things up.

### This module is not for massive frameworks, only for small scripts/code snippets. It is very simple and straightforward to use.

#### pip install cinpy

## Please install:

MSVC ..... C++ x64/x86 build tools from: 
[https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&passive=false&cid=2030](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&passive=false&cid=2030)

#### Localize the following files (Version number might vary) and copy their path:

vcvarsall_bat = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"

cl_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe"

link_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe"


### Examples


```python


from cinpy import CreateCppDll

variable_for_function_creation = (
    r"!CT_DATA_DTYPE!_!CT_DATA_DTYPE2!_!C_FUNCTION_NAME!_!CT_DATA_DTYPE3!"
)
appc = CreateCppDll(
    cfunctioname="cppradixsort",
    cfunction=rf"""
!DTYPE_EXPLANATIONC!
__declspec(dllexport) void {variable_for_function_creation}
(!C_DATA_DTYPE! * indatav1,size_t size, 
!C_DATA_DTYPE2! * indatav2, 
!C_DATA_DTYPE3! * outdatav )
{{
   std::vector<!C_DATA_DTYPE!> v(indatav1, 
   indatav1 + size);
   concurrency::parallel_radixsort(begin(v), end(v));
   std::copy(v.begin(), v.begin()+size, outdatav);
}}
""",
    samedtypes=("!C_DATA_DTYPE!", "!C_DATA_DTYPE3!"),
    modulename="radixsortcpp",
    variable_for_function_creation=variable_for_function_creation,
    cheader="""
    //#include <iostream>
    //#include <stdio.h>
    //#include <algorithm>    // std::replace_if
    #include <vector>       // std::vector
    //#include <functional> 
    //#include <conio.h>
    #include <ppl.h>

    """,
    cfooter="",
    ignored_dtypes1=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes2=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes3=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
    compilerflags=("/std:c++17", "/Ferelease", "/EHsc", "/MT", "/O2", "/bigobj"),
)
appc.compile_cpp_code()

# compile and run
from cinpy.radixsortcppmodule import cppradixsort
import numpy as np
arr1 = np.random.randint(0, 10000, 800000000)
arr2 = np.array([],dtype=arr1.dtype)
sodi=cppradixsort(arr1,arr2,arr1.dtype)

import numpy as np
from time import perf_counter
arr1 = np.random.randint(0, 10000, 800000000)
arr2 = np.array([],dtype=arr1.dtype)
start=perf_counter()
sodi=cppradixsort(arr1,arr2,arr1.dtype)
print('c++: ', perf_counter()-start)
start=perf_counter()
np.sort(arr1)
print('numpy: ', perf_counter()-start)
c++:  5.262247000000002
numpy:  36.521482199999994


import numpy as np
from time import perf_counter
arr1 = np.random.randint(0, 10000, 800000000).tolist()
start=perf_counter()
arr1.sort()
print('python: ', perf_counter()-start)
python:  158.9699383

```



```python
from cinpy import CreateCppDll

variable_for_function_creation = (
    r"!CT_DATA_DTYPE!_!CT_DATA_DTYPE2!_!C_FUNCTION_NAME!_!CT_DATA_DTYPE3!"
)
appc = CreateCppDll(
    cfunctioname="cppbufferedsort",
    cfunction=rf"""
!DTYPE_EXPLANATIONC!
__declspec(dllexport) void {variable_for_function_creation}(!C_DATA_DTYPE! * indatav1,size_t size, !C_DATA_DTYPE2! * indatav2, !C_DATA_DTYPE3! * outdatav )
{{
   std::vector<!C_DATA_DTYPE!> v(indatav1, indatav1 + size);
   concurrency::parallel_buffered_sort(begin(v), end(v));
   std::copy(v.begin(), v.begin()+size, outdatav);
}}
""",
    samedtypes=("!C_DATA_DTYPE!", "!C_DATA_DTYPE3!"),
    modulename="bufferedsortcpp",
    variable_for_function_creation=variable_for_function_creation,
    cheader="""
    //#include <iostream>
    //#include <stdio.h>
    //#include <algorithm>    // std::replace_if
    #include <vector>       // std::vector
    //#include <functional> 
    //#include <conio.h>
    #include <ppl.h>

    """,
    cfooter="",
    ignored_dtypes1=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes2=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes3=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
    compilerflags=("/std:c++17", "/Ferelease", "/EHsc", "/MT", "/O2", "/bigobj"),
)
appc.compile_cpp_code()

"""
# Compile and run
from cinpy.bufferedsortcppmodule import cppbufferedsort
import numpy as np
arr1 = np.random.random(8000000)
arr2 = np.array([],dtype=arr1.dtype)
%timeit cppbufferedsort(arr1,arr2,arr1.dtype)
%timeit np.sort(arr1)
193 ms ± 7.74 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
568 ms ± 1.97 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

cppbufferedsort(arr1,arr2,arr1.dtype)
Out[3]:
array([5.84790262e-07, 6.10106611e-07, 6.50635063e-07, ...,
       9.99999442e-01, 9.99999492e-01, 9.99999790e-01])

np.sort(arr1)
Out[6]:
array([5.84790262e-07, 6.10106611e-07, 6.50635063e-07, ...,
       9.99999442e-01, 9.99999492e-01, 9.99999790e-01])
"""
```



```python


from cinpy import CreateCppDll

variable_for_function_creation = (
    r"!CT_DATA_DTYPE!_!CT_DATA_DTYPE2!_!C_FUNCTION_NAME!_!CT_DATA_DTYPE3!"
)
appc = CreateCppDll(
    cfunctioname="variouscalculations",
    cfunction=rf"""
!DTYPE_EXPLANATIONC!
__declspec(dllexport) void {variable_for_function_creation}(!C_DATA_DTYPE! * indatav1,size_t size, !C_DATA_DTYPE2! * indatav2, !C_DATA_DTYPE3! * outdatav )
{{
        concurrency::parallel_for (size_t(0), size, [&](size_t u){{
        outdatav[u] = indatav1[u] * indatav2[0] / indatav2[1] + indatav2[2] - indatav2[3];}});
}}
""",
    samedtypes=(),
    modulename="calcvarious",
    variable_for_function_creation=variable_for_function_creation,
    cheader="""
    //#include <iostream>
    //#include <stdio.h>
    //#include <algorithm>    // std::replace_if
    //#include <vector>       // std::vector
    //#include <functional> 
    //#include <conio.h>
    #include <ppl.h>

    """,
    cfooter="",
    ignored_dtypes1=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes2=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes3=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
    compilerflags=("/std:c++17", "/Ferelease", "/EHsc", "/MT", "/O2", "/bigobj"),
)
appc.compile_cpp_code()


# Compile the code and run:
from cinpy.calcvariousmodule import variouscalculations
import numpy as np
inputarray3np = np.random.randint(0, 10000000, 1000000).astype(np.float64)
inputarray4np = np.array([40.2901,4.21,2.12,6.3])
cp=variouscalculations(inputarray3np,inputarray4np,np.float64)
nu= inputarray3np *40.2901/4.21+2.12-6.3

print(cp)
print(nu)
[15388258.80463183 85115406.42555821 75231240.03558196 ...
 34228493.34042756 68792824.6350119  86092819.36931117]
[15388258.80463183 85115406.42555821 75231240.03558196 ...
 34228493.34042756 68792824.6350119  86092819.36931117]
 
%timeit variouscalculations(inputarray3np,inputarray4np,np.float64)
2.04 ms ± 124 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
%timeit inputarray3np *40.2901/4.21+2.12-6.3
10.2 ms ± 63.6 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


```





```python
from cinpy import CreateCppDll

variable_for_function_creation = (
    r"!CT_DATA_DTYPE!_!CT_DATA_DTYPE2!_!C_FUNCTION_NAME!_!CT_DATA_DTYPE3!"
)
appc = CreateCppDll(
    cfunctioname="multiplybyarray",
    cfunction=rf"""
!DTYPE_EXPLANATIONC!
__declspec(dllexport) void {variable_for_function_creation}(!C_DATA_DTYPE! * indatav1,size_t size, !C_DATA_DTYPE2! * indatav2, !C_DATA_DTYPE3! * outdatav )
{{
        concurrency::parallel_for (size_t(0), size, [&](size_t u){{
        outdatav[u] = indatav1[u] * indatav2[u];}});
}}
""",
    samedtypes=(),
    modulename="multiplyarrays",
    variable_for_function_creation=variable_for_function_creation,
    cheader="""
    //#include <iostream>
    //#include <stdio.h>
    //#include <algorithm>    // std::replace_if
    //#include <vector>       // std::vector
    //#include <functional> 
    //#include <conio.h>
    #include <ppl.h>

    """,
    cfooter="",
    ignored_dtypes1=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes2=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes3=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
    compilerflags=("/std:c++17", "/Ferelease", "/EHsc", "/MT", "/O2", "/bigobj"),
)
appc.compile_cpp_code()


# compile and run
from cinpy.multiplyarraysmodule import multiplybyarray
import numpy as np
inputarray3np = np.random.randint(0, 1005000, 8000000).astype(np.uint64)
inputarray4np = np.random.randint(0, 1022300, 8000000).astype(np.uint64)
%timeit multiplybyarray(inputarray3np,inputarray4np,np.uint64)
%timeit inputarray3np*inputarray4np
18.1 ms ± 757 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
26.6 ms ± 163 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

multiplybyarray(inputarray3np,inputarray4np,np.uint64)
Out[4]:
array([218000641625, 493834462272,  38299985966, ...,  74381999748,
       168393582760, 515058090867], dtype=uint64)
inputarray3np*inputarray4np
Out[5]:
array([218000641625, 493834462272,  38299985966, ...,  74381999748,
       168393582760, 515058090867], dtype=uint64)

```

```python


from cinpy import CreateCppDll

variable_for_function_creation = (
    r"!CT_DATA_DTYPE!_!CT_DATA_DTYPE2!_!C_FUNCTION_NAME!_!CT_DATA_DTYPE3!"
)
appc = CreateCppDll(
    cfunctioname="multiplybynumber",
    cfunction=rf"""
!DTYPE_EXPLANATIONC!
__declspec(dllexport) void {variable_for_function_creation}(!C_DATA_DTYPE! * indatav1,size_t size, !C_DATA_DTYPE2! * indatav2, !C_DATA_DTYPE3! * outdatav )
{{
        concurrency::parallel_for (size_t(0), size, [&](size_t u){{
        outdatav[u] = indatav1[u] * indatav2[0];}});
}}
""",
samedtypes=(),
    modulename="mulbyonenumber",
    variable_for_function_creation=variable_for_function_creation,
    cheader="""
    //#include <iostream>
    //#include <stdio.h>
    //#include <algorithm>    // std::replace_if
    //#include <vector>       // std::vector
    //#include <functional> 
    //#include <conio.h>
    #include <ppl.h>

    """,
    cfooter="",
    ignored_dtypes1=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes2=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    ignored_dtypes3=(
        "bool",
        # "signed char",
        # "unsigned char",
        # "short",
        # "unsigned short",
        # "int",
        # "unsigned int",
        # "long",
        # "unsigned long",
        # "long long",
        # "unsigned long long",
        "float",
        # "double",
        "long double",
        "float complex",
        "double complex",
        "long double complex",
    ),
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
    compilerflags=("/std:c++17", "/Ferelease", "/EHsc", "/MT", "/O2", "/bigobj"),
)
appc.compile_cpp_code()

# compile and run

from cinpy.mulbyonenumbermodule import multiplybynumber
import numpy as np
inputarray3np = np.random.randint(0, 100000, 8000000).astype(np.float64)
inputarray4np = np.array([2.345122],dtype=np.float64)
%timeit multiplybynumber(inputarray3np,inputarray4np,np.float64)
%timeit inputarray3np*inputarray4np[0]
14.5 ms ± 99 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
22.1 ms ± 131 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

multiplybynumber(inputarray3np,inputarray4np,np.float64)
Out[10]:
array([221388.897288, 123871.689162,  40683.176456, ..., 222221.415598,
        73761.122266,  69851.803892])
inputarray3np*inputarray4np[0]
Out[11]:
array([221388.897288, 123871.689162,  40683.176456, ..., 222221.415598,
        73761.122266,  69851.803892])



# There is also a second version (if you need to pass more variables)

from cinpy import CreateCppDllv2

cppco = CreateCppDllv2(
    modulename="cppsort",
    # "module" will be added to "cppsort"
    # This is how to import it after compiling the code:
    # from cinpy.cppsortmodule import cppradixsort
    cheader="""
#include <vector>       // std::vector
#include <ppl.h>

""",  # Code before the functions in the .cpp file -> imports etc.
    cfooter="",  # Code after the functions in the .cpp file
    cfunctioname="cppradixsort",
    # This is the name of the C++ function in Python, this is how you import it:
    # from cinpy.cppsortmodule import cppradixsort
    var_variations={
        # cinpy creates various versions of the functions (I could not make
        # templates/function overloading work with Python) Create a dict with
        # all datadtypes that you want to use for each variable
        "!C_DATA_DTYPE1!": (  # "bool",
            "signed char",
            "unsigned char",
            "short",
            "unsigned short",
            "int",
            "unsigned int",
            "long",
            "unsigned long",
            "long long",
            "unsigned long long",  # "float",
            # "double",
            # "long double",
            # "float complex",
            # "double complex",
            # "long double complex",
        ),
        "!C_DATA_DTYPE2!": ("size_t",),
        "!C_DATA_DTYPE3!": (  # "bool",
            "signed char",
            "unsigned char",
            "short",
            "unsigned short",
            "int",
            "unsigned int",
            "long",
            "unsigned long",
            "long long",
            "unsigned long long",  # "float",
            # "double",
            # "long double",
            # "float complex",
            # "double complex",
            # "long double complex",
        ),
        "!C_DATA_DTYPE4!": ("size_t",),
        "!C_DATA_DTYPE5!": (  # "bool",
            "signed char",
            "unsigned char",
            "short",
            "unsigned short",
            "int",
            "unsigned int",
            "long",
            "unsigned long",
            "long long",
            "unsigned long long",  # "float",
            # "double",
            # "long double",
            # "float complex",
            # "double complex",
            # "long double complex",
        ),
        "!C_DATA_DTYPE6!": ("size_t",),
    },
    dtypemustbeequal=[("!C_DATA_DTYPE1!", "!C_DATA_DTYPE3!", "!C_DATA_DTYPE5!")],
    # "!C_DATA_DTYPE1!", "!C_DATA_DTYPE3!", "!C_DATA_DTYPE5!" will always have the same Datatype
    fu=rf"""
__declspec(dllexport) void variable_for_function_creation
(!C_DATA_DTYPE1! * indatav1,!C_DATA_DTYPE2!  size1,
!C_DATA_DTYPE3! * indatav2,!C_DATA_DTYPE4!  size2,
!C_DATA_DTYPE5! * indatav3,!C_DATA_DTYPE6! size3  )
{{
   std::vector<!C_DATA_DTYPE1!> v(indatav1,
   indatav1 + size1);
   concurrency::parallel_radixsort(begin(v), end(v));
   std::copy(v.begin(), v.begin()+size1, indatav3);

   std::vector<!C_DATA_DTYPE1!> v2(indatav1, indatav1 + size1);
   concurrency::parallel_buffered_sort(begin(v2), end(v2));
   std::copy(v2.begin(), v2.begin()+size1, indatav2);


}}""",
    # The C++ code, use the keys in the dict for the data types, don't change the function name:  variable_for_function_creation
)
cppco.compile_cpp_code(
    vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
    cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
    link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
    compilerflags=("/std:c++20", "/Ferelease", "/EHsc", "/MT", "/O2", "/bigobj"),
) # Compile the code

#import the compiled code

from cinpy.cppsortmodule import cppradixsort
import numpy as np
inputarray = np.array([6,3,2,64,2,46],dtype=np.uint8)
npbufferedsort = np.zeros_like(inputarray)
npradixsort = np.zeros_like(inputarray)
len1=inputarray.size
len2=npbufferedsort.size
len3=npradixsort.size
# arguments always start with v + number, data dtype should be detected automatically
cppradixsort(v0=inputarray,v1=len1,v2=npbufferedsort,v3=len2,v4=npradixsort,v5=len3,)
print(inputarray)
print(npbufferedsort)
print(npradixsort)

# results
# [ 6  3  2 64  2 46]
# [ 2  2  3  6 46 64]
# [ 2  2  3  6 46 64]

```
