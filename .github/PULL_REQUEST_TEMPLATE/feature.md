## ✨ New Feature

### Feature Description
<!-- Clear description of the new feature -->

**What does this feature do?**


**Why is this feature needed?**


**Who requested this feature?**
- [ ] User request (Issue #___)
- [ ] Roadmap item
- [ ] Personal initiative
- [ ] Dependency requirement

## Related Issues
Closes #
Relates to #

## Design & Implementation

### Feature Overview
<!-- High-level overview of how the feature works -->


### Architecture Decisions
<!-- Explain key architectural decisions -->

**Why this approach?**


**Alternatives considered:**
1. 
2. 

### Design Patterns Used
- [ ] Strategy Pattern
- [ ] Factory Pattern
- [ ] Builder Pattern
- [ ] Singleton Pattern
- [ ] Observer Pattern
- [ ] Other: ___________

## Changes Made

### New Components
- `dotzen/module/new_class.py` - Description
- `dotzen/module/helper.py` - Description

### Modified Components
- `dotzen/config.py` - Added integration
- `dotzen/__init__.py` - Exported new API

### New Dependencies
<!-- List any new dependencies -->
- **package-name** `^1.0.0` - Reason for adding

## Usage Examples

### Basic Usage
```python
from dotzen import config, ConfigBuilder

# Example of using the new feature
result = config.new_feature('param')
```

### Advanced Usage
```python
# More complex example
builder = ConfigBuilder()
builder.use_new_feature(
    option1='value1',
    option2='value2'
)
config = builder.build()
```

### Integration Example
```python
# Example showing integration with existing features
```

## API Reference

### New Public APIs
```python
def new_function(param: str) -> Result:
    """
    Brief description.
    
    Args:
        param: Description
        
    Returns:
        Description
        
    Raises:
        ValueError: When...
    """
```

### Breaking Changes
- [ ] No breaking changes
- [ ] Breaking changes (documented below)

**If breaking changes:**
```python
# Old way
old_api()

# New way
new_api()
```

## Documentation

### Documentation Added
- [ ] Docstrings for all new functions/classes
- [ ] Usage guide in `/docs`
- [ ] API reference updated
- [ ] Examples added to `/examples`
- [ ] README.md updated (if needed)
- [ ] CHANGELOG.md updated

### Documentation Links
- User guide: `/docs/features/new-feature.md`
- API docs: `/docs/api/new-module.md`
- Examples: `/examples/new-feature/`

## Testing

### Test Coverage
- [ ] Unit tests added (>90% coverage)
- [ ] Integration tests added
- [ ] Example tests added
- [ ] Edge cases covered
- [ ] Error handling tested

### Test Files
- `tests/test_new_feature.py` - Core functionality
- `tests/integration/test_new_feature_integration.py` - Integration tests

### Test Results
```bash
pytest tests/test_new_feature.py -v --cov
# Coverage: X%
```

### Manual Testing
- [ ] Tested with Python 3.8
- [ ] Tested with Python 3.12
- [ ] Tested with optional dependencies
- [ ] Tested without optional dependencies
- [ ] Tested on multiple platforms

## Performance Impact

### Performance Benchmarks
```
Operation: X operations/second
Memory: Y MB
Startup time: Z ms
```

### Optimization Notes
<!-- Any performance considerations or optimizations -->


## Backward Compatibility
- [ ] Fully backward compatible
- [ ] Opt-in feature (no impact on existing code)
- [ ] Requires migration (breaking change)

## Security Considerations
- [ ] No security implications
- [ ] Security review completed
- [ ] Input validation added
- [ ] No sensitive data exposed

## Checklist
- [ ] Feature complete and working
- [ ] Code follows style guidelines
- [ ] Type hints added
- [ ] Documentation complete
- [ ] Tests comprehensive (>90% coverage)
- [ ] Examples provided
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented)
- [ ] Performance acceptable
- [ ] Security reviewed

## Screenshots/Demo
<!-- If applicable, add screenshots or demo -->


## Future Enhancements
<!-- Ideas for future improvements to this feature -->
- 
- 

## Additional Notes

