#include "malloc.h"
#include <stdlib.h>
#include <sys/mman.h>

typedef struct mem_block
{
    size_t size;
    int free;
    struct mem_block* next;
} m_block;

static m_block* heap = NULL;

m_block* find_free_block(m_block** last, size_t size)
{
    m_block* current = heap;
    *last = NULL;
    while (current)
    {
        if (current->free && current->size >= size)
        {
            return current;
        }
        *last = current;
        current = current->next;
    }
    return NULL;
}

m_block* request_block(m_block* last, size_t size)
{
    m_block* block =
        mmap(NULL, sizeof(m_block) + size, PROT_READ | PROT_WRITE,
             MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (block == MAP_FAILED)
        return NULL;

    block->size = size;
    block->free = 0;
    block->next = NULL;

    if (last)
        last->next = block;

    return block;
}

void* m_malloc(size_t size)
{
    if (size <= 0)
        return NULL;

    m_block* block;
    if (!heap)
    {
        block = request_block(NULL, size);
        if (!block)
            return NULL;
        heap = block;
    }
    else
    {
        m_block* last = NULL;
        block = find_free_block(&last, size);
        if (!block)
        {
            block = request_block(last, size);
            if (!block)
                return NULL;
        }
        else
        {
            block->free = 0;
        }
    }

    return (void*)(block + 1);
}

int m_free(void* ptr)
{
    if (!ptr)
        return -1;
    m_block* block = (m_block*)ptr - 1;
    block->free = 1;
    return 0;
}
