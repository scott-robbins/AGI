import java.io.*;
import java.util.*;

class ReadFile{

    public static void main(String [] args){
        if (args.length < 1){
            System.out.println("Usage: java ReadFile <filename>");
            System.exit(0);
        }

        String fileName = args[0];
        System.out.format("Reading : %s%n", fileName);

        long start = System.currentTimeMillis();

        Vector <String> content = new Vector<>();
        BufferedReader br = null;
        String data = "";
        try{
            br = new BufferedReader(new FileReader(fileName));
            String line = "";
            while( (line = br.readLine()) != null){
                content.add(line);
            }
        } catch(FileNotFoundException e){System.out.println("File Not Found!");}
          catch(IOException e){e.printStackTrace();}

        long end = System.currentTimeMillis();
        System.out.format("%d Lines Read.    %d ms.%n", content.size(), (end-start) );
    }

}