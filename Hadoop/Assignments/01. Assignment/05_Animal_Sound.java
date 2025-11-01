// 5. Animal Sounds
// Create a base class called Animal with a method:
// • void makeSound(): This method prints "The animal makes a sound."
// Create two subclasses, Dog and Cat, that inherit from Animal.
// • Override the makeSound() method in each subclass to print "The dog barks." and "The cat
// meows.", respectively.
// In your main method, create a Dog object and a Cat object, store them in Animal reference
// variables (polymorphism), and call the makeSound() method on both.


class Animal {

    void makeSound(){
        System.out.println("The Animal makes a sound.");
    }

}

class Dog extends Animal {

    void makeSound(){
        System.out.println("The dog barks.");
    }    
}

class Cat extends Animal {

    void makeSound(){
        System.out.println("The cat meows.");
    }
}


class Sounds {

    public static void main(String[] args) {
        Dog d = new Dog();
        Cat c = new Cat();
        d.makeSound();
        c.makeSound();
    }
}