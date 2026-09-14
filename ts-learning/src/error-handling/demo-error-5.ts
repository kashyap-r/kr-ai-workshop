/**
 * Error Propagation and Rethrowing
 * Sometimes a lower-level function fails, but it doesn't know how the application should respond.
 * 
 */

function databaseQuery(): string {
    throw new Error("Database connection refused");
}

function getUser(): string {
    try {
        return databaseQuery();
    } catch (error) {
        if (error instanceof Error) {
            console.log("Application handled error:", error.message);
        }
        throw error;
    }
}