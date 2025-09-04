#include <stdio.h>
#include <string.h>
#include "output.h"
int main() {
    arena_t arena;
    arena_init(&arena, 1024);
    void* ptr = arena_alloc(&arena, 1024);
    printf("ptr: %p\n", ptr);
	strcpy(ptr, "hello world");
    printf("ptr: %s\n", (char*)ptr);
    arena_free(&arena);
    return 0;
}
