/**
 * Async Exception Handling
 */

// We'll simulate an API request 

async function fetchUser(): Promise<string> {
    await new Promise(resolve => setTimeout(resolve, 1000));
    throw new Error ("User service unavailable");
}

