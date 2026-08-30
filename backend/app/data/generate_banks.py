import json
import os
import random
from app.config.careers import CAREERS

TECHNICAL_SKILLS = {
    'APIs', 'AWS', 'CI_CD', 'CSS', 'Docker', 'Embeddings', 'HTML', 'Hugging_Face', 
    'Image_Processing', 'JavaScript', 'Kubernetes', 'LLMs', 'MLOps', 'Machine_Learning', 
    'Node.js', 'OpenCV', 'Pandas', 'Prompt_Engineering', 'PyTorch', 'Python', 'RAG', 
    'React', 'SQL', 'Scikit_Learn', 'Selenium', 'Transformers', 'TypeScript', 'YOLO',
    'API_Testing', 'Automation'
}

UNIQUE_MCQS = [
    {"q": "What is the primary architectural advantage of utilizing {skill} in a distributed system?", "o": ["It ensures high availability and horizontal scalability.", "It completely eliminates the need for database backups.", "It prevents all network latency automatically.", "It is the only way to write backend services."], "c": 0, "exp": "It provides scalability benefits in distributed architectures."},
    {"q": "When optimizing a legacy application, how does {skill} improve overall performance?", "o": ["By caching objects directly in the CPU L1 cache.", "By reducing execution overhead and streamlining data flows.", "By rewriting the operating system kernel.", "It does not improve performance."], "c": 1, "exp": "It streamlines execution and data pipelines."},
    {"q": "Which of the following is considered a critical anti-pattern when developing with {skill}?", "o": ["Using descriptive variable names.", "Hardcoding sensitive credentials in plaintext.", "Refactoring monolithic code into microservices.", "Writing unit tests."], "c": 1, "exp": "Security credentials should never be hardcoded."},
    {"q": "How does {skill} manage state or data persistence across independent sessions?", "o": ["It relies on external storage or structured memory caching.", "It writes directly to the motherboard BIOS.", "It uses a localized text file on the user's desktop.", "It forces the user to manually save state."], "c": 0, "exp": "State is managed via structured memory or external DBs."},
    {"q": "What is the most effective strategy for debugging a complex issue in {skill}?", "o": ["Deploying immediately to production.", "Using breakpoints, stack trace analysis, and profiling tools.", "Deleting the code and starting over.", "Ignoring the error if the application compiles."], "c": 1, "exp": "Stack tracing and breakpoints are standard debugging tools."},
    {"q": "In a continuous integration (CI) pipeline, what role does {skill} play?", "o": ["It acts as a firewall against DDoS attacks.", "It automates validation, building, or deployment logic.", "It manages the payroll for the engineering team.", "It writes marketing copy."], "c": 1, "exp": "It is used for automation and validation in CI/CD."},
    {"q": "Which security vulnerability is most commonly mitigated by proper {skill} implementation?", "o": ["Cross-site scripting (XSS) or Injection attacks.", "Too much internal documentation.", "Over-commented source code.", "High employee turnover."], "c": 0, "exp": "Proper implementations mitigate injection and XSS."},
    {"q": "What is the standard convention for dependency management in {skill} projects?", "o": ["Downloading zip files from forums.", "Using official package managers and version lockfiles.", "Storing dependencies on floppy disks.", "Writing all third-party code from scratch."], "c": 1, "exp": "Package managers and lockfiles ensure stability."},
    {"q": "When migrating an application to the cloud, how should {skill} be configured?", "o": ["Using stateless, environment-agnostic deployment patterns.", "Hardcoding the local IP address of the developer's laptop.", "Disabling all encryption for faster speeds.", "Deploying via USB drive."], "c": 0, "exp": "Stateless configurations are required for cloud scaling."},
    {"q": "What is the primary function of the core modules provided by {skill}?", "o": ["To provide low-level abstractions and reusable logic.", "To generate CSS stylesheets.", "To replace the need for an operating system.", "To track user mouse movements."], "c": 0, "exp": "Core modules provide foundational abstractions."},
    {"q": "How does {skill} handle concurrency or asynchronous operations?", "o": ["It utilizes non-blocking I/O or threading models.", "It blocks the entire CPU until completion.", "It ignores background tasks entirely.", "It requires a manual hardware reboot."], "c": 0, "exp": "Non-blocking or threading models handle concurrency."},
    {"q": "Which design pattern is most frequently applied when architecting solutions with {skill}?", "o": ["The Singleton or Factory pattern.", "The Waterfall pattern.", "The Spaghetti code pattern.", "The 'Copy-Paste' pattern."], "c": 0, "exp": "Standard design patterns ensure maintainability."},
    {"q": "What is the best practice for handling exceptions and errors in {skill}?", "o": ["Catching them silently without logging.", "Implementing structured error handling and monitoring.", "Crashing the entire server immediately.", "Displaying the raw stack trace to the end user."], "c": 1, "exp": "Structured error handling prevents silent failures."},
    {"q": "How does {skill} ensure backward compatibility when upgrading versions?", "o": ["Through semantic versioning and deprecation cycles.", "By breaking all old code intentionally.", "By forcing users to never upgrade.", "It doesn't support versioning."], "c": 0, "exp": "Semantic versioning provides safe upgrade paths."},
    {"q": "What is the role of unit testing within a {skill} environment?", "o": ["To manually click through the UI.", "To validate individual components in isolation.", "To stress test the production database.", "To write documentation automatically."], "c": 1, "exp": "Unit tests validate components in isolation."},
    {"q": "When integrating {skill} with external APIs, what is a crucial consideration?", "o": ["Implementing rate limiting and retry logic.", "Sending unlimited requests per second.", "Ignoring authentication headers.", "Assuming the API will never experience downtime."], "c": 0, "exp": "Rate limiting and retries ensure resilience."},
    {"q": "What mechanism does {skill} use to optimize memory consumption?", "o": ["Garbage collection or manual memory allocation.", "Downloading more RAM from the internet.", "Deleting random files from the hard drive.", "Running on an infinite loop."], "c": 0, "exp": "Memory optimization is handled via GC or manual allocation."},
    {"q": "How should configuration variables be managed in a {skill} deployment?", "o": ["Through environment variables or secure vaults.", "Hardcoded in the main source file.", "Stored in a public GitHub repository.", "Written on a sticky note."], "c": 0, "exp": "Environment variables keep configurations secure."},
    {"q": "What is the primary benefit of containerizing a {skill} application?", "o": ["It ensures consistent execution environments across different machines.", "It makes the code run 100x faster.", "It prevents the need for writing tests.", "It allows the application to run without a CPU."], "c": 0, "exp": "Containers provide environmental consistency."},
    {"q": "In the context of scalability, how does {skill} perform under high load?", "o": ["It can be horizontally scaled via load balancers.", "It crashes after 10 concurrent users.", "It requires a quantum computer.", "It physically overheats the server rack."], "c": 0, "exp": "Horizontal scaling distributes high loads effectively."}
]

UNIQUE_SCENARIOS = [
    {"q": "Scenario: You are leading a team adopting {skill} for the first time. How do you ensure a smooth transition?", "o": ["Provide structured training and start with a pilot project.", "Force everyone to use it immediately with no documentation.", "Fire anyone who doesn't understand it.", "Cancel the adoption entirely."], "c": 0, "exp": "Structured training mitigates transition risks."},
    {"q": "Scenario: A critical project utilizing {skill} is behind schedule. How do you recover?", "o": ["Re-evaluate the scope, prioritize tasks, and communicate delays.", "Hide the delay from stakeholders until the deadline.", "Work 100-hour weeks without sleep.", "Abandon the project."], "c": 0, "exp": "Scope management and communication are key to recovery."},
    {"q": "Scenario: Two senior engineers disagree on the best practice for implementing {skill}. How do you resolve this?", "o": ["Facilitate a technical review to evaluate both approaches objectively.", "Flip a coin.", "Implement both simultaneously.", "Ignore them both and write it yourself."], "c": 0, "exp": "Objective technical reviews resolve disputes professionally."},
    {"q": "Scenario: A newly deployed {skill} solution is causing unexpected errors in production. What is your immediate action?", "o": ["Roll back to the previous stable version while investigating.", "Leave it running and hope it fixes itself.", "Delete the database.", "Blame the QA team publicly."], "c": 0, "exp": "Rolling back minimizes production impact during investigation."},
    {"q": "Scenario: Stakeholders want to drastically change the requirements for a {skill} project midway through development.", "o": ["Conduct an impact analysis and present the trade-offs in time and cost.", "Accept all changes blindly and miss the deadline.", "Refuse the changes entirely.", "Quit the job."], "c": 0, "exp": "Impact analysis ensures stakeholders understand the cost of changes."},
    {"q": "Scenario: You identify a severe security vulnerability in your {skill} infrastructure. What do you do?", "o": ["Follow the incident response plan to patch and disclose the issue.", "Cover it up and hope nobody notices.", "Post the exploit on a public forum.", "Wait until the next scheduled release in 6 months."], "c": 0, "exp": "Following incident response protocols is mandatory for security."},
    {"q": "Scenario: A junior team member is struggling to understand {skill}. How do you assist them?", "o": ["Offer pair programming sessions and constructive feedback.", "Assign them menial tasks instead.", "Report them to HR for incompetence.", "Tell them to figure it out alone."], "c": 0, "exp": "Mentorship and pairing accelerate junior development."},
    {"q": "Scenario: You are tasked with optimizing the cost of a {skill} deployment. Where do you start?", "o": ["Analyze resource utilization metrics to identify inefficiencies.", "Turn off random servers to save money.", "Cut the salaries of the engineering team.", "Downgrade to outdated hardware."], "c": 0, "exp": "Metrics-driven analysis identifies cost inefficiencies safely."},
    {"q": "Scenario: A third-party vendor providing {skill} services suddenly goes offline. What is your response?", "o": ["Activate the fallback/redundancy systems and contact support.", "Panic and shut down the entire company.", "Wait indefinitely for them to return.", "Switch vendors immediately without testing."], "c": 0, "exp": "Redundancy systems prevent complete outages during vendor downtime."},
    {"q": "Scenario: You must present the benefits of {skill} to a non-technical executive board. How do you approach this?", "o": ["Focus on business value, ROI, and risk mitigation.", "Read them the official API documentation line-by-line.", "Refuse to present because they won't understand.", "Make up fake statistics to sound impressive."], "c": 0, "exp": "Executives prioritize business value and ROI over technical details."}
]

# We are reverting CODING back to empty structural functions so the user can code from scratch
CODING = [
    {"q": "Implement a modular function using {skill} that processes data streams efficiently.", "code": "// Implement {skill} streaming logic\nfunction process() {\n\n}"},
    {"q": "Write a highly optimized sorting algorithm in {skill}.", "code": "// Implement {skill} sorting\nfunction sort() {\n\n}"},
    {"q": "Design an authentication middleware component using {skill}.", "code": "// {skill} middleware\nfunction auth() {\n\n}"},
    {"q": "Build a scalable data aggregation pipeline utilizing {skill}.", "code": "// {skill} aggregation pipeline\nfunction aggregate() {\n\n}"},
    {"q": "Create a fault-tolerant network request handler in {skill}.", "code": "// {skill} network handler\nfunction request() {\n\n}"}
]

# We keep DEBUGGING highly robust with actual buggy code
DEBUGGING = [
    {"q": "Identify and fix the memory leak in this {skill} class. The event listener is never removed when the component unmounts.", "code": "// BUG: Event listener causes a massive memory leak over time in {skill}\n\nclass DataHandler {\n  constructor() {\n    this.buffer = [];\n    this.listener = (e) => this.buffer.push(e.data);\n    window.addEventListener('message', this.listener);\n  }\n\n  // FIX ME: Add a teardown method to properly clean up the listener\n  teardown() {\n    // Write your fix here\n    \n  }\n}"},
    {"q": "Resolve the race condition occurring in this asynchronous {skill} process. The UI updates out of order if requests finish at different times.", "code": "// BUG: Race condition in {skill} async fetching\n\nlet currentRequestId = 0;\n\nasync function loadUserData(userId) {\n  currentRequestId++;\n  \n  // Network request takes random amount of time\n  const response = await fetchAPI(userId);\n  \n  // FIX ME: Ensure we only update UI if this response matches the most recently requested ID!\n  // Currently, it blindly updates, causing older requests to overwrite newer ones if they are slow.\n  updateUI(response.data);\n}"},
    {"q": "Fix the improper error handling in this {skill} implementation. Critical exceptions are being swallowed silently.", "code": "// BUG: Swallowed exceptions in {skill}\n\nasync function processTransaction(tx) {\n  try {\n    await db.save(tx);\n    await paymentGateway.charge(tx);\n  } catch (error) {\n    // FIX ME: This catch block completely hides the error!\n    // 1. Log the error to the monitoring service\n    // 2. Re-throw the error so the caller knows the transaction failed\n    console.log('Something went wrong');\n  }\n}"}
]

all_skills = set()
for c_data in CAREERS.values():
    for s in c_data['skills']:
        all_skills.add(s)

os.makedirs('app/data/questions', exist_ok=True)

for skill in all_skills:
    qs = []
    
    # 20 UNIQUE MCQs
    for i, t in enumerate(UNIQUE_MCQS):
        qs.append({
            "id": f"{skill}_mcq_{i}",
            "skill": skill,
            "difficulty": random.choice(["Easy", "Medium", "Hard"]),
            "question_type": "mcq",
            "question": t["q"].replace("{skill}", skill),
            "options": t["o"],
            "correct_option": t["c"],
            "explanation": t["exp"].replace("{skill}", skill)
        })

    if skill in TECHNICAL_SKILLS:
        # 5 UNIQUE CODING (Empty scaffolds)
        for i, t in enumerate(CODING):
            qs.append({
                "id": f"{skill}_coding_{i}",
                "skill": skill,
                "difficulty": "Hard",
                "question_type": "coding",
                "question": t["q"].replace("{skill}", skill),
                "default_code": t["code"].replace("{skill}", skill)
            })

        # 3 UNIQUE DEBUGGING (Robust buggy code)
        for i, t in enumerate(DEBUGGING):
            qs.append({
                "id": f"{skill}_debugging_{i}",
                "skill": skill,
                "difficulty": "Hard",
                "question_type": "debugging",
                "question": t["q"].replace("{skill}", skill),
                "default_code": t["code"].replace("{skill}", skill)
            })
    else:
        # 10 UNIQUE SCENARIOS
        for i, t in enumerate(UNIQUE_SCENARIOS):
            qs.append({
                "id": f"{skill}_scenario_{i}",
                "skill": skill,
                "difficulty": "Medium",
                "question_type": "scenario",
                "question": t["q"].replace("{skill}", skill),
                "options": t["o"],
                "correct_option": t["c"],
                "explanation": t["exp"].replace("{skill}", skill)
            })

    with open(f'app/data/questions/{skill.lower()}.json', 'w') as f:
        json.dump(qs, f, indent=4)

print("Successfully reverted Coding questions to blank scaffolds while keeping Debugging robust!")
