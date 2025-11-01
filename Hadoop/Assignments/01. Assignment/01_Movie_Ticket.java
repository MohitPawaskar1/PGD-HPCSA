// 1. Movie Ticket Price Calculator
// Write a Java program that determines the price of a movie ticket.
// • The base price is $12.
// • If the person is a senior (age 65 or older), they get a $2 discount.
// • If the person is a child (age 12 or younger), they get a $4 discount.
// • The program should ask for the user's age and then print the final ticket price.

import java.io.DataInputStream;
import java.io.IOException;

class Movie{
    public static void main(String[] args) throws IOException{
        int base_price = 12;
        DataInputStream i = new DataInputStream(System.in);
        String num = null;
        System.out.print("Please Enter Your Age: ");
        num = i.readLine();
        int age = Integer.parseInt(num);
        System.out.println("Age "+ age);
    
    int s_ticket= base_price-2;
    int j_ticket= base_price-4;
    
    if (age>=65){
        System.out.println("The Discounted price for Senior citizen is: $"+s_ticket);
    }
    if (age<=12) {
        System.out.println("The Discounted price for Children is: $"+j_ticket);

   }
    }
}