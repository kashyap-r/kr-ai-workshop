// Variable declarations 

// using let: mutable i.e. value can be changed after declaration 
// let provides block-level scoping 
let count = 5;
if (count > 0) {
  let message = "Count is positive";
  console.log(message); 
}
// console.log(message);  // Error: message is not accessible here


// using const: Immutable

// Types of variable declarations
// declare type and value in a single statement 
let name: string = "Kashyap";
// declare type without value 
let age: number;
// declare value without type 
let city = "Bengaluru"

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