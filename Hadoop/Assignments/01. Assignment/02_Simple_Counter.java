// 2. Simple Countdown Timer
// Write a Java program that asks the user to enter a positive integer.
// • Using a for loop or a while loop, count down from that number to 1.
// • Print each number on a new line, followed by "Liftoff!" when the countdown reaches zero.
// Example Output (if user enters 3):
// 3
// 2
// 1
// Liftoff!

import java.util.Scanner;

class Counter {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        System.out.print("Enter the Positive Number: ");
        int count = scan.nextInt();

        for (int i=count; i >= 1; i--){
            System.out.println(i);
        }
        // System.out.println("Count is: "+count);
        System.out.println("Liftoff ✈️✈️✈️ ");
        scan.close();
    }

    
}