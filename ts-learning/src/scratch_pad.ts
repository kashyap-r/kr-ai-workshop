/*
### Variables in TypeScript 

* The can be declared using let, const, or var with optional type annotations for better type safety. 

Note: Using var is generally avoided for variable declaration because let and const provide safer block-level scoping.
*/

//1. Declare Type and Value in a single statement 

    let username: string = 'Jam';
    const userage: number = 25;

// 2. Declare Type without a value 

    let gender: string;

// 3. Declare value without a type 

    let country = 'India';

/* Variable declarations 
// using let: mutable i.e. value can be changed after declaration 
// let provides block-level scoping 
*/

let count = 5;
if (count > 0) {
  let message = "Count is positive";
  console.log(message); 
}
// The below statement will error out, the variable 'message' is not accessible here
// console.log(message);  

/* 
Using var: var is function scoped.  It is generally avoided in modern typescript because let 
and const provide for safer block-level scoping
*/


// using const: Immutable


// Type Annotations
let userName: string = "Jane";  
let uage: number = 25;            
let isActive: boolean = true;    

function greetUser(name: string, age: number): string {
  return `Hello, ${name}! You are ${uage} years old.`;
}

let greeting = greetUser(userName, uage);
console.log(greeting);


/**
 * Variable scope
 */

// local scope ;- variables declared within a function or a loop are only accessible within that loop. 
function testScope(){
    let localVar='I am a localite';
    console.log(localVar)
}
// console.log(localVar) // errors as it is not defined outside the function 

// global scope
let globalVar = 22;
function testGScope(){
    console.log(globalVar)
}
testGScope()
// works perfectly

// class scope - variables declared within a class are accessible to all members (methods) of that class
class Employee {
    salary: number = 50000;
    printSalary(): void{
        console.log('Salary: ${this.salary');
    }

}

const emp = new Employee();
emp.printSalary();

// Datatypes 
console.log('=============:Datatypes:===========')
/* Primitive Types 
number, string, boolean, null, undefined, symbol, bigint

Object Types 
Object, array, tuple, enum function class interface

Advanced Types 
union types, interscriotion types, literal types mapped types/.

*/