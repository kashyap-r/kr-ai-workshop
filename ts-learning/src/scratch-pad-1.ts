/* 
The Scoping demonstration (Block vs. Function) 
This experiment shows how var leaks outside of loops and if statements, while let and const stay safely locked inside. 
*/
/*
function scopeTest(){
    if (true) {
        var functionScoped = "I am accessible anywhere in this function";
        let blockScoped = " I am only accesible inside this IF Block";
    }
    // the variable functionScoped is accessible here
    console.log(functionScoped);
    // the variable blockScoped is NOT acceble here.
    // console.log(blockScoped);
}

*/
/*
The Hoisting Demonstration 
This experiment shows how JavaScript moves var declarations to the top of the code before running it,
resulting in undefined instead of a crash. 

let and const will safely crash the program to warn you of a mistake.

*/
/*
function hoistingTest() {
    // demostrating var hoisting 
    console.log(hoistedVar);
    var hoistedVar = "Hello from Var";

    // Demonstrating let/const temporal dead zone 
    console.log(hoistedLet);
    let hoistedLet = "Hello from Let";
}

hoistingTest()
*/

// Type Annotations 
// Specify the type of a variable, parameter or return value improving readability and type safety 
console.log();
console.log("----------------------===Demo Type Annotation===------------------------");

let userName: string = "Wow";
let age: number = 25;
let isActive: boolean = true;

function greetUser(name: string, age:number): string {
    return `Hello, ${name}! You are ${age} years old.`;
}

let greeting = greetUser(userName, age);
console.log(greeting);

// Variable Scope
// Local Scope: Variables declared within a function or block are accessible only within that function or block
console.log();
console.log("----------------------===Demo Local Variable Scope===------------------------");
function testLocalScope() {
    let localVar = "I am a local";
    console.log(localVar);
}
// The variable localVar is not accessible here !!! 
// console.log(localVar);
testLocalScope()

// Global Scope - variables declared outside any function or block are accessible throughout the entire program
console.log();
console.log("----------------------===Demo Global Variable Scope===------------------------");
let globalVar = "I am Global, he he he ..!!"
function testGlobalScope(){
    console.log(globalVar);
}
testGlobalScope()
console.log(globalVar);

// class scope
console.log();
console.log("----------------------===Demo Class Scope===------------------------");
class Employee {
    salary: number = 50000;
    printSalary(): void {
        console.log(`Salary: ${this.salary}`);
    }
}

const emp = new Employee();
emp.printSalary();
// variable not accessible
//console.log(salary);
// 
console.log("I can print the salary here too.. ",emp.salary)


