### Functions in TypeScript

TypeScript provides powerful function features like function types, optional/
default parameters, rest parameters, function overloading, and arrow functions 
with this binding.

#### 1. Function Types 
A function type defines thte types of parameters and the return value.

function add (x: number, y:number): number {
    return x + y;
};

console.log(add(10, 20));

How It Works?
    The function type (a: number, b: number) => number means:
    The function takes two numbers as parameters.
    It returns a number.

#### 2. Optional and Default Parameters
    - Optional Parameters (param?: type): The parameter can be omitted.
    - Default Parameters (param: type = defaultValue): If omitted, it gets a default value.

function greet(name: string, message?: string, suffix: string = "Welcome!") {
    console.log(`${message || "Hello"}, ${name}! ${suffix}`);
}

greet("James Bond");
greet("james bond", "Howdy!");
greet("James Bond", "How u doin?");

How It Works?
message?: string → This is an optional parameter.
suffix: string = "Welcome!" → If omitted, "Welcome!" is used as a default value.

#### 3. Rest Parameters (...args)
Rest parameters allow a function to accept multiple arguments as an array.

function sum(...numbers: number[]): number {
  return numbers.reduce((acc, num) => acc + num, 0);
}

console.log(sum(1, 2, 3, 4, 5)); // Output: 15
console.log(sum(10, 20));        // Output: 30

How It Works?
...numbers: number[] means any number of parameters will be stored in an array.
reduce((acc, num) => acc + num, 0) sums up all elements.

#### 4. Function Overloading
Function overloading allows defining multiple function signatures with the same 
name but different parameter types.

function displayInfo(info: string): void;
function displayInfo(info: number): void;
function displayInfo(info: string | number): void {
  if (typeof info === "string") {
    console.log(`Name: ${info}`);
  } else {
    console.log(`Age: ${info}`);
  }
}

displayInfo("James Bond"); // Output: Name: James Bond
displayInfo(25);        // Output: Age: 25

How It Works?
First two lines define function overload signatures.
The actual function handles both cases (string and number).
This ensures type safety while allowing multiple argument types.

#### 5. Arrow Functions & this Binding
Arrow functions preserve the this context of their surrounding scope.

Problem with this in Regular Functions

class Person {
    name = "James Bond";

    greet() {
        setTimeout (function() {function () {
            console.log(`Hello, ${this.name`}); // 'this' is undefined here 
        }, 1000);
    }
}
const p = new Person();
p.greet(); // Ouput: Hello, undefined

here, the funciton inside setTimeout has its own this, so it loses the context of 
Person.

Solution: Use Arraw function 

class Person {
    name = "James Zond";

    greet() {
        setTimeout(() => {
            console.log(`Hello, ${this.name`});
        }, 1000);
    }
}

const p = new Person();
p.greet(); 

//Output: Hello, James Bond

How Arrow Functions Fix this?
Arrow functions do not have their own this.
They inherit this from the surrounding function (i.e., Person class in this case).