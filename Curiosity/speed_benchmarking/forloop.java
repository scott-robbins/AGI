import java.io.*;

class test{

    public static void main(String [] args){
        if (args.length < 2){
            System.out.println("Usage: java test <size>");
            exit(0);
        }
        long start = System.currentTimeMillis();

        int result = 0;
        int size = Integer.parseInt(args[0]);
        System.out.format("Accumulating Using For-Loop Size: %d%n", size);
        for(int i=0;i<size;i++){
            result += i;
        }
        long end = System.currentTimeMillis();
        System.out.format("Result: %d    Time Elapsed: %dms%n", result, (end-start));
    }
}
