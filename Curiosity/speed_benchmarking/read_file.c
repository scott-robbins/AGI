#include <stdio.h>
#include <time.h>


void main(int argc, char **argv){
    if (argc < 2){
        printf("Usage: ./test_c <size>\n");
        exit(0);
    } else{
        clock_t start = clock();

        FILE *fid;
        char line [256];
        int nLines = 0;

        fid = fopen(argv[1], "r");
        while(fgets(line, 255, (FILE*) fid)){
            nLines = nLines + 1;
        }

        clock_t end = clock();
        double dt = (double)(end - start) / CLOCKS_PER_SEC;
        printf("%d Lines Read\tTime Elapsed:%f seconds\n",nLines, dt);
    }

 }