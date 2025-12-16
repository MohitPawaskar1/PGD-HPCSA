#!/bin/bash
#SBATCH --output=/tmp/basic_job.out
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=1
#SBATCH --partition=debug

apt install gcc &> /dev/null
touch HelloWorld.c

echo '#include <stdio.h>
int main() {
    printf("Hello, World!\n");
    return 0;
}' >> HelloWorld.c

gcc HelloWorld.c -o hello
./hello




