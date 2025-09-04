#pragma once

#include <stddef.h>

// A chunk of memory.
typedef struct arena_block
{
    void* start;              // where the block starts
    size_t size;              // total bytes in this block
    size_t offset;            // how much we've used
    struct arena_block* next; // next block if this one fills
} arena_block_t;

// allocator struct.
typedef struct
{
    arena_block_t* head; // first block
    size_t block_size;   // default size for new blocks
} arena_t;

//
// `arena`: the allocator (&pointer).
// `block_size`: the default size for new blocks in bytes.
//
void arena_init(arena_t* arena, size_t block_size);

// allocate a block of memory.
void* arena_alloc(arena_t* arena, size_t size);

// reset the allocator, wipes everything but memory.
void arena_reset(arena_t* arena);

// Free everything, allocator is no longer usable.
void arena_free(arena_t* arena);
