
console.log("---- Function Types --------------");

function add(x: number, y: number): number {
    return x + y;
}

console.log(add(10, 20));

console.log("---- Functions with Optional and Defualt paramters --------------");

function greet(name: string, message?: string, suffix: string = "Welcome!") {
    console.log(`${message || "Hello"}, ${name}! ${suffix}`);
}

greet("James Bond");
greet("james bond", "Howdy!");
greet("James Bond", "How u doin?");

console.log("---- Functions - Rest Parameters --------------");

function sum(...number: number[]): number{
    return number.reduce((acc, num) => acc + num, 0);
}

console.log(sum(1, 2, 3, 4, 5)); // Output: 15
console.log(sum(10, 20));        // Output: 30

