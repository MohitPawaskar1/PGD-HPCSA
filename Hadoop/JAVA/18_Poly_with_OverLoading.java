class Shape {
    int calcArea(int side){
        return side * side;
    }

    int calcArea(int height, int width) {
        return height * width;
    }

    double calcArea(float radius) {
        return Math.PI * radius * radius;
    }
}


class OverLoading {
    public static void main(String[] args) {
        Shape s = new Shape();
        System.out.println("Area of Square   : "+ s.calcArea(12));
        System.out.println("Area of Rectangel: "+ s.calcArea(23,12));
        System.out.println("Area of Circle   : "+ s.calcArea(4.76f));
    }
}