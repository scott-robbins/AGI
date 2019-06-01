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

![pibench](https://raw.githubusercontent.com/scott-robbins/AGI/master/Curiousity/speed_benchmarking/pi_benchmark.png)