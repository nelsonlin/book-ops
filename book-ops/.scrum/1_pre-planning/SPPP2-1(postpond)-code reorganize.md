title: "25-Min Sprint: Code Reorganization for gemini-cli & kilo Workflow"
issue: "nelsonlin/book-ops#2", book-ops\docs\issue\IS2(open)-code reorganize.md
timeboxed: "25 minutes"
phases:

  phase_1:
    name: "Discovery & Audit (7 mins)"
    description: "Map current codebase structure"
    tasks:
      - task: "List all directories and files in the repo"
        time: "2 mins"
        action: TBD 
        
      - task: "Identify gemini-cli related files"
        time: "2 mins"
        action: TBD 
        
      - task: "Identify kilo code related files"
        time: "2 mins"
        action: TBD
        
      - task: "Document current structure"
        time: "1 min"
        action: "Create a simple ASCII tree diagram in notes"

  phase_2:
    name: "Design Proposed Architecture (10 mins)"
    description: "Plan reorganization strategy"
    tasks:
      - task: "Define pipeline stages"
        time: "3 mins"
        subtasks:
          - "Input stage"
          - "Processing stage"
          - "Integration stage"
          - "Output stage"
        
      - task: "Create proposed folder structure"
        time: "4 mins"
        example structure: |
          src/
          ├── pipeline/
          │   ├── input/         
          │   ├── processing/     
          │   ├── integration/    
          │   ├── output/         
          │   └── core/           
          ├── config/             
          └── tests/              
        
      - task: "Document rationale"
        time: "3 mins"
        action: "Write brief notes on why each layer exists and its responsibility"

  phase_3:
    name: "Create Action Plan Document (8 mins)"
    description: "Generate migration roadmap"
    tasks:
      - task: "Create ARCHITECTURE_proposed.md"
        time: "4 mins"
        sections:
          - "Current vs Proposed Structure comparison table"
          - "Migration steps (phased approach)"
          - "Dependencies to watch"
          - "Rollback plan"
        
      - task: "Identify migration priorities"
        time: "2 mins"
        action: "List which files/modules should move first (lowest dependencies first)"
        
      - task: "Estimate effort per phase"
        time: "2 mins"
        action: "Break refactoring into 3-4 implementable chunks for future sprints"

  deliverables:
    - "ARCHITECTURE_proposed.md with proposed structure and rationale"
    - "ASCII tree diagram of both current and proposed layouts"
    - "Migration checklist with prioritized file movements"
    - "Comments added to #2 documenting findings and next steps"

timeline:
  - "0-7 min: Discovery phase"
  - "7-17 min: Design phase"
  - "17-25 min: Documentation phase"
  - "Goal: Exit with clear plan, no code changes yet (prep work only)"

success_criteria:
  - "Team has clear visual understanding of proposed structure"
  - "Dependencies between components are mapped"
  - "Next sprint has concrete first-step migration tasks ready"
  - "ARCHITECTURE_proposed.md provides reference for future contributors"