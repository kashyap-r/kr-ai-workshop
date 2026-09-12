/**
 * Functions
 * function function_name (param1[:type], param2[:type], param3[:type])
 */

function disp_details(id:number, name:string, mail_id?:string){
    console.log("ID:", id);
    console.log("Name:", name);
    if (mail_id != undefined)
        console.log("Email id:", mail_id);
}

disp_details(123, "James Bond");
disp_details(1234, "Goldfinger", "goldfinger@jamesbond.com");

/**
 * Rest Parameters
 * Similar to variable arguements in Java
 * Rest parameters dont restrict the number of values that you can pass to a 
 * function. However, the values passed must all be of the same type.
 */
console.log();
console.log("---------------Rest Parameters demo----------------");
function addNumbers(...nums:number[]){
    var i;
    var sum:number = 0;

    for (i=0;i<nums.length;i++){
        sum = sum + nums[i];
    }
    console.log("Sum of the numbers ", sum);
}

addNumbers(1, 2, 3);
addNumbers(10, 10, 10, 10, 10, 10);

/**
 * Default Parameters 
 * function function_name (param1[:type], param2[:type2]=default_type) {
 *      //statements
 * }
 */
console.log();
console.log("---------------Default Parameters demo----------------");
function calculate_discount(price:number, rate:number = 0.50){
    var discount = price * rate;
    console.log("Discount Amount:", discount);
}

calculate_discount(1000);
calculate_discount(1000, 0.3);

/**
 * Anonymous Function
 * Functions that are not bound to an identifier.
 * var res = function([arguements]) { ... }
 */
console.log();
console.log("---------------Anonymous Functions demo----------------");

var msg = function() {
    return "Hello world";
}

console.log(msg());

console.log();
console.log("---------------Anonymous Functions with parameters demo----------------");

var res = function (a:number, b:number) {
    return a*b;
}

console.log(res(12,2));

/** 
 * Function Expression and Function Declaration Are they synonymous? 
 * Function expression and function declaration are not synonymous. Unlike a 
 * function expression, a function declaration is bound by the function name.
 * The fundamental difference between the two is that, function declarations 
 * are parsed before their execution. On the other hand, function expressions
 * are parsed only when the script engine encounters it during execution.
 * 
 * When the JavaScript parser sees a function in the main code flow, it assumes
 * Function Declaration. When a function comes as a part of a statement, it is
 *  a Function Expression.
 */

/** 
 * The Function Constructor
 * 
 * 
 */