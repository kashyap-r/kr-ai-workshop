/***
 * Demonstrating Error, throw, try, catch, finally
 */

function divide(a: number, b:number): number {
    if (b===0) {
        throw new Error ("Division by Zero is not allowed");
    }
    return a/b;
}

try {
    console.log("Starting calculation...");
    const result = divide(10, 0);
    console.log("Result:", result);
} catch (error) {
    console.log("An error occured!");

    if (error instanceof Error) {
        console.log("Error message:", error.message);
    }
} finally {
    console.log("Calculation finished.");
}