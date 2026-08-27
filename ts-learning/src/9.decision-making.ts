/**
 * Decision Making 
 * if statement 
 *  if (boolean expression) {
 *      // statements will execute if the boolean expression is true
 * }
 * if...else statement 
 *  if (boolean_expression) {
 *      // statements will execute if the expressinis true 
 *  } else {
 *      // statements will execute if the expression is false
 * }
 * 
 * elseif and nested if statements 
 * 
 * switch statement
 */

// if statement 
var num: number = 5;
if (num > 0) {
    console.log("number is positive")
}

var isQualified: boolean = true;
if (isQualified){
    console.log("Qualified for driving")
}

var x = 20 
var y = 30 
if (x < y) {
    console.log("x is less than y")
}

// when the condition is false
var x: number = 30;
var count: number = 0 ;
if (x < 30) {
    count ++;
}
console.log(count)

console.log("==========================================")
// if-else statement 

var num: number = 12;
if (num % 2 == 0) {
    console.log("Even");
} else {
    console.log("Odd Number")
}

// if-else-if 
let grade: number = 85;
if (grade >= 90){
    console.log("A Grade")
} else if (grade >= 80) {
    console.log("A Grade")
} else {
    console.log("Pass")
}

/**
 * if (boolean expression1) {
 *      // execute statements if expression1 is true 
 * } else if (boolean expression2) {
 *      // execute if expression 2 is true 
 * } else if (boolean expression3) {
 *      // execute if the expression 3 is true
 * } else {
 *      // exeute if all the expressions evaluate to false
 * }
 */

var num: number = 0 

if (num>0){
    console.log(num+" is positive")
} else if (num < 0) { 
    console.log(num+" is negative")
} else {
    console.log("The number " + num + " is neither positive nor negative!")
}

/**
 * Switcase statement 
 * switch (variable_expression) {
 *      case const_expn1:{
 *          //statements 
 *          break;
 *      }
 *      case const_expn2: {
 *          //statements
 *          break;
 *      }
 *      default: {
 *          //statements 
 *          break;
 *      }
 * }
 */
console.log("-----------Demonstrating Switch Case---------------")
var studentGrade: string = "G";

switch (studentGrade){
    case "A": {
        console.log("Excellent");
        break;
    }
    case "B": {
        console.log("Good");
        break
    }
    case "C": {
        console.log("Average");
        break;
    }
    case "D": {
        console.log("Poor");
        break;
    }
    default: {
        console.log("Needs to repeat!");
        break;
    }
}

console.log("-----------Demonstrating Loops ---------------")

/**
 * Loops 
 * 
 * for 
 * 
 * while 
 *  - The while loop executes the instructions each time the condition specified evaluates to true.
 * 
 * 
 * do..while 
 *  - The dowhile loop is similar to the while loop except that the do...while loop doesnt evaluate the condition for the first time the loop executes.
 *
 */

var i:number = 1;
while (i<=10) {
    if (i % 5 == 0) {
        console.log("The first multiple of 5 between 1 and 10 us "+i);
        break;
    }
    i++
} // outputs 5 and exits the loop 

// The continue statement 

var num: number = 0;
var count:number = 0;

for (num=0; num<=20; num++){
    if (num % 2 == 0) {
        continue;
    }
    count ++;
}
console.log("The count  of odd values between 0 and 20 is: "+count);

// Infinite loops 

/* 
for (;;){
    console.log("This is an endless loop");
}

while (true){
    console.log("this is an endless loop");
}
*/
console.log ("Factorial..")
var num: number = 5;
var i: number;
var factorial = 1;

for (i=num; i>= 1; i--){
    factorial *= i;
}
console.log(factorial)

// for loop with break
var i: number = 0;
for (i;i<5;i++){
    if (i==4) {
        break;
    }
    console.log(i)
}

// for loop with continue statement 
var i: number = 0;
for (i; i<10; i++){
    if (i%2 == 0) {
        continue;
    }
    console.log(i)
}

// for..in loop with strings 
console.log("Printing contents of a string one character by one...")
var j: any;
var n: any = "this is a string";

for (j in n) {
    console.log(n[j]);
}

// the for..in loop with arrays
const arr: number[] = [10, 20, 30, 40];
for (var idx in arr){
    console.log(arr[idx]);
}

// for..in loop with tuples  
const tp:[string, number] = ['Type-script', 20];
for (var jam in tp){
    console.log(tp[jam])
}

// for..of loop 
// for..of loop with arrays
const array: string[] = ["this", "is", "a", "typescript", "class"];
for (var element of array){
    console.log(element);
}

// for..of loop with strings 
const str: string = "this is a typescript class";
for (var char of str){
    console.log(char)
}

/** While loop */

var num: number = 5;
var factorial: number = 1;

while (num >= 1) {
    factorial *= num;
    num --;
}
console.log("The factorial of "+num + " is " + factorial);




