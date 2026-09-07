

Creating your first Typescript project

Step 1: Create a project folder 
        mkdir my-ts-project

Step 2: Initialize the project
        Navigate to the folder 
            cd my-ts-project
        Create the tsconfig.json file containing the compiler configuration 
            tsc --init 

Step 3: Write Typescript Code 
        console.log("Hello, TypeScript!");
        save the file as main.ts

Step 4: Compile the TypeScript Code 
        tsc 
        To compile all the files in the source directory, run: npx tsc 

Step 5: Run the generated Javascript code using Node.js
        node main.js 


### Variables in TypeScript 

* The can be declared using let, const, or var with optional type annotations for better type safety. 

Note: Using var is generally avoided for variable declaration because let and const provide safer block-level scoping.

1. Declare Type and Value in a single statement 

    let name: string = 'Jam';
    cons age: number = 25;

2. Declare Type without a value 

    let gender: string;

3. Declare value without a type 

    let country = 'India';

### Data Types in TypeScript 

#### Primitive Types 
Type        KeyWord     Description
Number      number      Represents both integer and floating-point numbers 
String      string      Represents textual data
Boolean     boolean     Represents logical Value: true or false 
Null        null        Represents intentionl absence of any vale
Undefined   undefined   Represents n uninitialized variable
Symbol      symbol      Represents a unique, immutable value, often used as object keys 
BigInt      bigint      Represents integers with arbitrary precision

#### Object Types 

Type        Description 
Object      Represents any non-primitive type, its use is generally discouraged. 
Array       Represents a collection of elements of specific types 
Tuple       Represents array with fixed number of elements of specifi types 
Enum        Represents a set of named constants, allowing for a collection of related values 
Function    Represents a callable entity; candefine parameter and return types 
Class       Defines a blueprint for creating objects with specific properties and methods
Interface   Describes the shape of an object 

#### Advanced Types 
Typescript also offers advanced types that provide additional capabilites for complex type 
definitions.

Type            Description 

Union Types     Allows a variable to hold one of several types providing flexibility in type 
                assignments
Intersection    Combines multipe types into one, requiring a value to satisfy all included types 
Types

Literal Types   Enables exact value types, allowing variables to be assigned specific values only 

Mapped Types    Creates new types by transforming properties of an existing type according to a 
                specified rule


### Best Practices
1. Use let and const Instead of var: Prefer let and const for block-scoped variables to avoid 
issues with hoisting and scope leakage.

2. Avoid the any Type: Refrain from using any as it bypasses type checking; opt for specific types 
to maintain type safety.

3. Leverage Type Inference: Allow TypeScript to infer types when possible, reducing redundancy and 
enhancing code readability.

4. Utilize Utility Types: Employ built-in utility types like Partial<T> and Readonly<T> to create 
flexible and readable type definitions.

Reference: https://www.geeksforgeeks.org/typescript/data-types-in-typescript/








Note: 
1. Do this - Create object, access object atributes. 
2. Try creating list of objects and access the object attributes 
