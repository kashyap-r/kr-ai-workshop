/**
 * Basic Retry Logic 
 * To test, lets createa service that fails twice and succeeds 
 * on the third attempt. 
 */

let attemptCount = 0;

async function unstableService(): Promise<string> {
    attemptCount++;
    console.log(`Service call attempt ${attemptCount}`);

    if(attemptCount < 3) {
        throw new Error("Temporary Service failure, Retrying..");
    }
    return "Success!";
}

// now the generic retry function 
async function retry<T>(
    // operation is a function that takes no arguments and returns a Promise 
    // containing type T.
    operation: () => Promise<T>,
    maxAttempts: number): Promise<T> {
        let lastError: unknown;
        for (
            let attempt = 1; 
            attempt<= maxAttempts; 
            attempt++) {
                try {
                    return await operation();
                } catch (error) {
                    console.log(`Attempt ${attempt} failed`);
                    lastError = error;
                }
        }
        throw lastError;
    }

async function main() {
    try {
        const result = await retry (unstableService, 3);
        console.log("Final result:", result);
    } catch (error) {
        console.log ("All retry attempts failed");
    }
}

main();