import datetime
from typing import Dict

class Employee:
    _db: Dict[str, "Employee"] = {}

    def __init__(
        self,
        name: str,
        emp_id: str,
        pay_per_day: float,
        bill_address: str
    ):
        self.name = name
        self.emp_id = emp_id
        self.pay_per_day = pay_per_day
        self.bill_address = bill_address

        self.leaves_remaining = 2  # Start with 2 for the first month
        self.days_worked = {}  # { "2025-08": 15, ... }
        self.total_pay_received = 0.0

        self.last_updated_month = self.current_month()

    @classmethod
    def current_month(cls):
        return datetime.datetime.now().strftime("%Y-%m")

    @classmethod
    def get(cls, emp_id: str) -> "Employee":
        emp = cls._db.get(emp_id)
        if emp:
            emp._update_monthly_state()
        return emp

    @classmethod
    def add(cls, employee: "Employee"):
        cls._db[employee.emp_id] = employee

    def _update_monthly_state(self):
        current_month = self.current_month()
        if self.last_updated_month != current_month:
            # carry forward unused leaves
            self.leaves_remaining += 2
            self.last_updated_month = current_month

    def log_work_day(self, days: int):
        month = self.current_month()
        self._update_monthly_state()
        self.days_worked[month] = self.days_worked.get(month, 0) + days
        self.total_pay_received += days * self.pay_per_day

    def apply_leave(self, count: int) -> bool:
        self._update_monthly_state()
        if self.leaves_remaining >= count:
            self.leaves_remaining -= count
            return True
        return False

    def info(self) -> Dict:
        self._update_monthly_state()
        return {
            "name": self.name,
            "employee_id": self.emp_id,
            "pay_per_day": self.pay_per_day,
            "bill_address": self.bill_address,
            "leaves_remaining": self.leaves_remaining,
            "days_worked": self.days_worked,
            "total_pay_received": self.total_pay_received
        }
