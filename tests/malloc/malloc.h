#pragma once
#include <stddef.h>

//
// allocate a chunk of memory:
//
// `size`: how many bytes you want.
// return: a pointer to usable memory.
//
void* m_malloc(size_t size);

//
// free a chunk of memory previously allocated by m_malloc:
//
// `ptr`: must be a pointer returned by m_malloc.
// return: 0 on success, error code if failed.
//
int m_free(void* ptr);
