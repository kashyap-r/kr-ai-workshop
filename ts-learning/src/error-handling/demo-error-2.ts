/**
 * "unknown inside catch"
 * TypeScript doesn't assume everything thrown is an Error.
 * When it comes across ..
 *  throw "Something failed"
 * Typescript treats the caught value as potentially unknown
 */

function riskyOperation(): void {
    throw "Server Exploded!";
}
try {
    riskyOperation();
} catch (error) {
    console.log("Caught Something! ");
    if (typeof error === "string") {
        console.log("String error:", error);
    }
}

try {
    throw 500; 
} catch (error) {
    if (typeof error === "number") {
        console.log("Error Code:", error);
    }
}