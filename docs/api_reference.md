# API Reference for VulnVortex

This document details the functions, classes, and modules available in VulnVortex.

## **Modules**

### **Core Module**
Handles the primary logic of VulnVortex.

#### Functions:
- `run_scan(target: str, depth: int, exclude: List[str]) -> dict`  
  Initiates a scan on the specified target.

---

### **CLI Module**
Provides a command-line interface for VulnVortex.

#### Functions:
- `main()`  
  Parses arguments and invokes corresponding core functions.

---

### **Utilities**
Utility functions for internal use.

#### Functions:
- `validate_config(config: dict) -> bool`  
  Validates the provided configuration.

---

For detailed inline documentation, refer to the source code.
