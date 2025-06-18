# Side Effects Log
Created: {{CREATION_DATE}}
User: {{USER_NAME}}

## Automated Side Effects Tracking
This log captures unexpected consequences of changes and executions across the {{PROJECT_NAME}} system.

## Known Side Effects
<!-- Document unexpected consequences of changes -->

## Automated Triggers
- Pattern execution side effects
- File system changes
- Configuration modifications
- Session state changes
- Error cascades

## Side Effects Template
```
### Side Effect - {{TIMESTAMP}}
**Source**: {{SOURCE_OPERATION}}
**Description**: {{SIDE_EFFECT_DESCRIPTION}}
**Impact**: {{IMPACT_LEVEL}}
**Files Affected**: {{AFFECTED_FILES}}
**Trigger**: {{TRIGGERING_ACTION}}
**Resolution**: {{RESOLUTION_STATUS}}
---
```

## Configuration Parameters
- **Project Name**: {{PROJECT_NAME}}
- **User**: {{USER_NAME}}
- **Framework Version**: {{FRAMEWORK_VERSION}}
- **Side Effect Tracking**: {{SIDE_EFFECT_TRACKING_ENABLED}}
- **Auto-logging**: {{AUTO_LOGGING_ENABLED}}

## Impact Levels
- **low**: Minimal impact, informational
- **medium**: Notable changes, monitoring required
- **high**: Significant impact, immediate attention needed
- **critical**: System-affecting changes, intervention required

## Resolution Status Types
- **pending**: Side effect identified, resolution pending
- **monitoring**: Under observation for further effects
- **resolved**: Side effect addressed and closed
- **accepted**: Side effect acknowledged as expected behavior