import java.util.Scanner;

class Input{
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        System.out.print("Please Enter Your Name: ");
        String name = scan.nextLine();
        System.out.println("Welcome "+ name);
        scan.close();
    }
}