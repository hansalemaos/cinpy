import collections
import configparser
import itertools
import os
import re
import subprocess
from time import sleep

from cprinter import TC
import numpy as np
import ctypes

from touchtouch import touch

nested_dict = lambda: collections.defaultdict(nested_dict)
d_types2 = collections.namedtuple("d_types", "np c ct use comment code alias")
d_typesall = []
d_typesall.append(
    d_types2(
        np="np.bool_",
        c="bool",
        ct="ctypes.c_bool",
        use=True,
        comment="The bool_ type is not a subclass of the int_ type (the bool_ is not even a number type). T",
        code="?",
        alias="numpy.bool8",
    )
)
d_typesall.append(
    d_types2(
        np="np.byte",
        c="signed char",
        ct="ctypes.c_byte",
        use=True,
        comment="Signed integer type, compatible with C char",
        code="b",
        alias="numpy.int8: 8-bit signed integer (-128 to 127).",
    )
)
d_typesall.append(
    d_types2(
        np="np.ubyte",
        c="unsigned char",
        ct="ctypes.c_ubyte",
        use=True,
        comment="Unsigned integer type, compatible with C unsigned char. ",
        code="B",
        alias="numpy.uint8: 8-bit unsigned integer (0 to 255).",
    )
)
d_typesall.append(
    d_types2(
        np="np.short",
        c="short",
        ct="ctypes.c_short",
        use=True,
        comment="Signed integer type, compatible with C short.",
        code="h",
        alias="numpy.int16: 16-bit signed integer (-32_768 to 32_767)",
    )
)
d_typesall.append(
    d_types2(
        np="np.ushort",
        c="unsigned short",
        ct="ctypes.c_ushort",
        use=True,
        comment="Unsigned integer type, compatible with C unsigned short",
        code="H",
        alias="numpy.uint16: 16-bit unsigned integer (0 to 65_535)",
    )
)
d_typesall.append(
    d_types2(
        np="np.intc",
        c="int",
        ct="ctypes.c_int",
        use=True,
        comment="Signed integer type, compatible with C int",
        code="i",
        alias="numpy.int32: 32-bit signed integer (-2_147_483_648 to 2_147_483_647)",
    )
)
d_typesall.append(
    d_types2(
        np="np.uintc",
        c="unsigned int",
        ct="ctypes.c_uint",
        use=True,
        comment="Unsigned integer type, compatible with C unsigned int",
        code="I",
        alias="numpy.uint32: 32-bit unsigned integer (0 to 4_294_967_295)",
    )
)
d_typesall.append(
    d_types2(
        np="np.int_",
        c="long",
        ct="ctypes.c_long",
        use=True,
        comment="Signed integer type, compatible with Python int and C long",
        code="l",
        alias="numpy.int64: 64-bit signed integer (-9_223_372_036_854_775_808 to 9_223_372_036_854_775_807) / numpy.intp: Signed integer large enough to fit pointer, compatible with C intptr_t.",
    )
)
d_typesall.append(
    d_types2(
        np="np.uint",
        c="unsigned long",
        ct="ctypes.c_ulong",
        use=True,
        comment="Unsigned integer type, compatible with C unsigned long",
        code="L",
        alias="numpy.uint32: 32-bit unsigned integer (0 to 4_294_967_295)",
    )
)
d_typesall.append(
    d_types2(
        np="np.longlong",
        c="long long",
        ct="ctypes.c_longlong",
        use=True,
        comment="Signed integer type, compatible with C long long",
        code="q",
        alias="",
    )
)
d_typesall.append(
    d_types2(
        np="np.ulonglong",
        c="unsigned long long",
        ct="ctypes.c_ulonglong",
        use=True,
        comment="Signed integer type, compatible with C unsigned long long",
        code="Q",
        alias="",
    )
)
d_typesall.append(
    d_types2(
        np="np.single",
        c="float",
        ct="ctypes.c_float",
        use=True,
        comment="Single-precision floating-point number type, compatible with C float",
        code="f",
        alias="numpy.float32: 32-bit-precision floating-point number type: sign bit, 8 bits exponent, 23 bits mantissa.",
    )
)
d_typesall.append(
    d_types2(
        np="np.double",
        c="double",
        ct="ctypes.c_double",
        use=True,
        comment="Double-precision floating-point number type, compatible with Python float and C double",
        code="d",
        alias="numpy.float64: 64-bit precision floating-point number type: sign bit, 11 bits exponent, 52 bits mantissa.",
    )
)
d_typesall.append(
    d_types2(
        np="np.longdouble",
        c="long double",
        ct="ctypes.c_longdouble",
        use=True,
        comment="Extended-precision floating-point number type, compatible with C long double but not necessarily with IEEE 754 quadruple-precision.",
        code="g",
        alias="numpy.float128: 128-bit extended-precision floating-point number type.",
    )
)
d_typesall.append(
    d_types2(
        np="np.csingle",
        c="float complex",
        ct="ctypes.c_double",
        use=True,
        comment="Complex number type composed of two single-precision floating-point numbers",
        code="F",
        alias="numpy.complex64: Complex number type composed of 2 32-bit-precision floating-point numbers.",
    )
)
d_typesall.append(
    d_types2(
        np="np.cdouble",
        c="double complex",
        ct="ctypes.c_double",
        use=True,
        comment="Complex number type composed of two double-precision floating-point numbers, compatible with Python complex.",
        code="D",
        alias="numpy.complex128: Complex number type composed of 2 64-bit-precision floating-point numbers.",
    )
)
d_typesall.append(
    d_types2(
        np="np.clongdouble",
        c="long double complex",
        ct="ctypes.c_longdouble",
        use=True,
        comment="Complex number type composed of two extended-precision floating-point numbers.",
        code="G",
        alias="Complex number type composed of 2 128-bit extended-precision floating-point numbers",
    )
)
d_typesall.append(
    d_types2(
        np="np.int32",
        c="size_t",
        ct="ctypes.c_size_t",
        use=True,
        comment="for size",
        code="",
        alias="for size",
    )
)


def compile_cpp_codev2(
    outputdll,
    cfgfile,
    cpath,
    modulename,
    vcvarsall_bat,
    cl_exe,
    link_exe,
    compilerflags,
    allfunctionvariations,
):
    try_delete_file(outputdll)
    try_delete_file(cfgfile)
    try_delete_file(outputdll[:-3] + "exp")
    try_delete_file(outputdll[:-3] + "lib")
    try_delete_file(cpath[-3] + "obj")
    compile_cppv2(
        modulename=modulename,
        fnames=allfunctionvariations,
        vcvarsall_bat=vcvarsall_bat,
        cl_exe=cl_exe,
        link_exe=link_exe,
        cppsource=cpath,
        compilerflags=compilerflags,
    )


def compile_cppv2(
    modulename,
    fnames,
    vcvarsall_bat,
    cl_exe,
    link_exe,
    cppsource,
    compilerflags=(
        "/std:c++20",
        "/Ferelease",
        "/EHsc",
        "/MT",
        "/O2",
        "/bigobj",
    ),
):
    cfgfile = get_file(f"{modulename}.ini")
    output = get_file(f"{modulename}.dll")

    config = configparser.ConfigParser()
    allcommand = [
        vcvarsall_bat,
        "x64",
        "&&",
        cl_exe,
        "/D_USRDL",
        "/D_WINDLL",
        cppsource,
        *compilerflags,
        "/link",
        "/DLL",
        f'/OUT:"{output}"',
        "/MACHINE:X64",
    ]
    subprocess.run(allcommand, shell=True)

    p = subprocess.run([link_exe, "/dump", "/exports", output], capture_output=True)
    fnamesre = [
        (
            x,
            re.compile(
                rf"[\r\n]+\s+[a-fA-F0-9]+\s+[a-fA-F0-9]+\s+[a-fA-F0-9]+\s+(\?[^\s]*{x}@[^\s]+)"
            ),
        )
        for x in fnames
    ]
    decor = p.stdout.decode("utf-8", "ignore")
    print(decor)
    franmesre = [(x[0], x[1].findall(decor)) for x in fnamesre]
    config["DEFAULT"] = {k: v[0] for k, v in franmesre if v}
    with open(cfgfile, "w") as f:
        config.write(f)


def iter_nested_for_loop(*args):
    for vals in itertools.product(*args):
        yield vals


def write_source_code_filesv2(
    modulename, var_variations, dtypemustbeequal, fu, cfunctioname, cheader, cfooter
):
    cfgfile = get_file(f"{modulename}.ini")
    outputdll = get_file(f"{modulename}.dll")
    cpath = get_file(f"{modulename}_cppcode.cpp")
    pypath = get_file(f"{modulename}module.py")

    allvari = []
    for q in list(iter_nested_for_loop(*[x[1] for x in var_variations.items()])):
        allvari.append({qq: k for qq, k in zip(list(var_variations.keys()), q)})

    allvarifinal = []
    for v in allvari:
        checkva = []

        for d in dtypemustbeequal:
            for dd in d:
                checkva.append(v.get(dd))
            print(checkva)
        if len(set(checkva)) > 1:
            continue
        allvarifinal.append(v)

    allinfos = []
    for v in allvarifinal:
        fuco = fu
        funame = ""
        ctypesargs = ""
        numpytypes = []
        forfunction = []
        for key, item in v.items():
            print(key, item)
            fuco = fuco.replace(key, item)
            funame += item.replace(" ", "_").strip("_") + "_"
            for k in d_typesall:
                if item == k.c:
                    print(item)
                    print(k.ct)
                    if k.ct != "ctypes.c_size_t":
                        ctypesargs += f"""ctypes.POINTER( {k.ct}),"""
                    else:
                        ctypesargs += f""" {k.ct},"""

                    numpytypes.append(k.np)
                    forfunction.append((k.ct, k.c, k.np, item))
        funame = funame.strip("_")
        completefunname = cfunctioname + "_" + funame
        fuco = fuco.replace("variable_for_function_creation", completefunname)
        argt = f"""
            ("{completefunname}",
            r'''{ctypesargs}''',
            "bb_",
            "aa_",
            None,
            [{ctypesargs}])
            """
        condidion = (
            "if "
            + " ".join(
                [
                    f"v{n}.dtype == {x[2]} and"
                    for n, x in enumerate(forfunction)
                    if x[0] != "ctypes.c_size_t"
                ]
            )[:-4]
            + ":"
        )
        ar = "".join([f"v{n}," for n, x in enumerate(numpytypes)])
        arpo = "".join([f"v{n}po," for n, x in enumerate(numpytypes)])
        completefunction_with_args = completefunname + f"({arpo})"
        convertstring = [
            f"""v{v}np=np.require(v{v}, {x[2]}, ["ALIGNED","C_CONTIGUOUS"])\n        v{v}po=v{v}np.ctypes.data_as(ctypes.POINTER({x[0]}))"""
            if x[0] != "ctypes.c_size_t"
            else f"""v{v}po=int(v{v})"""
            for v, x in enumerate(forfunction)
        ]
        convertstring = "\n".join([f"        {x}" for x in convertstring])
        print(completefunction_with_args)
        print(argt)
        print(fuco)
        allinfos.append(
            (
                funame,
                completefunname,
                fuco,
                argt,
                condidion,
                ar,
                completefunction_with_args,
                convertstring,
            )
        )

    allcfunctions = ""
    for a in allinfos:
        allcfunctions += (a[2]) + "\n"

    csource = cheader + "\n" + allcfunctions + "\n" + cfooter
    with open(cpath, mode="w", encoding="utf-8") as f:
        f.write(csource)

    allfuncvariations = []
    for a in allinfos:
        allfuncvariations.append(a[1])

    pythonheader = "import sys\nimport ctypes\nfrom numpy.ctypeslib import ndpointer\nimport configparser\nfrom flexible_partial import FlexiblePartialOwnName\nimport numpy as np\n\n"

    pythonfooter = rf"""
dllpath = r"{outputdll}"
cfgfile = r"{cfgfile}"
lib = ctypes.CDLL(dllpath)
confignew = configparser.ConfigParser()
confignew.read(cfgfile)
funcs = confignew.defaults()
c_functions = sys.modules[__name__]

def execute_function(f,*args, **kwargs): # create a function
    f(*args, **kwargs)

allfu = []
for (fname, descri, function_prefix, functionnormalprefix, restype, argtypes,) in allargtypes:
    fun = lib.__getattr__(funcs[fname])
    fun.restype = restype
    if len(argtypes) != 0:
        fun.argtypes = argtypes
    allfu.append((fname, fun))
    setattr(c_functions, f"{{functionnormalprefix}}{{fname}}", fun)
    setattr(c_functions, f"{{function_prefix}}{{fname}}", FlexiblePartialOwnName(execute_function, descri, True, fun), )


    """

    allargtype = "\nallargtypes = ["
    for a in allinfos:
        allargtype += (a[3]) + ","

    allargtype += "]"

    wholepyfun = f"\ndef {cfunctioname}({allinfos[0][5]}):\n\n"
    for a in allinfos:
        wholepyfun += "    " + a[4] + "\n"
        wholepyfun += "" + a[7] + "\n"
        wholepyfun += f'        c_functions.bb_{f"{a[6]}"}\n        return' + "\n"

    with open(pypath, mode="w", encoding="utf-8") as f:
        f.write(pythonheader + wholepyfun + allargtype + pythonfooter)

    return allfuncvariations, outputdll, cfgfile, cpath, pypath


class CreateCppDllv2:
    def __init__(
        self,
        modulename,
        cheader,
        cfooter,
        cfunctioname,
        var_variations,
        dtypemustbeequal,
        fu,
    ):
        (
            allfuncvariations,
            outputdll,
            cfgfile,
            cpath,
            pypath,
        ) = write_source_code_filesv2(
            modulename,
            var_variations,
            dtypemustbeequal,
            fu,
            cfunctioname,
            cheader,
            cfooter,
        )

        print("Files written:")
        print(TC(f"Python import file: {pypath}").bg_black.fg_lightgreen)
        print(TC(f"C++ file: {cpath}").bg_black.fg_lightgreen)
        print(TC("If you want/need, you can edit the code before compiling it."))
        self.outputdll = outputdll
        self.cfgfile = cfgfile
        self.cpath = cpath
        self.modulename = modulename
        self.allfuncvariations = allfuncvariations

    def compile_cpp_code(
        self,
        vcvarsall_bat=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
        cl_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\cl.exe",
        link_exe=r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx86\x64\link.exe",
        compilerflags=("/std:c++20", "/Ferelease", "/EHsc", "/MT", "/O2", "/bigobj"),
    ):
        compile_cpp_codev2(
            self.outputdll,
            self.cfgfile,
            self.cpath,
            self.modulename,
            vcvarsall_bat,
            cl_exe,
            link_exe,
            compilerflags,
            self.allfuncvariations,
        )


def create_function_variations(
    cfunctioname,
    cfunctionname_with_prefix,
    functionvariation1,
    functionvariation2,
    cfunction,
    argtypes,
    replacedict_argtypes,
    replacedict_c_code,
    ignored_dtypes1,
    ignored_dtypes2,
    ignored_dtypes3,
    samedtypes,
    printoutput=False,
):

    allresults = nested_dict()
    for dty3 in d_typesall:
        if (
            dty3.np in ignored_dtypes3
            or dty3.c in ignored_dtypes3
            or dty3.ct in ignored_dtypes3
        ):
            continue
        for dty2 in d_typesall:
            if (
                dty2.np in ignored_dtypes2
                or dty2.c in ignored_dtypes2
                or dty2.ct in ignored_dtypes2
            ):
                continue
            for dty in d_typesall:
                if (
                    dty.np in ignored_dtypes1
                    or dty.c in ignored_dtypes1
                    or dty.ct in ignored_dtypes1
                ):
                    continue
                if samedtypes:
                    chdi = {
                        "!C_DATA_DTYPE!": dty.c,
                        "!C_DATA_DTYPE2!": dty2.c,
                        "!C_DATA_DTYPE3!": dty3.c,
                    }
                    checkdu = []
                    for s in samedtypes:
                        checkdu.append(chdi[s])
                    if len(set(checkdu)) > 1:
                        continue

                ctdatatype = dty.ct.split(".")[-1]
                ctdatatype2 = dty2.ct.split(".")[-1]
                ctdatatype3 = dty3.ct.split(".")[-1]

                comment0 = (
                    f"// np={dty.np}, c={dty.c}, ctypes={dty.ct}, code={dty.code}".replace(
                        "\n", " "
                    ).replace(
                        "\r", " "
                    )
                    + f" ||| np={dty2.np}, c={dty2.c}, ctypes={dty2.ct}, code={dty2.code}".replace(
                        "\n", " "
                    ).replace(
                        "\r", " "
                    )
                    + f" ||| np={dty3.np}, c={dty3.c}, ctypes={dty3.ct}, code={dty3.code}".replace(
                        "\n", " "
                    ).replace(
                        "\r", " "
                    )
                )
                comment1 = (
                    f"// {dty.alias}".replace("\n", " ").replace("\r", " ")
                    + f" ||| {dty2.alias}".replace("\n", " ").replace("\r", " ")
                    + f" ||| {dty3.alias}".replace("\n", " ").replace("\r", " ")
                )
                comment2 = (
                    f"// {dty.comment}".replace("\n", " ").replace("\r", " ")
                    + f" ||| {dty2.comment}".replace("\n", " ").replace("\r", " ")
                    + f" ||| {dty3.comment}".replace("\n", " ").replace("\r", " ")
                )
                allcomments = f"{comment0}\n{comment1}\n{comment2}"
                allcommentsargs = f"{comment0[3:]}\n{comment1[3:]}\n{comment2[3:]}"
                allstdreplacementsdict = {
                    "!C_FUNCTION_NAME!": cfunctioname,
                    "!DTYPE_EXPLANATION!": allcommentsargs,
                    "!DTYPE_EXPLANATIONC!": allcomments,
                    "!C_DATA_DTYPE!": dty.c,
                    "!CT_DATA_DTYPE!": ctdatatype,
                    "!C_DATA_DTYPE2!": dty2.c,
                    "!CT_DATA_DTYPE2!": ctdatatype2,
                    "!C_DATA_DTYPE3!": dty3.c,
                    "!CT_DATA_DTYPE3!": ctdatatype3,
                    "!NP_DATA_DTYPE!": dty.np,
                    "!ALIAS_DATA_DTYPE!": dty.alias,
                }
                cfunctionname_with_prefixvar = cfunctionname_with_prefix
                cfunctionvar = cfunction

                argtypesvar = argtypes
                for key, item in allstdreplacementsdict.items():
                    argtypesvar = argtypesvar.replace(key, item)
                for key, item in replacedict_argtypes.items():
                    argtypesvar = argtypesvar.replace(key, item)
                for key, item in allstdreplacementsdict.items():
                    argtypesvar = argtypesvar.replace(key, item)

                functionvariation1var, functionvariation2var = (
                    functionvariation1,
                    functionvariation2,
                )
                for key, item in allstdreplacementsdict.items():
                    functionvariation1var = functionvariation1var.replace(key, item)
                    functionvariation2var = functionvariation2var.replace(key, item)
                    cfunctionname_with_prefixvar = cfunctionname_with_prefixvar.replace(
                        key, item
                    )
                    cfunctionvar = cfunctionvar.replace(key, item)

                for key, item in allstdreplacementsdict.items():
                    functionvariation1var = functionvariation1var.replace(key, item)
                    functionvariation2var = functionvariation2var.replace(key, item)
                    cfunctionname_with_prefixvar = cfunctionname_with_prefixvar.replace(
                        key, item
                    )
                    cfunctionvar = cfunctionvar.replace(key, item)

                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["np"] = dty.np
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["c"] = dty.c
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["ct"] = dty.ct
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["use"] = True
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["comment"] = dty.comment
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["code"] = dty.code
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["alias"] = dty.alias
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["argtypes"] = argtypesvar
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["cfunction"] = cfunctionvar
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["functionvariation1"] = functionvariation1var
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["functionvariation2"] = functionvariation2var
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["cfunctionname_with_prefix"] = cfunctionname_with_prefixvar

                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["np2"] = dty2.np
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["c2"] = dty2.c
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["ct2"] = dty2.ct
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["comment2"] = dty2.comment
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["code2"] = dty2.code
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["alias2"] = dty2.alias

                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["np3"] = dty3.np
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["c3"] = dty3.c
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["ct3"] = dty3.ct
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["comment3"] = dty3.comment
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["code3"] = dty3.code
                allresults[
                    f"{dty.np}XXX{dty2.np}XXX{dty3.np}{dty.ct}XXX{dty2.ct}XXX{dty3.ct}{dty.c}XXX{dty2.c}XXX{dty3.c}"
                ]["alias3"] = dty3.alias

                if printoutput:
                    print(argtypesvar)
                    print(cfunctionvar)
                    print("----------------------------------")
    return allresults


def write_argtypes_import(cpydict, pythonheader, pythonfooter, path, printout=True):

    allargtypes = "["

    for key, item in cpydict.items():
        allargtypes += f"""{item['argtypes']},\n\n"""
    allargtypes += "]"
    wholepyfile = f"{pythonheader}\n\nallargtypes={allargtypes}\n\n{pythonfooter}"
    if printout:
        print(wholepyfile)
    if path:
        touch(path)
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(wholepyfile)
    return wholepyfile


def write_ccode(cpydict, cheader, cfooter, path, printout=True):
    allargtypes = ""
    for key, item in cpydict.items():
        allargtypes += f"""{item['cfunction']}\n\n"""

    wholecfile = f"{cheader}\n\n{allargtypes}\n\n{cfooter}"
    if printout:
        print(wholecfile)
    if path:
        touch(path)
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(wholecfile)
    return wholecfile


def get_file(f):
    return os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), f))


def get_file_own_folder(f, folder):
    return os.path.normpath(os.path.join(folder, f))


def compile_cpp(
    modulename,
    fnames,
    vcvarsall_bat,
    cl_exe,
    link_exe,
    cppsource,
    compilerflags=(
        "/std:c++17",
        "/Ferelease",
        "/EHsc",
        "/MT",
        "/O2",
        "/bigobj",
    ),
):

    cfgfile = get_file(f"{modulename}.ini")
    output = get_file(f"{modulename}.dll")

    config = configparser.ConfigParser()
    allcommand = [
        vcvarsall_bat,
        "x64",
        "&&",
        cl_exe,
        "/D_USRDL",
        "/D_WINDLL",
        cppsource,
        *compilerflags,
        "/link",
        "/DLL",
        f'/OUT:"{output}"',
        "/MACHINE:X64",
    ]
    subprocess.run(allcommand, shell=True)

    p = subprocess.run([link_exe, "/dump", "/exports", output], capture_output=True)
    fnamesre = [
        (
            x,
            re.compile(
                rf"[\r\n]+\s+[a-fA-F0-9]+\s+[a-fA-F0-9]+\s+[a-fA-F0-9]+\s+(\?[^\s]*{x}@[^\s]+)"
            ),
        )
        for x in fnames
    ]
    decor = p.stdout.decode("utf-8", "ignore")
    print(decor)
    franmesre = [(x[0], x[1].findall(decor)) for x in fnamesre]
    config["DEFAULT"] = {k: v[0] for k, v in franmesre if v}
    with open(cfgfile, "w") as f:
        config.write(f)


def try_delete_file(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            return True
        except Exception:
            return False
    return True


class CreateCppDll:
    def __init__(
        self,
        cfunctioname,
        cfunction,
        samedtypes,
        modulename,
        variable_for_function_creation=(
            r"!CT_DATA_DTYPE!_!CT_DATA_DTYPE2!_!C_FUNCTION_NAME!_!CT_DATA_DTYPE3!"
        ),
        cheader="""
    #include <iostream>
    #include <stdio.h>
    #include <algorithm>  
    #include <vector>     
    #include <functional> 
    #include <conio.h>
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
    ):
        (
            self.cfunctioname,
            self.cfunction,
            self.modulename,
            self.variable_for_function_creation,
            self.cheader,
            self.cfooter,
            self.ignored_dtypes1,
            self.ignored_dtypes2,
            self.ignored_dtypes3,
            self.vcvarsall_bat,
            self.cl_exe,
            self.link_exe,
            self.compilerflags,
            self.samedtypes,
        ) = (
            cfunctioname,
            cfunction,
            modulename,
            variable_for_function_creation,
            cheader,
            cfooter,
            ignored_dtypes1,
            ignored_dtypes2,
            ignored_dtypes3,
            vcvarsall_bat,
            cl_exe,
            link_exe,
            compilerflags,
            samedtypes,
        )
        self.functionvariation1 = f"""aa_{variable_for_function_creation}"""

        self.functionvariation2 = f"""bb_{variable_for_function_creation}"""
        self.argtypes = f"""
        ("{variable_for_function_creation}",
        '''!DTYPE_EXPLANATION!''',
        "bb_",
        "aa_",
        None,
        [ctypes.POINTER( ctypes.!CT_DATA_DTYPE!),
        ctypes.c_size_t,
        ctypes.POINTER( ctypes.!CT_DATA_DTYPE2!),
        ctypes.POINTER( ctypes.!CT_DATA_DTYPE3!),])
        """
        self.cfunctionname_with_prefix = f"""{variable_for_function_creation}"""

        self.cpydict = create_function_variations(
            cfunctioname,
            self.cfunctionname_with_prefix,
            self.functionvariation1,
            self.functionvariation2,
            cfunction,
            self.argtypes,
            replacedict_argtypes={},
            replacedict_c_code={},
            ignored_dtypes1=ignored_dtypes1,
            ignored_dtypes2=ignored_dtypes2,
            ignored_dtypes3=ignored_dtypes3,
            samedtypes=self.samedtypes,
        )
        self.allfunctionvariations = [
            x[1]["cfunctionname_with_prefix"] for x in self.cpydict.items()
        ]
        self.cfgfile = get_file(f"{modulename}.ini")
        self.outputdll = get_file(f"{modulename}.dll")
        self.pythonheader = "import sys\nimport ctypes\nfrom numpy.ctypeslib import ndpointer\nimport configparser\nfrom flexible_partial import FlexiblePartialOwnName\nimport numpy as np\n\n"
        self.pythonfooter = rf"""




dllpath = r"{self.outputdll}"
cfgfile = r"{self.cfgfile}"
lib = ctypes.CDLL(dllpath)
confignew = configparser.ConfigParser()
confignew.read(cfgfile)
funcs = confignew.defaults()
c_functions = sys.modules[__name__]

def execute_function(f,*args, **kwargs):
    f(*args, **kwargs)


allfu = []
for (fname, descri, function_prefix, functionnormalprefix, restype, argtypes,) in allargtypes:
    fun = lib.__getattr__(funcs[fname])
    fun.restype = restype
    if len(argtypes) != 0:
        fun.argtypes = argtypes
    allfu.append((fname, fun))
    setattr(c_functions, f"{{functionnormalprefix}}{{fname}}", fun)
    setattr(c_functions, f"{{function_prefix}}{{fname}}", FlexiblePartialOwnName(execute_function, descri, True, fun), )


        """

        self.wholefunction = (
            f"""def {self.cfunctioname}(inputarray1np,inputarray2np,outputdtype):\n\n"""
        )
        co = 0
        ifword = "if"
        for key, item in self.cpydict.items():
            checkdty = f"""
            {ifword} (inputarray1np.dtype == {item['np']}
            and inputarray2np.dtype == {item['np2']}
            and outputdtype == {item['np3']}):
                inputarray1_dtype_np = {item['np']}
                inputarray2_dtype_np = {item['np2']}
                outputarray_dtype_np = {item['np3']}
                inputarray1_dtype_ct = {item['ct']}
                inputarray2_dtype_ct = {item['ct2']}
                outputarray_dtype_ct = {item['ct3']}
                execfunc = c_functions.{item['functionvariation2']}
            """
            co += 1
            if co > 0:
                ifword = "elif"
            self.wholefunction += f"\n{checkdty}\n\n"

        self.subsdict = self.cpydict[
            sorted([(x.count("double"), x) for x in self.cpydict])[-1][1]
        ]

        self.wholefunction += f"""
            else: 
                inputarray1_dtype_np = {self.subsdict['np']}
                inputarray2_dtype_np = {self.subsdict['np2']}
                outputarray_dtype_np = {self.subsdict['np3']}
                inputarray1_dtype_ct = {self.subsdict['ct']}
                inputarray2_dtype_ct = {self.subsdict['ct2']}
                outputarray_dtype_ct = {self.subsdict['ct3']}
                execfunc = c_functions.{self.subsdict['functionvariation2']}
            outputarraynp = np.zeros(inputarray1np.shape,dtype=outputarray_dtype_np)
            inputarray1np = np.require(inputarray1np, inputarray1_dtype_np, ['ALIGNED',"C_CONTIGUOUS"])
            inputarray1ct = inputarray1np.ctypes.data_as(ctypes.POINTER(inputarray1_dtype_ct))
            inputarray2np = np.require(inputarray2np, inputarray2_dtype_np, ['ALIGNED',"C_CONTIGUOUS"])
            inputarray2ct = inputarray2np.ctypes.data_as(ctypes.POINTER(inputarray2_dtype_ct))
            outputarraynp = np.require(outputarraynp, outputarray_dtype_np, ['ALIGNED', 'WRITEABLE',"C_CONTIGUOUS"])
            outputarrayct = outputarraynp.ctypes.data_as(ctypes.POINTER(outputarray_dtype_ct))
            execfunc(inputarray1ct,inputarray1np.size,inputarray2ct,outputarrayct)
            return outputarrayct._arr
        """
        self.pythonfooter = self.pythonfooter + "\n\n" + self.wholefunction
        self.pypath = get_file(f"{self.modulename}module.py")

        self.pyfile = write_argtypes_import(
            self.cpydict, self.pythonheader, self.pythonfooter, self.pypath
        )
        ####################

        ###################################################

        self.cpath = get_file(f"{self.modulename}_cppcode.cpp")

        self.cfile = write_ccode(
            self.cpydict, self.cheader, self.cfooter, self.cpath, printout=True
        )
        print(TC(f"Python import file: {self.pypath}").bg_black.fg_lightgreen)
        print(TC(f"C++ file: {self.cpath}").bg_black.fg_lightgreen)

    def compile_cpp_code(self):
        try_delete_file(self.outputdll)
        try_delete_file(self.cfgfile)
        try_delete_file(self.outputdll[:-3] + "exp")
        try_delete_file(self.outputdll[:-3] + "lib")
        try_delete_file(self.cpath[-3] + "obj")
        compile_cpp(
            modulename=self.modulename,
            fnames=self.allfunctionvariations,
            vcvarsall_bat=self.vcvarsall_bat,
            cl_exe=self.cl_exe,
            link_exe=self.link_exe,
            cppsource=self.cpath,
            compilerflags=self.compilerflags,
        )
        print(
            TC(
                f"""Config file for functions: {self.cfgfile}\nC++ dll file: {self.outputdll}"""
            ).bg_black.fg_lightcyan
        )
        sleep(3)
        try_delete_file(self.cpath[-3] + "obj")
