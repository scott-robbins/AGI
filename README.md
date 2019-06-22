# [A]rtificial [G]eneral [I]ntelligence
The quest for AGI has accelerated since the recent uptick in
machine learning model accuracies and alongside the explosion in
volume of media/data available. 

But the advent of a *generalized* intelligence seems like a mysterious 
leap forward greater than the sum of it's parts. But why not try 
exactly that, and see what happens (the sum of parts)? 

The goal of this project will be try and tackle subdomains of the 
intellect and try to find the most generic approach to generating
computational models that solve/satisfy problem constraints. 

Once several domains have been developed, begin designing problems 
that are cross-domain by nature and try to develop even more generic
models!?

## Games 
 * Logic 
 * Planning
 * Learning/Memory 
 
## Visual
 * Computer Vision  
 * Learning/Object Detection
 * Learning/Object Classification
 * Learning/Motion Detection 
 
## NLP 
 * Logic 
 * Learning/Associations
 * Learning/Generative Models 
 
# Curiosity 
This is my sandbox for things computers.

## Benchmarking 
I decided to write a program that would take a single argument
to declare a stopping that a for-loop walks up to, accumulating 
a result along the way. The program then displays the final count
and the time elapsed. 

I tried to keep the general idea as identical as possible, writing
the same procedure in C, Python and Java. Running these programs 
size by side, and increasing the size of the input, you can see
how the languages stack up on this simple operation. 

![bench](https://raw.githubusercontent.com/scott-robbins/AGI/master/Curiosity/speed_benchmarking/ForLoop_Benchmarks.png)

Then I cloned this branch on a raspberry pi, recompiled the java and C scripts
and retried the benchmark scripts. 

![pibench](https://raw.githubusercontent.com/scott-robbins/AGI/master/Curiosity/speed_benchmarking/pi_benchmark.png)

OK, this isn't all that impressive though. What about a more memory intensive process
like trying to lead a large file? I wrote three scripts to read through a file (provided
as argument to program), and when it's finished it displays how many lines it read and the
run time of the program. 

Using a ~500k word word-list, we see a clear separation in performance begin to emerge once. 

![fio](https://raw.githubusercontent.com/scott-robbins/AGI/master/Curiosity/speed_benchmarking/fIO.png)

![pio](https://raw.githubusercontent.com/scott-robbins/AGI/master/Curiosity/speed_benchmarking/pIO.png)

Results: 

           ____Laptop BenchMarks____
          | Python | Java | C       |
          | 9.69ms | 12ms | 2.58 ms |  For-Loop         
          | 126 ms | 83ms | 22.2 ms |  File IO
         
           _Raspberry Pi Benchmarks_
          | Python | Java |    C    |
          | 20.7 ms| 69 ms| 5.3 ms  | For-Loop
          | 1.397 s| 979ms| 140.3 ms| File I-O 
 
 By Far the code written in C is fastest for both a laptop and a Raspberry pi, however it is 
 interesting to see the orders of magnitude difference between the languages and across different domains. 
 
 The results do seem to confirm a suspicion I've had though, that python is generally faster for numeric 
 calculations, and computation intensive programming while java excels in the file IO and string manipulation
 domaian. Then again, that could be my own approach to programming in these languages, however as the benchmark
 scripts are basically 10-20 lines each I think it's a fairly bare bones side by side comparison. 
 