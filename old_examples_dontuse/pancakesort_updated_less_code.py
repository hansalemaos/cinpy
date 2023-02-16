# Less C-code:
# void cfun_pancakesort(size_t size,  int  *outdatav ) 
# {
#     pancakeSort(outdatav, size);
# }

import ctypes
import os
from numpy.ctypeslib import ndpointer
import cinpy

whole_c_code = r"""// Sorting of array list using pancake sort
#include <stdio.h>
#include <stdlib.h>

/* Reverses the array */
void flip(int arr[], int i)
{
    int temp, start = 0;

    while (start < i)
    {
        temp = arr[start];
        arr[start] = arr[i];
        arr[i] = temp;
        start++;
        i--;
    }
}

// Returns index of the maximum element in arr[0..n-1]
int findMax(int arr[], int n)
{
    int maxElementIdx, i;

    for (maxElementIdx = 0, i = 0; i < n; ++i)
        if (arr[i] > arr[maxElementIdx])
            maxElementIdx = i;

    return maxElementIdx;
}

// Sorts the array using flip operations
void pancakeSort(int *arr, int n)
{
    // Start from the complete array and one by one reduce current size by one
    for (int curr_size = n; curr_size > 1; --curr_size)
    {
        // Find index of the maximum element in arr[0..curr_size-1]
        int maxElementIdx = findMax(arr, curr_size);

        // Move the maximum element to end of current array if it's not already
        // at the end
        if (maxElementIdx != curr_size - 1)
        {
            // To move at the end, first move maximum number to beginning
            flip(arr, maxElementIdx);

            // Now move the maximum number to end by reversing current array
            flip(arr, curr_size - 1);
        }
    }
}

// Displays the array, passed to this method
void display(int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }

    printf("\n");
}
void cfun_pancakesort(size_t size,  int  *outdatav ) 
{
    pancakeSort(outdatav, size);
}
#define N 50

// Driver program to test above function
int main()
{
    int arr[N];
    for (int i = 0; i < N; i++)
        arr[i] = rand() % (N << 1); /* random numbers from 0 to 2N */

    printf("Original array: ");
    display(arr, N);

    pancakeSort(arr, N);
    printf("Sorted array: ");
    display(arr, N);

    return 0;
}
""" # complete C-code

all_functions = [
    (
        "cfun_pancakesort", # name of the function in the C code
        r"""pcakgesort""",
        "aa_",
        "bb_",
        None,
        [
            #ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
            ctypes.c_size_t,
            ndpointer(ctypes.c_int, flags="aligned,C_CONTIGUOUS,writeable"),         ],
    ),
]
modulename = "pcakesort" # name of the module - whatever you want
savefolder = "f:\\pcakesortctest" # where do you want to save the shared library?
sofile = f"{savefolder}\\pcakesortc.so" # the path of the shared library once it is compiled
if not os.path.exists(sofile): # if sofile doesn't exist, we start the compiler, gcc from  ....\MinGW\bin is used
    sofile = cinpy.compile_c_code(
        gcc_exe="gcc.exe", c_code=whole_c_code, modulename=modulename, folder=savefolder
    )
cinpy.loadlib(sofile, all_functions) # now we load the function



import numpy as np

#indata = np.random.randint(1, 20 + 1, size=10000)
#indata = indata.astype(np.int32)
#outdata = cinpy.bb_cfun_pancakesort(indata)

# outdata
# Out[3]: array([ 1,  1,  1, ..., 20, 20, 20])
# indata
# Out[4]: array([ 2, 20,  4, ..., 19, 17, 15])


def pancake_c(arraysize=20000):
    indata, _ = getnparray_and_list(arraysize=arraysize)
    outdata=indata.copy()
    outdata=np.require(outdata, np.int32, ['ALIGNED','C_CONTIGUOUS','writeable'])
    cinpy.bb_cfun_pancakesort(indata.size,outdata)
    return outdata


def getnparray_and_list(arraysize=20000):
    indata = np.random.randint(1, 1000, size=arraysize).astype(np.int32)
    return indata, indata.tolist()  # Let's return both -> equal conditions

outc = pancake_c(arraysize=10000)