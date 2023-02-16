# adding one array to another
# dy='int'
# import numpy as np
# indata = np.random.randint(1,300000000,size=3000000)
# indata =indata.astype(dy)
# a = np.require(indata, dy, ['ALIGNED'])
# indatab = np.random.randint(1, 300000000,size=3000000)
# indatab =indatab.astype(dy)
# b = np.require(indatab, dy, ['ALIGNED'])
# %timeit cinpy.aa_adda_int(a,b)
# 4 ms ± 10.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# %timeit a+b
# 4.27 ms ± 66.5 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

import os
import cinpy

modulename = "addarray" # Any name for your module
moduleinport, folder, argtypesfile, cfile, sofile = cinpy.get_all_files_for_module(
    modulename
) # files are stored in the folder of the cinpy module to make the import easier
if not os.path.exists(sofile) or os.path.exists(sofile):
    whole_python_argtypes, whole_c_code = cinpy.create_signature_variations(
        basefunction="adda", # whatever you want because this script will auto-generate the C code and add an individual suffix (the data type) to each function

        # !BASE_FUNCTION_NAME! Will be replaced by cfun_short, cfun_long ...
        # !C_DATA_DTYPE! Leave it like it is
        # !ADDEXTRA! If you want to add more variables to the function signature
        # We will see an example soon.

        code_c_function=r"""
void !BASE_FUNCTION_NAME!(const !C_DATA_DTYPE!  *indatav, size_t size, !C_DATA_DTYPE!  *outdatav , const !C_DATA_DTYPE!  *addarray)
{
        size_t i;
        for (i = 0; i < size; ++i){
        *outdatav++ = *indatav++ + *addarray++;};
}
""",
        savepath_argtypes=argtypesfile, # the Python file with all the argtypes. It will be generated, but you can edit it afterward if you like.
        savepath_cfunctions=cfile,# C file with the whole C-code. (Generated, but can be edited)
        c_file_header="#include <stdio.h>", # everything you want to have above the generated functions
        add_to_function_signature="",  # !ADDEXTRA! will be replaced by this string
        add_to_argtypes="ndpointer(!CT_DATA_DTYPE!, flags=\"aligned,C_CONTIGUOUS\"),", # If you add additional variables (!ADDEXTRA!) you can add them to argtypes already to save some time # Example later on
        add_to_top_of_py_file="", # The Python import file for argtypes, usually nothing needed (Generated, but can be edited)
        prefix_for_partial_functions="aa_", # fewer arguments because it will make a copy of the array and get its size and pass everything to the C function.
        prefix_for_functions="bb_", # more arguments (size, copy of array)
        ignored_dtypes=(
            "bool",
            "np.csingle",
            "np.cdouble",
            "np.clongdouble",
            "np.longdouble",
        ), # Let's ignore those data types, complete list: cinpy.print_datatypes()
    )

    sofile = cinpy.compile_c_code(
        gcc_exe="gcc.exe", c_code=whole_c_code, modulename=modulename, folder=None
    ) # compiling the code
cinpy.load_module_extern_py_file(modulename) # importing it