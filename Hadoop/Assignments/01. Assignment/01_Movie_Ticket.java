// 1. Movie Ticket Price Calculator
// Write a Java program that determines the price of a movie ticket.
// • The base price is $12.
// • If the person is a senior (age 65 or older), they get a $2 discount.
// • If the person is a child (age 12 or younger), they get a $4 discount.
// • The program should ask for the user's age and then print the final ticket price.

import java.util.Scanner;

class Movie{
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int base_price = 12;
        System.out.print("Please Enter Your Age: ");
        int age = scan.nextInt();
    
    int s_ticket= base_price-2;
    int j_ticket= base_price-4;
    
    if (age>=65){
        System.out.println("The Discounted price for Senior citizen is: $"+s_ticket);
    }
    if (age<=12) {
        System.out.println("The Discounted price for Children is: $"+j_ticket);

   }
   scan.close();
    }

    
}