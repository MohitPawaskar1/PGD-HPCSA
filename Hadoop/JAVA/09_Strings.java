class StringOperations{
    public static void main(String args[]) {
        char ch = 'C'; // Character Declaration
        char name [] = {'H','P','C','S','A'};
        String str = new String(name); // Create String -I
        String city = "Pune"; // Create String -II
        System.out.println("Character is: " +ch);
        System.out.println("String is: "+str);
        System.out.println("City name is: "+city);
        System.out.println("After Concatenation: "+ (str+city)); // Concatenate Strings
        System.out.println("Length of String is: " +city.length()); // Length of Strings
        System.out.println("Char at: " + city.charAt(2) );
        System.out.println("Starts: "+ str.startsWith("h"));
        System.out.println("Lower: "+city.toLowerCase());
    }
    
}
