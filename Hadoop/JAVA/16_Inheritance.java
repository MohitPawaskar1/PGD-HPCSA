class Flower {
    String name;
    int num_petals;
    Flower(String name, int num_petals){
        this.name = name;
        this.num_petals=num_petals;
    }
    void show(){
        System.out.println("Flower: " + this.name);
        System.out.println("Petals: " + this.num_petals);

    }
}
class Rose extends Flower{
    String color;
    Rose(String n, int p, String c) {
        super (n,p);
        color = c;
    }
    void print(){
        System.out.println("Color : " + color);
    }

}
class Inheritance {
    public static void main(String[] args) {
        Rose r = new Rose("Red Rose" , 10, "Maroon");
        r.show();
        r.print();

    }
    
}
