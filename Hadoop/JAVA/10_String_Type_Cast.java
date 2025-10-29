class StringTypeCast {
    public static void main(String[] args) {
        String num1 = "123.0";
        String num2 = "234.6";
        System.out.println("Adding 2 Strings");
        System.out.println("Addition is: "+ (num1+num2));
        System.out.println("");


        Float add;
        add = Float.parseFloat(num1) + Float.parseFloat(num2);
        System.out.println("String to Float");
        System.out.println("Addition is: "+add);
        System.out.println("");


        String s = num1+123;
        System.out.println("Adding String + Number");
        System.out.println(s);
        System.out.println("");

        float n1 = 54.54f, n2 = 23.65f;
        int result;
        result = (int)n1 + (int)n2;
        System.out.println("Float to Integer");
        System.out.println("Float Addition is:" + result);
        System.out.println("");


        int num = 56;
        String s1 = num + "";
        System.out.println("Integer to String");
        System.out.println("String is : " + s1);
        System.out.println("");



    }
    
}
