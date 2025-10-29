class PrintOdd {
 public static void main(String[] args) {
    int num [] = {56,12,32,58,86,69,54,30,77,91,27};
    
    // System.out.println("The Array is : " + num[i]);
    System.out.println("The Odd numbers from Array are : ");
    for (int n : num){
        if (n % 2 == 1){
            
            System.out.println(n);
        }
    }
 }   
}
