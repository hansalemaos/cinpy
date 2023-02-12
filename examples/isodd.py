# Adapted from
# https://cplusplus.com/reference/algorithm/replace_if/

# indatarad = np.random.randint(1, 15000001, size=15000000)
# indatarad = indatarad.astype(np.uint64)
# %timeit cinpy.aa_isnumberodd_ulonglong(indatarad)
# indatarad2 = indatarad.copy()
# %timeit indatarad2[np.where(indatarad %2!=0)]=0 # the corresponding numpy code
# 151 ms ± 1.28 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 185 ms ± 2.12 ms per loop (mean ± std. dev. of 7 runs, 10 loops each) # numpy
#
import importlib
import cinpy



modulename = "isoddcpp"
moduleimport, folder, argtypesfile, cfile, sofile = cinpy.get_all_files_for_module(
   modulename
)  # C++ files generated this way, will be saved in the cinpy folder
whole_python_argtypes, whole_c_code = cinpy.create_signature_variations(
   basefunction="isnumberodd",
   code_c_function="""
  __declspec(dllexport) void !BASE_FUNCTION_NAME!(const !C_DATA_DTYPE! *indatav, size_t size, !C_DATA_DTYPE! *outdatav !ADDEXTRA!)
{
   size_t i;
   for (i = 0; i < size; ++i){
       outdatav[i] = indatav[i];};
   std::vector<!C_DATA_DTYPE!> v(outdatav, outdatav + i);

   std::replace_if (v.begin(), v.end(), IsOdd, 0); 
   std::copy(v.begin(), v.begin()+i, outdatav);
}
""",
   savepath_argtypes=argtypesfile,
   savepath_cfunctions=cfile,
   c_file_header="""  
#include <iostream>     // std::cout
#include <algorithm>    // std::replace_if
#include <vector>       // std::vector

bool IsOdd (int i) { return ((i%2)==1); };
""",
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
       "double",
       "float",
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