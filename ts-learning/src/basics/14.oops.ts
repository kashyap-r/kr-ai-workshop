/**
 * 
 * 
 */

console.log("---------------- ==== Classes ==== ----------------");
class person {
    name: string;
    age: number; 

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }

    greet() {
        console.log(`Hello, I am ${this.name} and am ${this.age} years old ! `);
    }
}

const myPerson = new person("Kashyap", 39);
myPerson.greet();

/**
 * Access modifiers - control the visibility of properties and methods
 *      - public: accessible everywhere (default)
 *      - private: accessible only within the class 
 *      - protected: accessible within the class and its subclasses
 *      - readonly: the property cannont be modified after initialization
 */
console.log("---------------- ==== Access modifiers ==== ----------------");
class Employee {
    public name: string;
    private salary: number;
    protected department: string;
    readonly id: number;

    constructor(
        name: string, 
        salary: number,
        department: string,
        id: number
    ) {
        this.name = name;
        this.salary = salary;
        this.department = department;
        this.id = id; 
    }

    getSalary (){
        return this.salary;
    }
}

const emp = new Employee("James Bond", 99999, "Spycraft", 7);
console.log(emp.name);
console.log(emp.getSalary);

/**
 * Static Properties and Methods 
 * Static members belong to the class itself, not instances
 */
console.log("---------------- ==== Static Properties & Methods ==== ----------------");
class MathUtil {
    static pi: number = 3.14;

    static claculateCircumference(radius: number): number {
        return 2 * this.pi * radius;
    }
}

console.log(MathUtil.pi);
console.log(MathUtil.claculateCircumference(5));

/**
 * Inheritance(extends)
 * An child class can inherity from a prent class using 'extends'
 */
console.log("---------------- ==== Inheritance ==== ----------------");
console.log("Cat class inheriting Animal class");
class Animal {
    public name: string;
    public color: string;

    constructor (name: string, color: string) {
        this.name = name; 
        this.color = color;
    }
}

class Cat extends Animal {
    public age: number; 

    constructor (name: string, color: string, age: number) {
        // correctly calling parent constructor
        super(name, color);
        this.age = age;
    }

    getDetails() {
        // fixed property access
        console.log(this.name, this.age, this.color);
    }
}

const cat = new Cat("MIKE", "black", 12);
cat.getDetails();

/**
 * Getter & Setters 
 * Getters (get) and setters (set) allow controlled access to properties
 */

console.log("---------------- ==== Getters & Setters ==== ----------------");
class BankAccount {
    private _balance: number = 0;

    get balance(): number {
        return this._balance;
    }

    set balance(amount: number) {
        if (amount  < 0) {
            console.log("Balance cannot be negative.");
        } else {
            this._balance = amount; 
        }
    }
}

const account = new BankAccount();
account.balance = 1000;
console.log(account.balance);

/**
 * Abstract Classes 
 *      - it is a blueprint for other classes.
 *      - It cannot be instantiated directly and may contain 
 *          abstract methods that must be implemented bu derived classes  
 * Key Points
 *  - Defined using the abstract keyword 
 *  - Can have both abstract and non-abstract methods
 */
console.log("---------------- ==== Abstract Classes ==== ----------------");
abstract class Vehicle {
    // Abstract method (must be implmented in derived classes)
    abstract move(): void;
    
    start() {
        console.log("Vehicle is starting...");
    }
}

class Car extends Vehicle {
    move() {
        console.log("Car is moving");
    }
}

const car = new Car();
car.start();
car.move();

/**
 * Method Overriding - A subclass can override a method from its superclass
 */
console.log("---------------- ==== Method Overriding ==== ----------------");
class Parent {
    greet() {
        console.log("Hello from Parent");
    }
}
 
class Child extends Parent {
    greet() {
        console.log("Hello from child");
    }
}

const obj = new Child();
obj.greet();

