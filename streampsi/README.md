In class we considered the Kolmogorov (Chaitin) Complexity of a string – the length of the shortest program that can generate the string. Obviously some strings can be generated quite simply (e.g. 010101...01 n times), while others are more diﬃcult (e.g. a truly random string). For this problem you will need to write a program (in Python) that generates the ﬁrst n digits of ψ, the reciprocal ﬁbonacci constant. ψ = 1/1 + 1/1 + 1/2 + 1/3 + 1/5.... Note that the program needs to be ”streaming” – it should generate one digit per line, and continue doing so until interrupted (killed). So we will execute:  
$python stream psi.py 100 \\
and expect the output to start \\
3 \\
3 \\
5 \\
9 \\
8 \\
8 \\
and so on. Note that the program can take in a ridiculously large input n, so the algorithm should not compute the whole number ψ and then output it – rather do it digit by digit. Hence we  also make sure to ﬂush the output buﬀer with every digit.
