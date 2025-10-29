class Person{ // Class Declaration
    String name; // Class Variables
    int age;
    Person(String n, int a){ // Constructor
        name = n;
        age = a;
    }    
    void display(){ // Class Method
        System.out.println("Name: " + name);
        System.out.println("Age : " + age);
    }

    class Player{
        String sport;
        float rating;
    }
    Player ply = new Player();
}

class InnerClass {
    public static void main(String[] args) {
        Person p1 = new Person("Mohit", 23);  //Object1
        p1.display(); // Method call for Object1
        p1.ply.sport = "Football";
        System.out.println("Sport : "+ p1.ply.sport);
        Person p2 = new Person("Soham", 22);  //Object 2
        p2.display(); // Method call for Object2
        p2.ply.sport = "Cricket";
        System.out.println("Sport : "+ p2.ply.sport);
        Person p3 = new Person("Yogesh", 25);  //Object 3
        p3.display();
        p3.ply.sport = "Carrom";
        System.out.println("Sport : "+ p3.ply.sport);
        Person p4 = new Person("Ajinkya", 27);  //Object 2
        p4.display();
        p4.ply.sport = "Chess";
        System.out.println("Sport : "+ p4.ply.sport);
    }
}
