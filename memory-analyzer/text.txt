#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define VL (Value *)malloc(sizeof(Value))

typedef struct Value
{
    int val;
    struct Value *next;
} Value;

typedef struct 
{
    Value *start, *end, *current;
} ARRAY;

int testArray(ARRAY *arr)
{
    return arr->current != NULL;
}

void initArray(ARRAY *arr)
{
    arr->start = NULL;
    arr->end = NULL;
    arr->current = NULL;
}

void freeArray(ARRAY *arr)
{
    if (arr == NULL) return;
    
    Value *current = arr->start;
    while (current != NULL)
    {
        Value *next = current->next;
        free(current);
        current = next;
    }
    arr->start = NULL;
    arr->end = NULL;
    arr->current = NULL;
}

void putArray(ARRAY *arr, int val)
{
    Value *newValue = VL;
    newValue->val = val;
    newValue->next = NULL;

    if (arr->start == NULL)
    {
        arr->start = newValue;
        arr->end = newValue;
        arr->current = newValue;
    }
    else
    {
        arr->end->next = newValue;
        arr->end = newValue;
    }
}

void printArray(ARRAY *arr)
{
    Value *current = arr->start;
    while (current != NULL)
    {
        printf("%d ", current->val);
        current = current->next;
    }
    printf("\n");
}

void resetArray(ARRAY *arr)
{
    arr->current = arr->start;
}

void nextArray(ARRAY *arr)
{
    if (arr->current != NULL)
    {
        arr->current = arr->current->next;
    }
}

int getArraySize(ARRAY *arr)
{
    int size = 0;
    Value *temp = arr->start;
    while (temp != NULL)
    {
        size++;
        temp = temp->next;
    }
    return size;
}

void setValueAtPosition(ARRAY *arr, int position, int value)
{
    // Check if position exceeds maximum allowed size
    if (position >= 5)
    {
        printf("Error: Position %d exceeds maximum array size (5)\n", position);
        return;
    }
    
    // Check if value exceeds maximum allowed value
    if (value > 20)
    {
        printf("Error: Value %d exceeds maximum allowed value (20)\n", value);
        return;
    }
    
    // Ensure we have enough elements in the array
    int currentSize = getArraySize(arr);
    
    // Add elements if position is beyond current size
    while (currentSize <= position)
    {
        putArray(arr, 0); // Initialize with 0
        currentSize++;
    }
    
    // Navigate to the specified position and set the value
    Value *temp = arr->start;
    for (int i = 0; i < position && temp != NULL; i++)
    {
        temp = temp->next;
    }
    
    if (temp != NULL)
    {
        temp->val = value;
    }
}

void fillArrayToSize(ARRAY *arr, int targetSize)
{
    if (targetSize > 5) 
    {
        targetSize = 5; // Cap at maximum size
    }
    
    int currentSize = getArraySize(arr);
    while (currentSize < targetSize)
    {
        putArray(arr, 0);
        currentSize = getArraySize(arr); // Recalculate size to avoid infinite loop
        
        // Safety check to prevent infinite loop
        if (currentSize >= 5) 
        {
            break;
        }
    }
}

void printArrayWithPositions(ARRAY *arr)
{
    Value *current = arr->start;
    int position = 0;
    
    printf("Array contents:\n");
    while (current != NULL)
    {
        printf("Position %d: %d\n", position, current->val);
        current = current->next;
        position++;
    }
    printf("\n");
}

int calculateSum(ARRAY *arr)
{
    int sum = 0;
    Value *current = arr->start;
    
    while (current != NULL)
    {
        sum += current->val;
        current = current->next;
    }
    
    return sum;
}

void printArraySum(ARRAY *arr)
{
    int sum = calculateSum(arr);
    printf("Sum of all numbers in the array: %d\n", sum);
}

int main(int argc, char const *argv[])
{
    ARRAY myArray;
    initArray(&myArray);
    
    char input[100];
    int position, value;
    
    printf("Enter commands in format 'position X value Y' or 'quit' to exit:\n");
    
    while (1)
    {
        printf("> ");
        if (fgets(input, sizeof(input), stdin) == NULL)
        {
            break;
        }
        
        // Check if user wants to quit
        if (strncmp(input, "quit", 4) == 0)
        {
            break;
        }
        
        // Parse input: "position X value Y"
        if (sscanf(input, "position %d value %d", &position, &value) == 2)
        {
            if (position < 0)
            {
                printf("Error: Position must be non-negative\n");
                continue;
            }
            
            setValueAtPosition(&myArray, position, value);
            printf("Set position %d to value %d\n", position, value);
            printArrayWithPositions(&myArray);
            printArraySum(&myArray);
        }
        else
        {
            printf("Invalid format. Use: position X value Y\n");
            printf("Example: position 2 value 3\n");
        }
    }
    
    // Fill array to 5 positions with zeros before exiting
    printf("\nFilling array to 5 positions with zeros...\n");
    fillArrayToSize(&myArray, 5);
    printf("Final array (filled to 5 positions):\n");
    printArrayWithPositions(&myArray);
    printArraySum(&myArray);

    freeArray(&myArray);
    return 0;
}
