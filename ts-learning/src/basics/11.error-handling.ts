/**
 * The basic typescript pattern
 * try {
 *  // code 
 * } catch (error) {
 *  // handle the error 
 * } finally 
 *  // always executes
 */

function divide(a: number, b: number): number {
    if (b === 0) {
        throw new Error("Cannot divide by Zero");
    }

    return a / b;
}

try {
    const result = divide(10, 0);
    console.log(result);
} catch (error) {
    console.log("Something went wrong:", error);
}
