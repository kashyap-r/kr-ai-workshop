class Agent {
    private executionCount = 0;

    constructor(
        public readonly name: string
    ) {}

    run (task: string): void {
        this.executionCount++;

        console.log(`${this.name}: ${task}`);
    }

    getExecutionCount(): number{
        return this.executionCount;
    }
}

// this fails becasue of encapsulation
const agent = new Agent("Planner");
// agent.executionCount = 100;
console.log(agent.run("Find parental leave policy"));

