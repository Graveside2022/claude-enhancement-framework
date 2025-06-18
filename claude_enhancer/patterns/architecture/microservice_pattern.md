# Microservice Architecture Pattern

## Pattern Summary
**Project**: {{PROJECT_NAME}}  
**Category**: Architecture  
**Framework**: Claude Enhancement Framework v1.0.0

## Problem Statement
Breaking down monolithic applications into manageable microservices with proper separation of concerns.

## Solution Pattern

### Core Components
1. **Service Discovery**: Dynamic service registration and lookup
2. **API Gateway**: Centralized routing and security
3. **Configuration Management**: Centralized configuration with environment-specific overrides
4. **Health Monitoring**: Service health checks and metrics collection

### Implementation Template

```python
# Service base class
class BaseService:
    def __init__(self, service_name: str, config: Dict[str, Any]):
        self.service_name = service_name
        self.config = config
        self.health_check_url = f"/health/{service_name}"
    
    def register_service(self):
        """Register service with discovery mechanism"""
        # {{IMPLEMENTATION}}
        pass
    
    def health_check(self) -> Dict[str, Any]:
        """Service health check endpoint"""
        return {
            "service": self.service_name,
            "status": "healthy",
            "timestamp": "{{CUSTOM_LOGIC}}"
        }

# API Gateway integration
class APIGateway:
    def route_request(self, path: str, method: str):
        """Route requests to appropriate microservice"""
        # {{PATTERN_CONTENT}}
        pass
```

### Configuration Pattern

```yaml
# docker-compose.yml template
version: '3.8'
services:
  {{PROJECT_SPECIFIC}}_service:
    build: .
    environment:
      - SERVICE_NAME={{PROJECT_NAME}}_service
      - CONFIG_URL=http://config-server:8888
    ports:
      - "8080:8080"
    depends_on:
      - config-server
      - service-discovery
```

## Implementation Checklist

- [ ] Define service boundaries and responsibilities
- [ ] Implement service discovery mechanism
- [ ] Set up API gateway for request routing
- [ ] Configure centralized logging and monitoring
- [ ] Implement circuit breaker pattern for resilience
- [ ] Set up automated deployment pipeline
- [ ] Create health check endpoints for all services
- [ ] Document service APIs and contracts

## Anti-Patterns to Avoid

1. **Distributed Monolith**: Services too tightly coupled
2. **Chatty Services**: Excessive inter-service communication
3. **Shared Database**: Multiple services accessing same database
4. **Synchronous Communication**: Over-reliance on synchronous calls

## Performance Considerations

- Use asynchronous communication where possible
- Implement caching strategies at service and gateway levels
- Monitor service response times and implement timeouts
- Use connection pooling for database connections

## Validation Criteria

✅ **Services are independently deployable**  
✅ **Clear service boundaries and responsibilities**  
✅ **Proper error handling and circuit breakers**  
✅ **Comprehensive monitoring and alerting**  
✅ **Automated testing for each service**

---

**Generated**: {{USER_NAME}} | Claude Enhancement Framework v1.0.0  
**Project**: {{PROJECT_NAME}} | **Path**: {{PROJECT_PATH}}