# dy='float32'
# import numpy as np
# indata = np.random.randint(1,300000000,size=3000000)
# indata =indata.astype(dy)
# a = np.require(indata, dy, ['ALIGNED'])
# indatab = np.random.randint(1, 300000000,size=3000000)
# indatab =indatab.astype(dy)
# b = np.require(indatab, dy, ['ALIGNED'])
# %timeit cinpy.aa_cpp_buffered_sort_float(a)
# %timeit np.sort(a)
# 56.2 ms ± 382 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 192 ms ± 229 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
import importlib
import cinpy


modulename = "cppsort_psort"
moduleimport, folder, argtypesfile, cfile, sofile = cinpy.get_all_files_for_module(
   modulename
)  # C++ files generated this way, will be saved in the cinpy folder
whole_python_argtypes, whole_c_code = cinpy.create_signature_variations(
   basefunction="cpp_parallel_sort",
   code_c_function="""
__declspec(dllexport) void !BASE_FUNCTION_NAME!(const !C_DATA_DTYPE! *indatav, size_t size, !C_DATA_DTYPE! *outdatav !ADDEXTRA!)
{
   size_t i;
   for (i = 0; i < size; ++i){
       outdatav[i] = indatav[i];};
   std::vector<!C_DATA_DTYPE!> v(outdatav, outdatav + i);
   parallel_sort(begin(v), end(v));
   std::copy(v.begin(), v.begin()+i, outdatav);
}

""",
   savepath_argtypes=argtypesfile,
   savepath_cfunctions=cfile,
   # Let's copy all imports from the Microsoft example.
   # Not all imports are necessary since we are using only parallel_radixsort,
   # but this module is for people without C/C++ knowledge who want to speed up
   # their Python code without spending half of their life editing C++ code.
   c_file_header="""  
#include <ppl.h>

using namespace concurrency;
using namespace std;""",
   add_to_function_signature="",
   add_to_argtypes="",
   add_to_top_of_py_file="",
   prefix_for_partial_functions="aa_",
   prefix_for_functions="bb_",
   ignored_dtypes=(
       "bool",
       "np.csingle",
       "np.cdouble",
       "np.clongdouble",
       "np.longdouble",
       #"double",
       #"float",
   ),
)

vcvarsall_bat = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
cl_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe"
link_exe = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe"

try:
   baxax = importlib.import_module(
       f'cinpy.{moduleimport}'
   )  # imports the generated argtypes from the code above
except Exception:
   baxax = importlib.import_module(
       moduleimport
   )  # imports the generated argtypes from the code above
all_functions = getattr(baxax, "all_functions")

cinpy.get_cpp_functions(
   modulename=modulename,
   code=whole_c_code,
   all_functions=all_functions,
   vcvarsall_bat=vcvarsall_bat,
   cl_exe=cl_exe,
   link_exe=link_exe,
   recompile=True,
)