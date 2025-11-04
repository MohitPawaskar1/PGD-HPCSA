class Strings {
    public static void main(String[] args) {
        
        // Concatenate
        String name = "Mohit";
        String surname = "Pawaskar";

        System.out.println("Concatenate Two Strings   : "+name+" "+surname);
        System.out.println("Check the Character Index : "+name.charAt(0));
        System.out.println("Check the Character Length: "+name.length());
        System.out.println("Replace the Character     : "+name.replace('M', 'R'));
        System.out.println("Printing SubString        : "+name.substring(0, 2));
    }
}
