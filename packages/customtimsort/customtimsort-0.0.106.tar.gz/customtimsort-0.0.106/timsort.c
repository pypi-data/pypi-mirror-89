#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <string.h>
//#include <timsort/llistobject.h>

#define ISLT(X, Y) (*(ms->key_compare))(X, Y, ms)
/* Compare X to Y via "<".  Goto "fail" if the comparison raises an
   error.  Else "k" is set to true iff X<Y, and an "if (k)" block is
   started.  It makes more sense in context <wink>.  X and Y are PyObject*s.
*/
#define IFLT(X, Y) if ((k = ISLT(X, Y)) < 0) goto fail;  \
           if (k)


static PyObject *
llist_sort_impl(PyListObject *self, PyObject *keyfunc, int reverse, Py_ssize_t minrun)
/*[clinic end generated code: output=57b9f9c5e23fbe42 input=cb56cd179a713060]*/
{
    MergeState ms;
    Py_ssize_t nremaining;
    sortslice lo;
    Py_ssize_t saved_ob_size, saved_allocated;
    PyObject **saved_ob_item;
    PyObject **final_ob_item;
    PyObject *result = NULL;            /* guilty until proved innocent */
    Py_ssize_t i;
    PyObject **keys;
    assert(self != NULL);
    assert(PyList_Check(self));
    if (keyfunc == Py_None)
        keyfunc = NULL;

    /* The list is temporarily made empty, so that mutations performed
     * by comparison functions can't affect the slice of memory we're
     * sorting (allowing mutations during sorting is a core-dump
     * factory, since ob_item may change).
     */

    saved_ob_item = self->ob_item;
    saved_allocated = self->allocated;
    saved_ob_size = Py_SIZE(self);
    Py_SIZE(self) = 0;
    self->ob_item = NULL;
    self->allocated = -1; /* any operation will reset it to >= 0 */

    if (keyfunc == NULL) {
        keys = NULL;
        lo.keys = saved_ob_item;
        lo.values = NULL;
    }
    else {
        if (saved_ob_size < MERGESTATE_TEMP_SIZE/2)
            /* Leverage stack space we allocated but won't otherwise use */
            keys = &ms.temparray[saved_ob_size+1];
        else {
            keys = PyMem_MALLOC(sizeof(PyObject *) * saved_ob_size);
            if (keys == NULL) {
                PyErr_NoMemory();
                goto keyfunc_fail;
            }
        }

        for (i = 0; i < saved_ob_size ; i++) {
            keys[i] = PyObject_CallFunctionObjArgs(keyfunc, saved_ob_item[i],
                                                   NULL);
            if (keys[i] == NULL) {
                for (i=i-1 ; i>=0 ; i--)
                    Py_DECREF(keys[i]);
                if (saved_ob_size >= MERGESTATE_TEMP_SIZE/2)
                    PyMem_FREE(keys);
                goto keyfunc_fail;
            }
        }

        lo.keys = keys;
        lo.values = saved_ob_item;
    }

    /* The pre-sort check: here's where we decide which compare function to use.
     * How much optimization is safe? We test for homogeneity with respect to
     * several properties that are expensive to check at compare-time, and
     * set ms appropriately. */
    if (saved_ob_size > 1) {
        /* Assume the first element is representative of the whole list. */
        int keys_are_in_tuples = (lo.keys[0]->ob_type == &PyTuple_Type &&
                                  Py_SIZE(lo.keys[0]) > 0);

        PyTypeObject* key_type = (keys_are_in_tuples ?
                                  PyTuple_GET_ITEM(lo.keys[0], 0)->ob_type :
                                  lo.keys[0]->ob_type);

        int keys_are_all_same_type = 1;
        int strings_are_latin = 1;
        int ints_are_bounded = 1;

        /* Prove that assumption by checking every key. */
        for (i=0; i < saved_ob_size; i++) {

            if (keys_are_in_tuples &&
                !(lo.keys[i]->ob_type == &PyTuple_Type && Py_SIZE(lo.keys[i]) != 0)) {
                keys_are_in_tuples = 0;
                keys_are_all_same_type = 0;
                break;
            }

            /* Note: for lists of tuples, key is the first element of the tuple
             * lo.keys[i], not lo.keys[i] itself! We verify type-homogeneity
             * for lists of tuples in the if-statement directly above. */
            PyObject *key = (keys_are_in_tuples ?
                             PyTuple_GET_ITEM(lo.keys[i], 0) :
                             lo.keys[i]);

            if (key->ob_type != key_type) {
                keys_are_all_same_type = 0;
                /* If keys are in tuple we must loop over the whole list to make
                   sure all items are tuples */
                if (!keys_are_in_tuples) {
                    break;
                }
            }

            if (keys_are_all_same_type) {
                if (key_type == &PyLong_Type &&
                    ints_are_bounded &&
                    Py_ABS(Py_SIZE(key)) > 1) {

                    ints_are_bounded = 0;
                }
                else if (key_type == &PyUnicode_Type &&
                         strings_are_latin &&
                         PyUnicode_KIND(key) != PyUnicode_1BYTE_KIND) {

                        strings_are_latin = 0;
                    }
                }
            }

        /* Choose the best compare, given what we now know about the keys. */
        if (keys_are_all_same_type) {

            if (key_type == &PyUnicode_Type && strings_are_latin) {
                ms.key_compare = unsafe_latin_compare;
            }
            else if (key_type == &PyLong_Type && ints_are_bounded) {
                ms.key_compare = unsafe_long_compare;
            }
            else if (key_type == &PyFloat_Type) {
                ms.key_compare = unsafe_float_compare;
            }
            else if ((ms.key_richcompare = key_type->tp_richcompare) != NULL) {
                ms.key_compare = unsafe_object_compare;
            }
            else {
                ms.key_compare = safe_object_compare;
            }
        }
        else {
            ms.key_compare = safe_object_compare;
        }

        if (keys_are_in_tuples) {
            /* Make sure we're not dealing with tuples of tuples
             * (remember: here, key_type refers list [key[0] for key in keys]) */
            if (key_type == &PyTuple_Type) {
                ms.tuple_elem_compare = safe_object_compare;
            }
            else {
                ms.tuple_elem_compare = ms.key_compare;
            }

            ms.key_compare = unsafe_tuple_compare;
        }
    }
    /* End of pre-sort check: ms is now set properly! */

    merge_init(&ms, saved_ob_size, keys != NULL);

    nremaining = saved_ob_size;
    if (nremaining < 2)
        goto succeed;

    /* Reverse sort stability achieved by initially reversing the list,
    applying a stable forward sort, then reversing the final result. */
    if (reverse) {
        if (keys != NULL)
            reverse_slice(&keys[0], &keys[saved_ob_size]);
        reverse_slice(&saved_ob_item[0], &saved_ob_item[saved_ob_size]);
    }

    /* March over the array once, left to right, finding natural runs,
     * and extending short natural runs to minrun elements.
     */
    do {
        int descending;
        Py_ssize_t n;

        /* Identify next run. */
        n = count_run(&ms, lo.keys, lo.keys + nremaining, &descending);
        if (n < 0)
            goto fail;
        if (descending)
            reverse_sortslice(&lo, n);
        /* If short, extend to min(minrun, nremaining). */
        if (n < minrun) {
            const Py_ssize_t force = nremaining <= minrun ?
                              nremaining : minrun;
            if (binarysort(&ms, lo, lo.keys + force, lo.keys + n) < 0)
                goto fail;

            n = force;
        }
        /* Push run onto pending-runs stack, and maybe merge. */
        assert(ms.n < MAX_MERGE_PENDING);
        ms.pending[ms.n].base = lo;
        ms.pending[ms.n].len = n;
        ++ms.n;
        if (merge_collapse(&ms) < 0)
            goto fail;
        /* Advance to find next run. */
        sortslice_advance(&lo, n);
        nremaining -= n;
    } while (nremaining);

    if (merge_force_collapse(&ms) < 0)
        goto fail;
    assert(ms.n == 1);
    assert(keys == NULL
           ? ms.pending[0].base.keys == saved_ob_item
           : ms.pending[0].base.keys == &keys[0]);
    assert(ms.pending[0].len == saved_ob_size);
    lo = ms.pending[0].base;

succeed:
    result = Py_None;
fail:
    if (keys != NULL) {
        for (i = 0; i < saved_ob_size; i++)
            Py_DECREF(keys[i]);
        if (saved_ob_size >= MERGESTATE_TEMP_SIZE/2)
            PyMem_FREE(keys);
    }

    if (self->allocated != -1 && result != NULL) {
        /* The user mucked with the list during the sort,
         * and we don't already have another error to report.
         */
        PyErr_SetString(PyExc_ValueError, "list modified during sort");
        result = NULL;
    }

    if (reverse && saved_ob_size > 1)
        reverse_slice(saved_ob_item, saved_ob_item + saved_ob_size);

    merge_freemem(&ms);

keyfunc_fail:
    final_ob_item = self->ob_item;
    i = Py_SIZE(self);
    Py_SIZE(self) = saved_ob_size;
    self->ob_item = saved_ob_item;
    self->allocated = saved_allocated;
    if (final_ob_item != NULL) {
        /* we cannot use _list_clear() for this because it does not
           guarantee that the list is really empty when it returns */
        while (--i >= 0) {
            Py_XDECREF(final_ob_item[i]);
        }
        PyMem_FREE(final_ob_item);
    }
    Py_XINCREF(result);
    return self;
}
#undef IFLT
#undef ISLT

void
lPyList_Sort(PyObject *self, Py_ssize_t minrun) {
    self = llist_sort_impl((PyListObject *)self, NULL, 0, minrun);
}











int Get_minrun(char path[], int size_of_array)
{
    char line[30] = {0};
    int line_count = -3;

    FILE *file = fopen(path, "r");

    int first_size = 0, step = 1;
    int minrun = 2;
    while (fgets(line, 30, file))
    {
        if (line_count == -3) {
            first_size = atoi(line);
        } else if (line_count == -2) {
            step = atoi(line);
        } else if (line_count >= 0 && first_size + line_count * step == size_of_array) {
            minrun = atoi(line);
        }
        line_count++;
    }
    fclose(file);
    return minrun;
}

static PyObject *
timsort(PyObject *self, PyObject *args)
{
    PyObject * arr;
    Py_ssize_t minrun;
    if (!PyArg_ParseTuple(args, "nO", &minrun, &arr))
        return NULL;
    lPyList_Sort(arr, minrun);
    return PyLong_FromLong(1);
}

static PyMethodDef TimSortMethods[] = {
    {"timsort",  timsort, METH_VARARGS,
     "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef timsortmodule = {
    PyModuleDef_HEAD_INIT,
    "timsort",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    TimSortMethods
};

PyMODINIT_FUNC
PyInit_timsort(void)
{
    return PyModule_Create(&timsortmodule);
}

