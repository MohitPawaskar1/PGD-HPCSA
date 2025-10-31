import java.io.DataInputStream;
import java.io.IOException;

class Input{
    public static void main(String[] args) throws IOException{
        DataInputStream i = new DataInputStream(System.in);
        String name = null;
        System.out.print("Please Enter Your Name: ");
        name = i.readLine();
        System.out.println("Welcome "+ name);
    }
}