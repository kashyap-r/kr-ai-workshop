/***
 * instanceof Error
 * In the real world ost libraries throw actual Error objects
 */

function loadConfiguration(): void {
    throw new Error("Configuration file is missing!");
}

try {
    loadConfiguration();
} catch (error) {
    if (error instanceof Error) {
        console.log("Name:", error.name);
        console.log("Message:", error.message);
        console.log("Stack available:", error.stack !== undefined);
        // console.log("Stack available:", error.stack);
        console.log("Cause:", error.cause);
    } else {
        console.log("Unknown non-Error value thrown:", error);
    }
}

// the statement "if (error instanceof Error)" confirms the error
// This concept is called type narrowing.