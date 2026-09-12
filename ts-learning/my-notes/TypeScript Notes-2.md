Type Script Classes 

1. Classes and Objects 
A class defines structure and behavior. An object is an instance of that class. 

class Agent {
    name: string;
    model: string;

    constructor(name: string, model: string) {
        this.name = name;
        this.model = model;
    }

    run(task: string): string {
        return `${this.name} is executing: ${task}`;
    }
}

const researchAgent = new Agent(
    "ResearchAgent",
    "gpt-5"
);

console.log(
    researchAgent.run("Find parental leave policy")
);



2. Constructors 

Defining a constructor is not mandatory in Typescript 

If you do not explicitly define a constructor in uour clas, Typescript (and 
the underlying JavaScript) automaatically provides a default constructor 
for you. 

How Default Constructors Work

The behavior of the automatic default constructor depends on whether your 
class stands alone or extends another class:

Base Classes (Standalone): If the class does not extend another class, 
TypeScript generates an empty, parameterless constructor.

class User {
  name: string = "Anonymous";
}

// Works perfectly. TypeScript uses the implicit default constructor.
const user = new User(); 

Derived Classes (Inheritance): If your class extends a base class, the 
default constructor automatically calls super() and passes along any 
arguments provided during instantiation.

class Animal {
  constructor(public species: string) {}
}

// No explicit constructor defined here
class Dog extends Animal {} 

// The implicit constructor automatically passes "Canine" to the parent 
class via super()
const myDog = new Dog("Canine"); 

When You Must Define a Constructor

While not syntactically mandatory to make a class compile, you will 
practically need to define a custom constructor in the following 
scenarios:

1. Custom Property Initialization: When you need to accept arguments when 
creating an object (using the new keyword) to set unique values for each 
instance.

2. Strict Property Initialization: If you have strictPropertyInitialization 
enabled in your tsconfig.json, TypeScript requires all class fields to 
either have a default value or be definitely assigned within the 
constructor.

3. Executing Setup Logic: If your class needs to perform specific initial 
operations, setup processes, or validation immediately upon creation.

4. Altering Derived Arguments: If your child class requires different 
parameters than the parent class, you must write a custom constructor and 
manually call super() with the required base class arguments

