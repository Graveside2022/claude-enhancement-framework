# Null Pointer Prevention Pattern

## Pattern Summary
**Project**: {{PROJECT_NAME}}  
**Category**: Bug Fixes  
**Framework**: Claude Enhancement Framework v1.0.0

## Problem Statement
Preventing null pointer exceptions and handling null values gracefully throughout the application.

## Solution Pattern

### Defensive Programming Approach

```python
from typing import Optional, Any, Union
from functools import wraps

def null_safe(func):
    """Decorator to handle null values in function parameters"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Filter out None values from args
        safe_args = [arg for arg in args if arg is not None]
        safe_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        
        if len(safe_args) != len(args) or len(safe_kwargs) != len(kwargs):
            return None  # Or raise custom exception
        
        return func(*safe_args, **safe_kwargs)
    return wrapper

class NullSafeAccessor:
    """Safe accessor for nested object properties"""
    
    @staticmethod
    def safe_get(obj: Any, *keys: str, default: Any = None) -> Any:
        """Safely access nested object properties"""
        try:
            for key in keys:
                if obj is None:
                    return default
                if hasattr(obj, key):
                    obj = getattr(obj, key)
                elif isinstance(obj, dict) and key in obj:
                    obj = obj[key]
                else:
                    return default
            return obj if obj is not None else default
        except (AttributeError, KeyError, TypeError):
            return default
    
    @staticmethod
    def safe_call(obj: Any, method_name: str, *args, **kwargs) -> Any:
        """Safely call method on object"""
        if obj is None:
            return None
        
        method = getattr(obj, method_name, None)
        if method is None or not callable(method):
            return None
        
        try:
            return method(*args, **kwargs)
        except Exception:
            return None

# Optional pattern implementation
class Maybe:
    """Optional-like pattern for handling nullable values"""
    
    def __init__(self, value: Any):
        self._value = value
    
    @classmethod
    def of(cls, value: Any):
        return cls(value)
    
    @classmethod
    def empty(cls):
        return cls(None)
    
    def is_present(self) -> bool:
        return self._value is not None
    
    def get(self) -> Any:
        if self._value is None:
            raise ValueError("No value present")
        return self._value
    
    def or_else(self, default: Any) -> Any:
        return self._value if self._value is not None else default
    
    def map(self, func):
        if self._value is None:
            return Maybe.empty()
        try:
            return Maybe.of(func(self._value))
        except Exception:
            return Maybe.empty()
    
    def filter(self, predicate):
        if self._value is None or not predicate(self._value):
            return Maybe.empty()
        return self
```

### Validation and Checking Patterns

```python
# Input validation patterns
def validate_input(data: dict, required_fields: list) -> dict:
    """Validate required fields are present and not None"""
    errors = []
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif data[field] is None:
            errors.append(f"Field cannot be null: {field}")
    
    if errors:
        raise ValueError(f"Validation errors: {', '.join(errors)}")
    
    return data

# Database query safety
class SafeDBQuery:
    """Safe database query patterns"""
    
    @staticmethod
    def safe_query_one(session, model, **filters):
        """Safely query single record"""
        try:
            result = session.query(model).filter_by(**filters).first()
            return Maybe.of(result)
        except Exception:
            return Maybe.empty()
    
    @staticmethod
    def safe_query_all(session, model, **filters):
        """Safely query multiple records"""
        try:
            results = session.query(model).filter_by(**filters).all()
            return results if results else []
        except Exception:
            return []
```

## Implementation Checklist

- [ ] Add null checks before object property access
- [ ] Implement safe accessor patterns for nested objects
- [ ] Use Optional/Maybe patterns for nullable return values
- [ ] Add input validation for all public methods
- [ ] Implement defensive copying for mutable objects
- [ ] Add logging for null value encounters
- [ ] Create unit tests for null scenarios
- [ ] Document nullable parameters and return values

## Common Null Scenarios

### API Response Handling
```python
def process_api_response(response_data: dict) -> Optional[str]:
    """Process API response with null safety"""
    if not response_data:
        return None
    
    # Safe nested access
    user_name = NullSafeAccessor.safe_get(
        response_data, 'user', 'profile', 'name', 
        default="Unknown User"
    )
    
    return user_name
```

### Configuration Loading
```python
def load_config(config_path: str) -> dict:
    """Load configuration with null safety"""
    default_config = {
        'database_url': 'sqlite:///default.db',
        'debug': False,
        'api_key': None
    }
    
    try:
        with open(config_path, 'r') as f:
            user_config = json.load(f)
        
        # Merge with defaults, handling None values
        for key, value in user_config.items():
            if value is not None:
                default_config[key] = value
        
        return default_config
    except (FileNotFoundError, json.JSONDecodeError):
        return default_config
```

## Prevention Strategies

1. **Initialize variables** with default values
2. **Validate inputs** at method entry points
3. **Use defensive copying** for mutable parameters
4. **Implement builder patterns** for complex object construction
5. **Add null object patterns** where appropriate
6. **Use type hints** to indicate nullable types

## Validation Criteria

✅ **All public methods validate input parameters**  
✅ **Nested object access uses safe accessors**  
✅ **Nullable return types are clearly documented**  
✅ **Unit tests cover null input scenarios**  
✅ **Error messages are descriptive and actionable**

---

**Generated**: {{USER_NAME}} | Claude Enhancement Framework v1.0.0  
**Project**: {{PROJECT_NAME}} | **Path**: {{PROJECT_PATH}}