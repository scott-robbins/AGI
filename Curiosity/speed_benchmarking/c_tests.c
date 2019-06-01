#include <stdio.h>
#include <time.h>

void main(int argc, char **argv){
    if (argc < 2){
        printf("Usage: ./test_c <size>\n");
        exit(0);
    } else{
        clock_t start = clock();

        int size;
        sscanf (argv[1],"%d",&size);
        printf("Using size: %d\n", size);

        int result = 0;
        for (int i=0;i<size;i++){
            result = result + i;
        }
        clock_t end = clock();
        double dt = (double)(end - start) / CLOCKS_PER_SEC;
        printf("Result: %d\t Time Elapsed:%f\n", result, dt);
    }

}