// Understanding Getter and setter in TypeScript

console.log("-------------------");

class User{
    constructor(public firstName: string, public lastName: string){
}

// get is the accessor is treated as a property, so you can access it like a property, 
// without calling it as a method
get fullName(): string {
    return `${this.firstName} ${this.lastName}`;
}
}

const user = new User("John", "Doe");
console.log(user.fullName);

// using setter to set the value of a property
class User2{
    private _age: number;

    constructor(public firstName: string, public lastName: string, age: number){
        this._age = age;
    }

    get age(): number {
        return this._age;
    }

    set age(value: number) {
        if (value < 0) {
            throw new Error("Age cannot be negative");
        }
        this._age = value;
    }
}

const user2 = new User2("Jane", "Doe", 30);
console.log(user2.age); // 30

user2.age = 35; // sets the age to 35
console.log(user2.age); // 35

// user2.age = -5; // Error: Age cannot be negative         

// static properties and methods are associated with the class itself, rather than with
//  instances of the class.
// So you can access them without creating an instance of the class.
console.log("-------------------");

class User3 {
    static count: number = 0;

    constructor(public firstName: string, public lastName: string){
        User3.count++;
    }

    static getCount(): number {
        return User3.count;
    }
}

const user3 = new User3("Alice", "Smith");
const user4 = new User3("Bob", "Johnson");

console.log(User3.getCount()); // 2

console.log("-------------------");
// understand inheritance in TypeScript
// inheritance allows you to create a new class that is based on an existing class,
//  inheriting its properties and methods. The new class is called a subclass or derived class, 
//  and the existing class is called a superclass or base class.
// The subclass can add new properties and methods, or override existing ones.
// In TypeScript, you use the extends keyword to create a subclass.
// The subclass can call the constructor of the superclass using the super keyword,
//  and it can also call methods of the superclass using super.methodName().    
// The subclass can also access public and protected properties and methods of the superclass,
//  but it cannot access private properties and methods of the superclass.
// The subclass can also implement interfaces, which are contracts that define the shape of an object.  
// The subclass can implement multiple interfaces, but it can only extend one superclass.
// The subclass can also be used as a type, so you can use it in type annotations and type assertions.
// The subclass can also be used in polymorphism, which is the ability of an object to take on many forms.
// The subclass can also be used in generics, which are a way to create reusable components that work with different types.
// The subclass can also be used in decorators, which are a way to add metadata to classes and methods.
// The subclass can also be used in mixins, which are a way to create reusable classes that can be combined with other classes.
// The subclass can also be used in abstract classes, which are classes that cannot be instantiated, but can be extended by other classes.
// The subclass can also be used in interfaces, which are contracts that define the shape of an object.
// The subclass can also be used in modules, which are a way to organize code into reusable units.
// The subclass can also be used in namespaces, which are a way to organize code into logical groups.
// The subclass can also be used in ambient declarations, which are a way to describe the shape of code that exists outside of TypeScript.
// The subclass can also be used in declaration merging, which is a way to combine multiple declarations of the same name into a single declaration.
// The subclass can also be used in type guards, which are a way to narrow the type of an object based on its properties and methods.
// The subclass can also be used in type inference, which is a way to automatically determine the type of an object based on its properties and methods.
// The subclass can also be used in type assertions, which are a way to tell the compiler what the type of an object is.
// The subclass can also be used in type aliases, which are a way to create a new name for an existing type.
// The subclass can also be used in type parameters, which are a way to create generic types that can be used with different types.
// The subclass can also be used in type constraints, which are a way to restrict the types that can be used with generic types.
// The subclass can also be used in type inference, which is a way to automatically determine the type of an object based on its properties and methods.    
// THe super() keyword is used to call the constructor of the superclass, and it must be called before you can use this in the subclass constructor.    
// The super.methodName() syntax is used to call a method of the superclass, and it can be used in any method of the subclass.
// The super.propertyName syntax is used to access a property of the superclass, and it can be used in any method of the subclass.
// The super keyword can also be used in static methods, but it can only be used to access static properties and methods of the superclass.
// The super keyword can also be used in getters and setters, but it can only be used to access getters and setters of the superclass.
// The super keyword can also be used in async methods, but it can only be used to access async methods of the superclass.

class Person {
    constructor(public firstName: string, public lastName: string) {
    }

    getFullName(): string {
        return `${this.firstName} ${this.lastName}`;
    }
}

class Employee extends Person {
    constructor(firstName: string, lastName: string, public jobTitle: string) {
        super(firstName, lastName);
    }

    getEmployeeInfo(): string {
        return `${this.getFullName()} - ${this.jobTitle}`;
    }
}

const employee = new Employee("James", "Bond", "Software Engineer");
console.log(employee.getEmployeeInfo()); // James Bond - Software Engineer   
