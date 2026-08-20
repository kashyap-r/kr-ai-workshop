/*
Author: Kashyap 
Description: TypeScript revision - 2026
This is a basic TypeScript file that demonstrates the usage of different data types in TypeScript.

* This is a multi-line comment in TypeScript. It can span multiple lines and is often used for documentation purposes.
*/

console.log("Hello welcome to TypeScript..!!");  


// declaring a variable 
// this is a variable of type "any" which can hold any type of value
let userId = 101;
console.log("User ID is : " + userId);

// declaring a variable of type "number"
// the usage of : is called type assignment or type annotation
let userAge: number = 25;
console.log("User Age is : " + userAge);

// declaring a variable of type "string"
let userName: string = "Kashyap";
console.log("User Name is : " + userName);

// declaring a variable of type "boolean"
let isUserActive: boolean = true;
console.log("Is User Active? : " + isUserActive);

// declaring a variable of type "array"
let userSkills: string[] = ["JavaScript", "TypeScript", "Node.js"];
console.log("User Skills are : " + userSkills.join(", "));

// declaring a variable of type "tuple"
let userDetails: [number, string, boolean] = [101, "Kashyap", true];
console.log("User Details are : ID - " + userDetails[0] + ", Name - " + userDetails[1] + ", Active - " + userDetails[2]);

// declaring a variable of type "enum"
enum UserRole {
    Admin,
    User,
    Guest
}
let userRole: UserRole = UserRole.Admin;
console.log("User Role is : " + UserRole[userRole]);    

// printing the type of variable
console.log("Type of userId is : " + typeof userId);
console.log("Type of userAge is : " + typeof userAge);
console.log("Type of userName is : " + typeof userName);
console.log("Type of isUserActive is : " + typeof isUserActive);
console.log("Type of userSkills is : " + typeof userSkills);
console.log("Type of userDetails is : " + typeof userDetails);
console.log("Type of userRole is : " + typeof userRole);


// Functions 

function add(a: number, b=5) {
    return a + b 
}

add(10)

console.log("Sum of two numbers ", add(20))
