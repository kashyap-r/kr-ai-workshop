// Type Script Classes 
// Can define a class without a constructor, but you have to initialize the 
// class attributes with some value
// console.log("Kashyap is learning Oops in TypeScript")

// console.log ("\n------------------====== =====---------------------");
// console.log ("Class definition without a constructor");
class User {
    name: string = "Anonymous";
}
// const user = new User();
// console.log(user.name);
// console.log ("\n------------------====== =====---------------------");

class Agent1 {
    name: string;
    model: string ;

    constructor(name: string, model:string) {
        this.name = name;
        this.model = model; 
    }

    run (task: string): string {
        return `Agent ${this.name} is executing the task: ${task}`;
    }
}

//const researchAgent = new Agent1("ResearchAgent", "gpt-5");
// researchAgent is the Object
// console.log(researchAgent.run("Find parental Leave Policy"));
// console.log(`The model being used by the agent ${researchAgent.name} is ${researchAgent.model}`)
// This Class definition is same as the above 
class AgentSameAs {
    constructor (
        public name: string,
        public model: string
    ) {}
}
// console.log ("\n------------------====== =====---------------------");

/** Encapsulation
 * public
 * private
 * protected
 */

class MyAgent {
    private executionCount = 0 
    constructor(
        // an agent ID should probably never mutate after creation
        public readonly id: string,
        public name: string,
        public model: string
    ){}

    run (task: string): string {
        this.executionCount++;
        return  `${this.name}: ${task}`;
    }

    getExecutionCount(): number{
        return this.executionCount;
    }
}

const agent = new MyAgent("XC90-1", "Planner", 'gpt-5.4-nano');
// the below statement will fail because of encapsulation, 
// executionCount is defined as private to the class and hence 
// modifiable only within the class
// agent.executionCount = 100;
console.log(`The agent id : ${agent.id}`);
console.log(`The agent name: ${agent.name}`);
console.log(`The model used: ${agent.model}`);
console.log(`The task: ${agent.run("Check my eligibility for parental leave")}`);
console.log('Execution Count: ',agent.getExecutionCount());
console.log ("\n------------------====== =====---------------------");

/**
 * Using Typescript getters and setters to make the classes cleaner
 * The Getter: Exposes the private executionCount as a read-only property to
 * the outside world.
 * 
 * The Setter: Prevents invalid configurations (like assigning an empty 
 * string to the agent's name or an unsupported LLM model).
 *  */

console.log("Same Agent implemented using getters and setters ")
class Agent {
    private _executionCount = 0;
    private _name: string;
    private _model: string;

    constructor(
        public readonly id: string,
        name: string, 
        model: string
    ){
        // Using the setters inside the constructor ensures initial values are also validated!
        this._name = name;
        this._model = model;
    }

    // 1. GETTER: Exposes executionCount as read-only. 
    // 
    public get executionCount(): number {
        return this._executionCount;
    }

    // 2. GETTER & SETTER for 'name'
    public get name(): string {
        return this._name
    }

    public set name(newName: string){
        if (!newName.trim()){
            throw new Error("Agent name cannot be empty.");
        }
        this._name = newName;
    }

    // 3. GETTER & SETTER for 'model' (with custom logic)
    public get model(): string {
        return this._model;
    }

    public set model(newModel: string) {
        if (!newModel.startsWith("gpt-") && !newModel.startsWith("deepseek-")) {
            throw new Error(`Unsupported model tier: $newModel`);
        }
        this._model = newModel;
    }

    public run(task: string): string {
        this._executionCount++;
        return `${this.name} (${this.model}): ${task}`;
    }
}

// Testing the implementation 

const newAgent = new Agent("XC90-1", "Planner", 'gpt-5.4-nano');

// Notice how we access .executionCount without parenthesis ()
console.log(`Initial count: ${newAgent.executionCount}`); // Outputs: 0

newAgent.run("Check parental leave eligibility");

// The getter intercepts this seamlessly
console.log(`New count: ${newAgent.executionCount}`); // Outputs: 1

// Attempting to overwrite the getter will fail compilation:
// agent.executionCount = 100; // ❌ Error: Cannot assign to 'executionCount' because it is a read-only property.

// Testing the Setters
newAgent.name = "Strategist"; // ✅ Works flawlessly
console.log(`Updated Name: ${newAgent.name}`); 

try {
    newAgent.model = "llama-3-basic"; // ❌ Throws error: Unsupported model tier
} catch (error: any) {
    console.error(`Validation caught: ${error.message}`);
}

/**
 * The Underscore Convention (_propertyName): When creating a getter/
 * setter, you must change the name of the underlying private variable 
 * (usually by adding an underscore). 
 * 
 * If you don't, JavaScript gets confused and enters an infinite 
 * loop.
 * 
 * Property-like Syntax: Outside the class, you read and write
 * data normally using = and no parentheses (agent.name = "New Name"),
 * but behind the scenes, your custom validation logic executes.
 * 
 */
