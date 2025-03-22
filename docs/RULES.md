# Solara AI Data Analysis - Interaction Rules

This document defines the rules for how we interact and when to update documentation in this project. These rules ensure consistency and clarity throughout the development process.

## Documentation Update Rules

<documentation_rules>
- **TECHNICAL.md**: Only update when the user explicitly confirms they are happy with the implementation and it should be included in the documentation.
- **PRD.md**: Only update when there's a confirmed change by the user that affects product requirements or specifications.
- **ROADMAP.md**: Only update when the user confirms a change to the roadmap, either based on the user's suggestions or AI suggestions that the user approves.
- Never update any documentation files without explicit user confirmation.
- When suggesting documentation updates, clearly indicate which document would be updated and why.
</documentation_rules>

## Code Implementation Rules

<code_rules>
- Always implement code in the develop branch for experimentation before merging to main.
- When implementing new features, ensure they align with the PRD and ROADMAP documents.
- Follow best practices for Solara applications and Python code.
- Ensure all code is well-documented with comments and docstrings.
- Always handle errors gracefully with appropriate user feedback.
- Prioritize code readability and maintainability over cleverness.
</code_rules>

## Communication Rules

<communication_rules>
- Be concise and clear in all responses.
- When suggesting changes, provide clear rationales and potential alternatives.
- When encountering errors, explain the issue clearly and suggest solutions.
- Always acknowledge user preferences and priorities.
- When researching solutions, explain the approach and findings.
- Provide regular status updates during complex implementations.
</communication_rules>

## Git Workflow Rules

<git_rules>
- Use descriptive commit messages that clearly explain the changes made.
- Keep commits focused on specific changes or features.
- Use the develop branch for all experimental work.
- Only merge to main when features are complete and tested.
- Tag significant releases with version numbers.
- Follow semantic versioning (MAJOR.MINOR.PATCH) for version numbers.
</git_rules>

## Feature Implementation Process

<feature_process>
1. **Planning**: Discuss the feature and ensure it's aligned with the PRD.
2. **Documentation**: Update ROADMAP.md (with user approval) to include the feature.
3. **Implementation**: Develop the feature in the develop branch.
4. **Testing**: Test the feature thoroughly and fix any issues.
5. **Review**: Have the user review and approve the implementation.
6. **Documentation**: Update TECHNICAL.md (with user approval) to include the new feature.
7. **Merge**: Merge the feature to the main branch when ready.
</feature_process>

## Bug Fixing Process

<bug_process>
1. **Identification**: Clearly identify and reproduce the bug.
2. **Analysis**: Determine the root cause of the bug.
3. **Fix**: Implement a fix in the develop branch.
4. **Testing**: Verify the fix resolves the issue without introducing new problems.
5. **Documentation**: Update TECHNICAL.md if the fix involves significant changes (with user approval).
6. **Merge**: Merge the fix to the main branch when ready.
</bug_process>

---

These rules are designed to ensure a smooth and productive development process. They may be updated as the project evolves, but only with explicit user approval.
