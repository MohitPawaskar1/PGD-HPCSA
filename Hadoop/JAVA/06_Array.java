class ArrayAddition {
 public static void main(String[] args) {
    int num [] = {56,12,32,58,86,69,54,30};
    int add=0;
    for (int i = 0; i< num.length; i++){
        add=add+num[i];
    }
    System.out.println("The Addition is: " + add);
 }   
}
