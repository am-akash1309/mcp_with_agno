from mcp.server.fastmcp import FastMCP
from employee import Employee

mcp = FastMCP("employee_server")


@mcp.tool()
async def add_employee(name: str, emp_id: str, pay_per_day: float, bill_address: str):
    """Add a new employee."""
    emp = Employee(name, emp_id, pay_per_day, bill_address)
    Employee.add(emp)
    return f"Employee {name} added."


@mcp.tool()
async def get_employee_info(emp_id: str) -> dict:
    """Get full employee info."""
    emp = Employee.get(emp_id)
    if not emp:
        return {"error": "Employee not found"}
    return emp.info()


@mcp.tool()
async def log_work(emp_id: str, days: int):
    """Log work days for the current month."""
    emp = Employee.get(emp_id)
    if not emp:
        return {"error": "Employee not found"}
    emp.log_work_day(days)
    return f"Logged {days} days for {emp.name}"


@mcp.tool()
async def apply_leave(emp_id: str, count: int):
    """Apply leave for the employee."""
    emp = Employee.get(emp_id)
    if not emp:
        return {"error": "Employee not found"}
    if emp.apply_leave(count):
        return f"{count} leave(s) granted to {emp.name}"
    return f"{emp.name} has insufficient leave balance"


@mcp.tool()
async def get_salary(emp_id: str) -> float:
    """Get total salary paid to the employee till now."""
    emp = Employee.get(emp_id)
    if not emp:
        return -1
    return emp.total_pay_received


if __name__ == "__main__":
    mcp.run(transport="sse")