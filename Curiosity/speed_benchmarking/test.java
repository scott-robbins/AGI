import java.io.*;

class test{

    public static void main(String [] args){
        long start = System.currentTimeMillis();

        int result = 0;
        int size = Integer.parseInt(args[0]);
        System.out.format("Using Size: %d%n", size);
        for(int i=0;i<size;i++){
            result += i;
        }
        long end = System.currentTimeMillis();
        System.out.format("Result: %d    Time Elapsed: %dms%n", result, (end-start));
    }
}