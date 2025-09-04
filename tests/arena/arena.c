#include "arena.h"
#include "../malloc/malloc.h"
#include <stdalign.h>
#include <stddef.h>
#include <string.h>

void arena_init(arena_t* arena, size_t block_size)
{
    arena->head = NULL;
    arena->block_size = block_size;
}

static arena_block_t* arena_add_block(arena_t* arena, size_t size)
{
    size_t alloc_size =
        (size > arena->block_size) ? size : arena->block_size;

    arena_block_t* block = m_malloc(sizeof(arena_block_t));
    if (block == NULL)
        return NULL;

    block->start = m_malloc(alloc_size);
    if (block->start == NULL)
        return NULL;

    block->size = alloc_size;
    block->offset = 0;
    block->next = NULL;

    if (arena->head == NULL)
    {
        arena->head = block;
    }
    else
    {
        arena_block_t* last = arena->head;
        while (last->next != NULL)
            last = last->next;
        last->next = block;
    }

    return block;
}

void* arena_alloc(arena_t* arena, size_t size)
{
    if (arena->head == NULL)
    {
        if (arena_add_block(arena, size) == NULL)
            return NULL;
    }

    arena_block_t* block = arena->head;
    while (block != NULL)
    {
        if (block->offset + size <= block->size)
        {
            void* ptr = (char*)block->start + block->offset;
            block->offset += size;
            return ptr;
        }
        if (block->next == NULL)
            break;
        block = block->next;
    }

    block = arena_add_block(arena, size);
    if (block == NULL)
        return NULL;
    block->offset = size;
    return block->start;
}

void arena_reset(arena_t* arena)
{
    for (arena_block_t* block = arena->head; block != NULL;
         block = block->next)
    {
        block->offset = 0;
    }
}

void arena_free(arena_t* arena)
{
    arena_block_t* block = arena->head;
    while (block != NULL)
    {
        arena_block_t* next = block->next;
        m_free(block->start);
        m_free(block);
        block = next;
    }
    arena->head = NULL;
}
